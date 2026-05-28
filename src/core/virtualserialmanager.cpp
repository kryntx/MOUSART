#include "virtualserialmanager.h"
#include <QFile>
#include <QDebug>
#include <QTextCodec>

#ifdef Q_OS_WIN
#include <QSerialPortInfo>
#else
#include <QRegularExpression>
#include <QProcess>
#include <termios.h>
#include <unistd.h>
#include <fcntl.h>

static const char* VPORT_SYMLINK = "/tmp/mousart_vport";
#endif

VirtualSerialManager::VirtualSerialManager(QObject *parent)
    : QObject(parent)
{
#ifndef Q_OS_WIN
    connect(&m_socat, &QProcess::readyReadStandardOutput, this, &VirtualSerialManager::onSocatOutput);
    connect(&m_socat, &QProcess::readyReadStandardError, this, &VirtualSerialManager::onSocatOutput);
    connect(&m_socat, QOverload<int, QProcess::ExitStatus>::of(&QProcess::finished),
            this, &VirtualSerialManager::onSocatFinished);
#endif

    m_timedSendTimer.setTimerType(Qt::PreciseTimer);
    connect(&m_timedSendTimer, &QTimer::timeout, this, &VirtualSerialManager::onTimedSendTick);

    // Stats timer
    m_statsTimer.start();
    m_statsUpdateTimer.setInterval(1000);
    connect(&m_statsUpdateTimer, &QTimer::timeout, this, [this]() {
        m_rxBytesSnapshot = m_rxBytes;
        m_txBytesSnapshot = m_txBytes;
        m_statsTimer.restart();
        emit statsChanged();
    });
    m_statsUpdateTimer.start();
}

VirtualSerialManager::~VirtualSerialManager()
{
    stopVirtualPort();
}

bool VirtualSerialManager::startVirtualPort()
{
#ifdef Q_OS_WIN
    emit errorOccurred(tr("虚拟串口功能在 Windows 上暂不可用，请使用硬件串口调试模式。"));
    return false;
#else
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
#endif
}

void VirtualSerialManager::stopVirtualPort()
{
    stopTimedSend();

#ifdef Q_OS_WIN
    if (m_winPort) {
        m_winPort->close();
        delete m_winPort;
        m_winPort = nullptr;
        emit isActiveChanged();
        emit externalPortChanged();
    }
#else
    m_waitingForPorts = false;

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
#endif
}

qint64 VirtualSerialManager::sendData(const QString &data, bool hexMode)
{
#ifdef Q_OS_WIN
    if (!m_winPort || !m_winPort->isOpen()) {
        emit errorOccurred(tr("虚拟串口未打开"));
        return -1;
    }

    QByteArray bytes;
    if (hexMode) {
        QString hex = QString(data).remove(' ').remove('\n').remove('\r');
        bytes = QByteArray::fromHex(hex.toUtf8());
    } else {
        QString text = data;
        if (m_newlineCr) text += "\r";
        if (m_newlineLf) text += "\n";
        bytes = text.toUtf8();
    }

    qint64 written = m_winPort->write(bytes);
    if (written == -1) {
        emit errorOccurred(m_winPort->errorString());
    } else {
        m_txBytes += written;
        emit statsChanged();
    }
    return written;
#else
    if (m_fd < 0) {
        emit errorOccurred(tr("虚拟串口未打开"));
        return -1;
    }

    QByteArray bytes;
    if (hexMode) {
        QString hex = QString(data).remove(' ').remove('\n').remove('\r');
        bytes = QByteArray::fromHex(hex.toUtf8());
    } else {
        QString text = data;
        if (m_newlineCr) text += "\r";
        if (m_newlineLf) text += "\n";
        bytes = text.toUtf8();
    }

    qint64 written = ::write(m_fd, bytes.constData(), bytes.size());
    if (written == -1) {
        emit errorOccurred(QString::fromLocal8Bit(strerror(errno)));
    } else {
        m_txBytes += written;
        emit statsChanged();
    }
    return written;
#endif
}

void VirtualSerialManager::startTimedSend(const QString &data, bool hexMode, int intervalMs, int count)
{
    if (!isActive()) {
        emit errorOccurred(tr("虚拟串口未打开"));
        return;
    }
    m_timedSendData = data;
    m_timedSendHexMode = hexMode;
    m_timedSendCount = count;
    m_timedSendSent = 0;
    m_timedSendTimer.setInterval(qMax(intervalMs, 1));
    m_timedSendTimer.start();
    emit timedSendActiveChanged();
}

void VirtualSerialManager::stopTimedSend()
{
    m_timedSendTimer.stop();
    m_timedSendSent = 0;
    m_timedSendCount = -1;
    emit timedSendActiveChanged();
}

void VirtualSerialManager::onTimedSendTick()
{
    if (!isActive()) {
        stopTimedSend();
        return;
    }
    qint64 result = sendData(m_timedSendData, m_timedSendHexMode);
    if (result > 0) {
        m_timedSendSent++;
        emit timedSendCompleted(m_timedSendData);
        if (m_timedSendCount > 0 && m_timedSendSent >= m_timedSendCount) {
            stopTimedSend();
        }
    }
}

// Stats
double VirtualSerialManager::rxRate() const
{
    qint64 elapsed = m_statsTimer.elapsed();
    if (elapsed < 100) return 0.0;
    return (double)(m_rxBytes - m_rxBytesSnapshot) * 1000.0 / elapsed;
}

double VirtualSerialManager::txRate() const
{
    qint64 elapsed = m_statsTimer.elapsed();
    if (elapsed < 100) return 0.0;
    return (double)(m_txBytes - m_txBytesSnapshot) * 1000.0 / elapsed;
}

void VirtualSerialManager::resetStats()
{
    m_rxBytes = 0;
    m_txBytes = 0;
    m_rxBytesSnapshot = 0;
    m_txBytesSnapshot = 0;
    m_statsTimer.restart();
    emit statsChanged();
}

// Settings
void VirtualSerialManager::setEchoEnabled(bool enabled)
{
    if (m_echoEnabled == enabled) return;
    m_echoEnabled = enabled;
    emit echoEnabledChanged();
}

void VirtualSerialManager::setNewlineCr(bool v)
{
    if (m_newlineCr == v) return;
    m_newlineCr = v;
    emit newlineChanged();
}

void VirtualSerialManager::setNewlineLf(bool v)
{
    if (m_newlineLf == v) return;
    m_newlineLf = v;
    emit newlineChanged();
}

void VirtualSerialManager::setReceiveEncoding(const QString &enc)
{
    if (m_receiveEncoding == enc) return;
    m_receiveEncoding = enc;
    emit receiveEncodingChanged();
}

QString VirtualSerialManager::decodeData(const QByteArray &data) const
{
    if (m_receiveEncoding == "UTF-8") {
        return QString::fromUtf8(data);
    } else if (m_receiveEncoding == "GBK" || m_receiveEncoding == "GB18030") {
        QTextCodec *codec = QTextCodec::codecForName(m_receiveEncoding.toUtf8());
        if (codec) return codec->toUnicode(data);
        return QString::fromLocal8Bit(data);
    } else if (m_receiveEncoding == "Latin-1") {
        return QString::fromLatin1(data);
    } else if (m_receiveEncoding == "ASCII") {
        QString result;
        for (char c : data) {
            if (c >= 0x20 && c <= 0x7E) result += QChar(c);
            else result += QString("\\x%1").arg((unsigned char)c, 2, 16, QChar('0'));
        }
        return result;
    }
    return QString::fromUtf8(data);
}

#ifndef Q_OS_WIN
void VirtualSerialManager::onSocatOutput()
{
    QByteArray output = m_socat.readAllStandardOutput() + m_socat.readAllStandardError();
    QString text = QString::fromUtf8(output);

    if (!m_waitingForPorts) return;

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
    m_fd = ::open(m_ptyA.toLocal8Bit().constData(), O_RDWR | O_NOCTTY | O_NONBLOCK);
    if (m_fd < 0) {
        emit errorOccurred(tr("无法打开虚拟串口A端: ") + QString::fromLocal8Bit(strerror(errno)));
        return;
    }

    struct termios tio;
    if (tcgetattr(m_fd, &tio) == 0) {
        cfmakeraw(&tio);
        tio.c_cc[VMIN] = 0;
        tio.c_cc[VTIME] = 1;
        tio.c_lflag &= ~(ECHO | ECHONL | ECHOE | ICANON);
        tio.c_oflag &= ~(ONLCR | OCRNL);
        tcsetattr(m_fd, TCSANOW, &tio);
    }

    int flags = fcntl(m_fd, F_GETFL, 0);
    if (flags >= 0) fcntl(m_fd, F_SETFL, flags & ~O_NONBLOCK);

    m_readNotifier = new QSocketNotifier(m_fd, QSocketNotifier::Read, this);
    connect(m_readNotifier, &QSocketNotifier::activated, this, &VirtualSerialManager::onFdReadyRead);
    m_readNotifier->setEnabled(true);

    resetStats();
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
        m_rxBytes += n;
        emit statsChanged();

        QString text = decodeData(data);
        emit dataReceived(text, data);
    }
}
#endif // !Q_OS_WIN
