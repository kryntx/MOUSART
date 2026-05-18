#ifndef VIRTUALSERIALMANAGER_H
#define VIRTUALSERIALMANAGER_H

#include <QObject>
#include <QProcess>
#include <QSocketNotifier>
#include <QTimer>

class VirtualSerialManager : public QObject
{
    Q_OBJECT
    Q_PROPERTY(bool isActive READ isActive NOTIFY isActiveChanged)
    Q_PROPERTY(QString externalPort READ externalPort NOTIFY externalPortChanged)
    Q_PROPERTY(bool timedSendActive READ timedSendActive NOTIFY timedSendActiveChanged)

public:
    explicit VirtualSerialManager(QObject *parent = nullptr);
    ~VirtualSerialManager();

    bool isActive() const { return m_fd >= 0; }
    QString externalPort() const { return "/tmp/mousart_vport"; }
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
    void onSocatOutput();
    void onSocatFinished(int exitCode, QProcess::ExitStatus status);
    void onFdReadyRead(int fd);
    void onTimedSendTick();

private:
    void openSideA();

    QProcess m_socat;
    int m_fd = -1;
    QSocketNotifier *m_readNotifier = nullptr;
    QString m_ptyA;
    QString m_ptyB;
    bool m_waitingForPorts = false;
    QTimer m_timedSendTimer;
    QString m_timedSendData;
    bool m_timedSendHexMode = false;
};

#endif // VIRTUALSERIALMANAGER_H
