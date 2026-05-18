#include "virtualserialmanager.h"
#include <QRegularExpression>
#include <QFile>
#include <QDebug>
#include <termios.h>
#include <unistd.h>
#include <fcntl.h>

static const char* VPORT_SYMLINK = "/tmp/mousart_vport";

VirtualSerialManager::VirtualSerialManager(QObject *parent)
    : QObject(parent)
{
    connect(&m_socat, &QProcess::readyReadStandardOutput, this, &VirtualSerialManager::onSocatOutput);
    connect(&m_socat, &QProcess::readyReadStandardError, this, &VirtualSerialManager::onSocatOutput);
    connect(&m_socat, QOverload<int, QProcess::ExitStatus>::of(&QProcess::finished),
            this, &VirtualSerialManager::onSocatFinished);

    m_timedSendTimer.setTimerType(Qt::PreciseTimer);
    connect(&m_timedSendTimer, &QTimer::timeout, this, &VirtualSerialManager::onTimedSendTick);
}

VirtualSerialManager::~VirtualSerialManager()
{
    stopVirtualPort();
}

bool VirtualSerialManager::startVirtualPort()
{
    if (m_socat.state() == QProcess::Running) {
        stopVirtualPort();
    }

    m_ptyA.clear();
    m_ptyB.clear();
    m_waitingForPorts = true;

    m_socat.start("socat", QStringList()
                     << "-d" << "-d"
                     << "pty,raw,echo=0"
                     << QString("pty,raw,echo=0,link=%1").arg(VPORT_SYMLINK));

    if (!m_socat.waitForStarted(3000)) {
        m_waitingForPorts = false;
        emit errorOccurred(tr("启动 socat 失败: ") + m_socat.errorString());
        return false;
    }

    return true;
}

void VirtualSerialManager::stopVirtualPort()
{
    m_waitingForPorts = false;
    stopTimedSend();

    if (m_readNotifier) {
        m_readNotifier->setEnabled(false);
        delete m_readNotifier;
        m_readNotifier = nullptr;
    }

    if (m_fd >= 0) {
        ::close(m_fd);
        m_fd = -1;
    }

    if (m_socat.state() == QProcess::Running) {
        m_socat.terminate();
        if (!m_socat.waitForFinished(2000)) {
            m_socat.kill();
            m_socat.waitForFinished(1000);
        }
    }

    m_ptyA.clear();
    m_ptyB.clear();
    QFile::remove(VPORT_SYMLINK);
    emit isActiveChanged();
    emit externalPortChanged();
}

qint64 VirtualSerialManager::sendData(const QString &data, bool hexMode)
{
    if (m_fd < 0) {
        emit errorOccurred(tr("虚拟串口未打开"));
        return -1;
    }

    QByteArray bytes;
    if (hexMode) {
        QString hex = QString(data).remove(' ').remove('\n').remove('\r');
        bytes = QByteArray::fromHex(hex.toUtf8());
    } else {
        bytes = data.toUtf8();
    }

    qint64 written = ::write(m_fd, bytes.constData(), bytes.size());
    if (written == -1) {
        emit errorOccurred(QString::fromLocal8Bit(strerror(errno)));
    }
    return written;
}

void VirtualSerialManager::startTimedSend(const QString &data, bool hexMode, int intervalMs)
{
    if (m_fd < 0) {
        emit errorOccurred(tr("虚拟串口未打开"));
        return;
    }
    m_timedSendData = data;
    m_timedSendHexMode = hexMode;
    m_timedSendTimer.setInterval(qMax(intervalMs, 1));
    m_timedSendTimer.start();
    emit timedSendActiveChanged();
}

void VirtualSerialManager::stopTimedSend()
{
    m_timedSendTimer.stop();
    emit timedSendActiveChanged();
}

void VirtualSerialManager::onTimedSendTick()
{
    if (m_fd < 0) {
        stopTimedSend();
        return;
    }
    qint64 result = sendData(m_timedSendData, m_timedSendHexMode);
    if (result > 0)
        emit timedSendCompleted(m_timedSendData);
}

void VirtualSerialManager::onSocatOutput()
{
    QByteArray output = m_socat.readAllStandardOutput() + m_socat.readAllStandardError();
    QString text = QString::fromUtf8(output);

    if (!m_waitingForPorts) return;

    // Parse PTY paths: "N PTY is /dev/pts/X"
    QRegularExpression re(R"(PTY is (\S+))");
    QRegularExpressionMatchIterator it = re.globalMatch(text);

    while (it.hasNext()) {
        QRegularExpressionMatch match = it.next();
        QString pty = match.captured(1);
        if (m_ptyA.isEmpty()) {
            m_ptyA = pty;
        } else if (m_ptyB.isEmpty() && pty != m_ptyA) {
            m_ptyB = pty;
        }
    }

    if (!m_ptyA.isEmpty() && !m_ptyB.isEmpty()) {
        m_waitingForPorts = false;
        qWarning() << "[MOUSART] Virtual port: A=" << m_ptyA << "(self) B=" << m_ptyB << "(external)";
        openSideA();
    }
}

void VirtualSerialManager::openSideA()
{
    // Open PTY slave with raw fd — bypass QSerialPort to avoid interference with socat
    m_fd = ::open(m_ptyA.toLocal8Bit().constData(), O_RDWR | O_NOCTTY | O_NONBLOCK);
    if (m_fd < 0) {
        emit errorOccurred(tr("无法打开虚拟串口A端: ") + QString::fromLocal8Bit(strerror(errno)));
        return;
    }

    // Configure raw mode
    struct termios tio;
    if (tcgetattr(m_fd, &tio) == 0) {
        cfmakeraw(&tio);
        tio.c_cc[VMIN] = 0;
        tio.c_cc[VTIME] = 1;
        // Disable echo
        tio.c_lflag &= ~(ECHO | ECHONL | ECHOE | ICANON);
        tio.c_oflag &= ~(ONLCR | OCRNL);
        tcsetattr(m_fd, TCSANOW, &tio);
    }

    // Set non-blocking
    int flags = fcntl(m_fd, F_GETFL, 0);
    if (flags >= 0) fcntl(m_fd, F_SETFL, flags & ~O_NONBLOCK);

    // Use QSocketNotifier for async reads
    m_readNotifier = new QSocketNotifier(m_fd, QSocketNotifier::Read, this);
    connect(m_readNotifier, &QSocketNotifier::activated, this, &VirtualSerialManager::onFdReadyRead);
    m_readNotifier->setEnabled(true);

    qWarning() << "[MOUSART] Side A opened:" << m_ptyA;
    emit isActiveChanged();
    emit externalPortChanged();
}

void VirtualSerialManager::onSocatFinished(int exitCode, QProcess::ExitStatus status)
{
    Q_UNUSED(exitCode)
    Q_UNUSED(status)

    if (m_readNotifier) {
        m_readNotifier->setEnabled(false);
        delete m_readNotifier;
        m_readNotifier = nullptr;
    }
    if (m_fd >= 0) {
        ::close(m_fd);
        m_fd = -1;
    }
    m_ptyA.clear();
    m_ptyB.clear();
    m_waitingForPorts = false;
    QFile::remove(VPORT_SYMLINK);
    emit isActiveChanged();
    emit externalPortChanged();
}

void VirtualSerialManager::onFdReadyRead(int fd)
{
    char buf[4096];
    ssize_t n = ::read(fd, buf, sizeof(buf));
    if (n > 0) {
        QByteArray data(buf, n);
        QString text = QString::fromUtf8(data);
        emit dataReceived(text, data);
    }
}
