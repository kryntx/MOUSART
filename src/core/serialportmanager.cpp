#include "serialportmanager.h"
#include <QDebug>
#include <QDir>
#include <QFileInfo>

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

    // Detect virtual port symlink created by any MOUSART instance
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

    // Extract port name: "ttyUSB0 - Description" -> ttyUSB0, "/dev/pts/3 [virtual]" -> /dev/pts/3
    QString portName = name;
    // Remove description suffix
    int dashIdx = portName.indexOf(" - ");
    if (dashIdx >= 0) portName = portName.left(dashIdx);
    // Remove [virtual] marker
    portName = portName.remove(" [virtual]").trimmed();
    // Ensure PTY paths are absolute
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
        emit isOpenChanged();
        emit currentPortChanged();
        emit portOpened(portName);
        return true;
    } else {
        emit errorOccurred(m_port.errorString());
        return false;
    }
}

void SerialPortManager::closePort()
{
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
        bytes = data.toUtf8();
    }

    qint64 written = m_port.write(bytes);
    if (written == -1) {
        emit errorOccurred(m_port.errorString());
    }
    return written;
}

QString SerialPortManager::getErrorString() const
{
    return m_port.errorString();
}

void SerialPortManager::onReadyRead()
{
    QByteArray data = m_port.readAll();
    if (!data.isEmpty()) {
        QString text = QString::fromUtf8(data);
        emit dataReceived(text, data);
    }
}
