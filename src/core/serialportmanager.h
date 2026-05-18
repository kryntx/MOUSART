#ifndef SERIALPORTMANAGER_H
#define SERIALPORTMANAGER_H

#include <QObject>
#include <QSerialPort>
#include <QSerialPortInfo>
#include <QTimer>

class SerialPortManager : public QObject
{
    Q_OBJECT
    Q_PROPERTY(bool isOpen READ isOpen NOTIFY isOpenChanged)
    Q_PROPERTY(QString currentPort READ currentPort NOTIFY currentPortChanged)
    Q_PROPERTY(QStringList portList READ portList NOTIFY portListChanged)
    Q_PROPERTY(bool filterSystemTty READ filterSystemTty WRITE setFilterSystemTty NOTIFY filterSystemTtyChanged)
    Q_PROPERTY(bool timedSendActive READ timedSendActive NOTIFY timedSendActiveChanged)

public:
    explicit SerialPortManager(QObject *parent = nullptr);
    ~SerialPortManager();

    bool isOpen() const { return m_port.isOpen(); }
    QString currentPort() const { return m_port.portName(); }
    QStringList portList() const { return m_ports; }
    bool filterSystemTty() const { return m_filterSystemTty; }
    void setFilterSystemTty(bool filter);
    bool timedSendActive() const { return m_timedSendTimer.isActive(); }

    Q_INVOKABLE void refreshPorts();
    Q_INVOKABLE bool openPort(const QString &name, int baudRate, int dataBits,
                               int stopBits, int parity, int flowControl);
    Q_INVOKABLE void closePort();
    Q_INVOKABLE qint64 sendData(const QString &data, bool hexMode);
    Q_INVOKABLE QString getErrorString() const;
    Q_INVOKABLE void startTimedSend(const QString &data, bool hexMode, int intervalMs);
    Q_INVOKABLE void stopTimedSend();

signals:
    void isOpenChanged();
    void currentPortChanged();
    void portListChanged();
    void dataReceived(const QString &data, const QByteArray &rawData);
    void errorOccurred(const QString &error);
    void portOpened(const QString &portName);
    void portClosed();
    void filterSystemTtyChanged();
    void timedSendActiveChanged();
    void timedSendCompleted(const QString &data);

private slots:
    void onReadyRead();
    void onTimedSendTick();

private:
    QSerialPort m_port;
    QStringList m_ports;
    QTimer m_refreshTimer;
    bool m_filterSystemTty = true;
    QTimer m_timedSendTimer;
    QString m_timedSendData;
    bool m_timedSendHexMode = false;
};

#endif // SERIALPORTMANAGER_H
