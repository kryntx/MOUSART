#include "serialportmanager.h"
#include <QDebug>
#include <QDir>
#include <QFileInfo>
#include <QFile>
#include <QTextStream>
#include <QDateTime>

SerialPortManager::SerialPortManager(QObject *parent)
    : QObject(parent)
{
    connect(&m_port, &QSerialPort::readyRead, this, &SerialPortManager::onReadyRead);
    connect(&m_port, &QSerialPort::errorOccurred, this, [this](QSerialPort::SerialPortError error) {
        if (error != QSerialPort::NoError && error != QSerialPort::TimeoutError) {
            emit errorOccurred(m_port.errorString());
        }
    });

    refreshPorts();
    connect(&m_refreshTimer, &QTimer::timeout, this, &SerialPortManager::refreshPorts);
    m_refreshTimer.start(2000);

    m_timedSendTimer.setTimerType(Qt::PreciseTimer);
    connect(&m_timedSendTimer, &QTimer::timeout, this, &SerialPortManager::onTimedSendTick);

    // Stats timer - update rates every second
    m_statsTimer.start();
    m_statsUpdateTimer.setInterval(1000);
    connect(&m_statsUpdateTimer, &QTimer::timeout, this, &SerialPortManager::onStatsTimer);
    m_statsUpdateTimer.start();

    // Auto-reply timer
    m_autoReplyTimer.setSingleShot(true);
    connect(&m_autoReplyTimer, &QTimer::timeout, this, [this]() {
        if (m_port.isOpen() && m_autoReplyEnabled) {
            QByteArray bytes;
            if (m_autoReplyResponse.startsWith("\\x")) {
                // Hex response
                QString hex = m_autoReplyResponse;
                hex.remove("\\x").remove(" ");
                bytes = QByteArray::fromHex(hex.toUtf8());
            } else {
                bytes = m_autoReplyResponse.toUtf8();
            }
            m_port.write(bytes);
            emit timedSendCompleted(m_autoReplyResponse);
        }
    });

    // Send sequence timer
    m_sendSeqTimer.setTimerType(Qt::PreciseTimer);
    connect(&m_sendSeqTimer, &QTimer::timeout, this, &SerialPortManager::onSendSequenceTick);
}

SerialPortManager::~SerialPortManager()
{
    if (m_port.isOpen()) m_port.close();
}

void SerialPortManager::refreshPorts()
{
    QStringList newPorts;
    const auto infos = QSerialPortInfo::availablePorts();
    for (const auto &info : infos) {
        QString name = info.portName();
        if (m_filterSystemTty) {
            if (name.startsWith("ttyS") || name.startsWith("ttyAMA") || name.startsWith("ttyO"))
                continue;
        }
        QString displayName = name;
        if (!info.description().isEmpty())
            displayName += " - " + info.description();
        newPorts.append(displayName);
    }

    static const char* VPORT_SYMLINK = "/tmp/mousart_vport";
    QFileInfo vlink(VPORT_SYMLINK);
    if (vlink.isSymLink()) {
        QString vpName = QString(VPORT_SYMLINK) + " [virtual]";
        if (!newPorts.contains(vpName))
            newPorts.append(vpName);
    }

    if (newPorts != m_ports) {
        m_ports = newPorts;
        emit portListChanged();
    }
}

void SerialPortManager::setFilterSystemTty(bool filter)
{
    if (m_filterSystemTty == filter) return;
    m_filterSystemTty = filter;
    emit filterSystemTtyChanged();
    refreshPorts();
}

bool SerialPortManager::openPort(const QString &name, int baudRate, int dataBits,
                                  int stopBits, int parity, int flowControl)
{
    if (m_port.isOpen()) closePort();

    QString portName = name;
    int dashIdx = portName.indexOf(" - ");
    if (dashIdx >= 0) portName = portName.left(dashIdx);
    portName = portName.remove(" [virtual]").trimmed();
    if (portName.startsWith("pts/"))
        portName = "/dev/" + portName;

    qWarning() << "[MOUSART] Opening port:" << portName;
    m_port.setPortName(portName);

    m_port.setBaudRate(static_cast<QSerialPort::BaudRate>(baudRate));
    m_port.setDataBits(static_cast<QSerialPort::DataBits>(dataBits));
    m_port.setStopBits(static_cast<QSerialPort::StopBits>(stopBits));
    m_port.setParity(static_cast<QSerialPort::Parity>(parity));
    m_port.setFlowControl(static_cast<QSerialPort::FlowControl>(flowControl));

    if (m_port.open(QIODevice::ReadWrite)) {
        resetStats();
        emit isOpenChanged();
        emit currentPortChanged();
        emit portOpened(portName);
        updatePinStates();
        return true;
    } else {
        emit errorOccurred(m_port.errorString());
        return false;
    }
}

void SerialPortManager::closePort()
{
    stopTimedSend();
    stopSendSequence();
    if (m_port.isOpen()) {
        m_port.close();
        emit isOpenChanged();
        emit currentPortChanged();
        emit portClosed();
    }
}

qint64 SerialPortManager::sendData(const QString &data, bool hexMode)
{
    if (!m_port.isOpen()) {
        emit errorOccurred(tr("Port not open"));
        return -1;
    }

    QByteArray bytes;
    if (hexMode) {
        QString hex = QString(data).remove(' ').remove('\n').remove('\r');
        bytes = QByteArray::fromHex(hex.toUtf8());
    } else {
        // Append newline if configured
        QString text = data;
        if (m_newlineCr) text += "\r";
        if (m_newlineLf) text += "\n";
        bytes = text.toUtf8();
    }

    qint64 written = m_port.write(bytes);
    if (written == -1) {
        emit errorOccurred(m_port.errorString());
    } else {
        m_txBytes += written;
        emit statsChanged();
    }
    return written;
}

qint64 SerialPortManager::sendRawBytes(const QByteArray &bytes)
{
    if (!m_port.isOpen()) {
        emit errorOccurred(tr("Port not open"));
        return -1;
    }
    qint64 written = m_port.write(bytes);
    if (written == -1) {
        emit errorOccurred(m_port.errorString());
    } else {
        m_txBytes += written;
        emit statsChanged();
    }
    return written;
}

QString SerialPortManager::sendFileData(const QString &filePath, bool hexMode)
{
    QFile file(filePath);
    if (!file.open(QIODevice::ReadOnly)) {
        return tr("无法打开文件: ") + file.errorString();
    }
    QByteArray data = file.readAll();
    file.close();

    if (data.isEmpty()) {
        return tr("文件为空");
    }

    qint64 written;
    if (hexMode) {
        // Treat file content as hex string
        QString hexStr = QString::fromUtf8(data).remove(' ').remove('\n').remove('\r');
        QByteArray bytes = QByteArray::fromHex(hexStr.toUtf8());
        written = sendRawBytes(bytes);
    } else {
        written = sendRawBytes(data);
    }

    if (written > 0) {
        return QString::number(written);
    }
    return tr("发送失败");
}

QString SerialPortManager::getErrorString() const
{
    return m_port.errorString();
}

// Timed send with count limit
void SerialPortManager::startTimedSend(const QString &data, bool hexMode, int intervalMs, int count)
{
    if (!m_port.isOpen()) {
        emit errorOccurred(tr("Port not open"));
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

void SerialPortManager::stopTimedSend()
{
    m_timedSendTimer.stop();
    m_timedSendSent = 0;
    m_timedSendCount = -1;
    emit timedSendActiveChanged();
}

void SerialPortManager::onTimedSendTick()
{
    if (!m_port.isOpen()) {
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

// Send sequence
void SerialPortManager::startSendSequence(const QStringList &dataList, const QList<int> &delays, bool hexMode, bool loop)
{
    if (!m_port.isOpen() || dataList.isEmpty()) return;
    stopSendSequence();
    m_sendSeqData = dataList;
    m_sendSeqDelays = delays;
    m_sendSeqHexMode = hexMode;
    m_sendSeqLoop = loop;
    m_sendSeqIndex = 0;
    onSendSequenceTick(); // Send first immediately
}

void SerialPortManager::stopSendSequence()
{
    m_sendSeqTimer.stop();
    m_sendSeqIndex = 0;
    emit sendSequenceActiveChanged();
}

void SerialPortManager::onSendSequenceTick()
{
    if (!m_port.isOpen() || m_sendSeqData.isEmpty()) {
        stopSendSequence();
        return;
    }

    if (m_sendSeqIndex >= m_sendSeqData.size()) {
        if (m_sendSeqLoop) {
            m_sendSeqIndex = 0;
        } else {
            stopSendSequence();
            emit sendSequenceCompleted();
            return;
        }
    }

    sendData(m_sendSeqData[m_sendSeqIndex], m_sendSeqHexMode);
    emit timedSendCompleted(m_sendSeqData[m_sendSeqIndex]);

    m_sendSeqIndex++;
    if (m_sendSeqIndex < m_sendSeqData.size()) {
        int delay = (m_sendSeqIndex - 1 < m_sendSeqDelays.size()) ? m_sendSeqDelays[m_sendSeqIndex - 1] : 100;
        m_sendSeqTimer.start(qMax(delay, 1));
    } else if (m_sendSeqLoop) {
        m_sendSeqTimer.start(100);
    } else {
        stopSendSequence();
        emit sendSequenceCompleted();
    }
}

void SerialPortManager::onReadyRead()
{
    QByteArray data = m_port.readAll();
    if (!data.isEmpty()) {
        m_rxBytes += data.size();
        emit statsChanged();

        QString text = decodeData(data);
        emit dataReceived(text, data);

        // Auto-reply check
        if (m_autoReplyEnabled && !m_autoReplyMatch.isEmpty()) {
            QString checkText = QString::fromUtf8(data);
            if (checkText.contains(m_autoReplyMatch, Qt::CaseInsensitive)) {
                if (m_autoReplyDelay > 0) {
                    m_autoReplyTimer.start(m_autoReplyDelay);
                } else {
                    // Immediate reply
                    QByteArray bytes;
                    if (m_autoReplyResponse.startsWith("\\x")) {
                        QString hex = m_autoReplyResponse;
                        hex.remove("\\x").remove(" ");
                        bytes = QByteArray::fromHex(hex.toUtf8());
                    } else {
                        bytes = m_autoReplyResponse.toUtf8();
                    }
                    m_port.write(bytes);
                    emit timedSendCompleted(m_autoReplyResponse);
                }
            }
        }

        // Auto-save
        if (m_autoSaveEnabled) {
            appendToFile(data);
        }
    }
}

// Pin control
bool SerialPortManager::dtr()
{
    if (!m_port.isOpen()) return false;
    return m_port.pinoutSignals() & QSerialPort::DataTerminalReadySignal;
}

void SerialPortManager::setDtr(bool state)
{
    if (m_port.isOpen()) {
        m_port.setDataTerminalReady(state);
        emit dtrChanged();
        emit pinStatesChanged();
    }
}

bool SerialPortManager::rts()
{
    if (!m_port.isOpen()) return false;
    return m_port.pinoutSignals() & QSerialPort::RequestToSendSignal;
}

void SerialPortManager::setRts(bool state)
{
    if (m_port.isOpen()) {
        m_port.setRequestToSend(state);
        emit rtsChanged();
        emit pinStatesChanged();
    }
}

bool SerialPortManager::cts()
{
    if (!m_port.isOpen()) return false;
    return m_port.pinoutSignals() & QSerialPort::ClearToSendSignal;
}

bool SerialPortManager::dsr()
{
    if (!m_port.isOpen()) return false;
    return m_port.pinoutSignals() & QSerialPort::DataSetReadySignal;
}

bool SerialPortManager::dcd()
{
    if (!m_port.isOpen()) return false;
    return m_port.pinoutSignals() & QSerialPort::DataCarrierDetectSignal;
}

bool SerialPortManager::ri()
{
    if (!m_port.isOpen()) return false;
    return m_port.pinoutSignals() & QSerialPort::RingIndicatorSignal;
}

void SerialPortManager::updatePinStates()
{
    emit pinStatesChanged();
}

// Stats
double SerialPortManager::rxRate() const
{
    qint64 elapsed = m_statsTimer.elapsed();
    if (elapsed < 100) return 0.0;
    return (double)(m_rxBytes - m_rxBytesSnapshot) * 1000.0 / elapsed;
}

double SerialPortManager::txRate() const
{
    qint64 elapsed = m_statsTimer.elapsed();
    if (elapsed < 100) return 0.0;
    return (double)(m_txBytes - m_txBytesSnapshot) * 1000.0 / elapsed;
}

void SerialPortManager::resetStats()
{
    m_rxBytes = 0;
    m_txBytes = 0;
    m_rxErrors = 0;
    m_rxBytesSnapshot = 0;
    m_txBytesSnapshot = 0;
    m_statsTimer.restart();
    emit statsChanged();
}

void SerialPortManager::onStatsTimer()
{
    m_rxBytesSnapshot = m_rxBytes;
    m_txBytesSnapshot = m_txBytes;
    m_statsTimer.restart();
    emit statsChanged();
}

// Auto-reply setters
void SerialPortManager::setAutoReplyEnabled(bool enabled)
{
    if (m_autoReplyEnabled == enabled) return;
    m_autoReplyEnabled = enabled;
    emit autoReplyConfigChanged();
}

void SerialPortManager::setAutoReplyMatch(const QString &match)
{
    if (m_autoReplyMatch == match) return;
    m_autoReplyMatch = match;
    emit autoReplyConfigChanged();
}

void SerialPortManager::setAutoReplyResponse(const QString &response)
{
    if (m_autoReplyResponse == response) return;
    m_autoReplyResponse = response;
    emit autoReplyConfigChanged();
}

void SerialPortManager::setAutoReplyDelay(int ms)
{
    if (m_autoReplyDelay == ms) return;
    m_autoReplyDelay = ms;
    emit autoReplyConfigChanged();
}

// Echo
void SerialPortManager::setEchoEnabled(bool enabled)
{
    if (m_echoEnabled == enabled) return;
    m_echoEnabled = enabled;
    emit echoEnabledChanged();
}

// Newline
void SerialPortManager::setNewlineCr(bool v)
{
    if (m_newlineCr == v) return;
    m_newlineCr = v;
    emit newlineChanged();
}

void SerialPortManager::setNewlineLf(bool v)
{
    if (m_newlineLf == v) return;
    m_newlineLf = v;
    emit newlineChanged();
}

// Encoding
void SerialPortManager::setReceiveEncoding(const QString &enc)
{
    if (m_receiveEncoding == enc) return;
    m_receiveEncoding = enc;
    emit receiveEncodingChanged();
}

QString SerialPortManager::decodeData(const QByteArray &data) const
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

// Auto-save
void SerialPortManager::setAutoSaveEnabled(bool enabled)
{
    if (m_autoSaveEnabled == enabled) return;
    m_autoSaveEnabled = enabled;
    emit autoSaveEnabledChanged();
}

void SerialPortManager::setAutoSavePath(const QString &path)
{
    if (m_autoSavePath == path) return;
    m_autoSavePath = path;
    emit autoSavePathChanged();
}

void SerialPortManager::appendToFile(const QByteArray &data)
{
    QString path = m_autoSavePath;
    if (path.isEmpty()) {
        path = QDir::homePath() + "/mousart_logs";
        QDir().mkpath(path);
        path += "/mousart_" + QDateTime::currentDateTime().toString("yyyyMMdd") + ".log";
    }
    QFile file(path);
    if (file.open(QIODevice::Append | QIODevice::Text)) {
        QTextStream ts(&file);
        ts << "[" << QDateTime::currentDateTime().toString("hh:mm:ss.zzz") << "] RX: ";
        ts << QString::fromUtf8(data) << "\n";
        file.close();
    }
}

void SerialPortManager::saveReceiveLog(const QString &filePath, bool append)
{
    // This is called from QML to save a log model to file
    // The actual data comes from QML side
    Q_UNUSED(filePath)
    Q_UNUSED(append)
}
