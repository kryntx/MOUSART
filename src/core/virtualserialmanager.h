#ifndef VIRTUALSERIALMANAGER_H
#define VIRTUALSERIALMANAGER_H

#include <QObject>
#include <QTimer>

#ifdef Q_OS_WIN
#include <QSerialPort>
#else
#include <QProcess>
#include <QSocketNotifier>
#endif

class VirtualSerialManager : public QObject
{
    Q_OBJECT
    Q_PROPERTY(bool isActive READ isActive NOTIFY isActiveChanged)
    Q_PROPERTY(QString externalPort READ externalPort NOTIFY externalPortChanged)
    Q_PROPERTY(bool timedSendActive READ timedSendActive NOTIFY timedSendActiveChanged)

public:
    explicit VirtualSerialManager(QObject *parent = nullptr);
    ~VirtualSerialManager();

    bool isActive() const
    {
#ifdef Q_OS_WIN
        return m_winPort && m_winPort->isOpen();
#else
        return m_fd >= 0;
#endif
    }
    QString externalPort() const
    {
#ifdef Q_OS_WIN
        return tr("虚拟串口在 Windows 上暂不可用");
#else
        return "/tmp/mousart_vport";
#endif
    }
    bool timedSendActive() const { return m_timedSendTimer.isActive(); }

    Q_INVOKABLE bool startVirtualPort();
    Q_INVOKABLE void stopVirtualPort();
    Q_INVOKABLE qint64 sendData(const QString &data, bool hexMode);
    Q_INVOKABLE void startTimedSend(const QString &data, bool hexMode, int intervalMs);
    Q_INVOKABLE void stopTimedSend();

signals:
    void isActiveChanged();
    void externalPortChanged();
    void dataReceived(const QString &data, const QByteArray &rawData);
    void errorOccurred(const QString &error);
    void timedSendActiveChanged();
    void timedSendCompleted(const QString &data);

private slots:
    void onTimedSendTick();
#ifndef Q_OS_WIN
    void onSocatOutput();
    void onSocatFinished(int exitCode, QProcess::ExitStatus status);
    void onFdReadyRead(int fd);
#endif

private:
#ifndef Q_OS_WIN
    void openSideA();

    QProcess m_socat;
    int m_fd = -1;
    QSocketNotifier *m_readNotifier = nullptr;
    QString m_ptyA;
    QString m_ptyB;
    bool m_waitingForPorts = false;
#else
    QSerialPort *m_winPort = nullptr;
#endif
    QTimer m_timedSendTimer;
    QString m_timedSendData;
    bool m_timedSendHexMode = false;
};

#endif // VIRTUALSERIALMANAGER_H
