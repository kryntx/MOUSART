#ifndef VIRTUALSERIALMANAGER_H
#define VIRTUALSERIALMANAGER_H

#include <QObject>
#include <QProcess>
#include <QSocketNotifier>

class VirtualSerialManager : public QObject
{
    Q_OBJECT
    Q_PROPERTY(bool isActive READ isActive NOTIFY isActiveChanged)
    Q_PROPERTY(QString externalPort READ externalPort NOTIFY externalPortChanged)

public:
    explicit VirtualSerialManager(QObject *parent = nullptr);
    ~VirtualSerialManager();

    bool isActive() const { return m_fd >= 0; }
    QString externalPort() const { return "/tmp/mousart_vport"; }

    Q_INVOKABLE bool startVirtualPort();
    Q_INVOKABLE void stopVirtualPort();
    Q_INVOKABLE qint64 sendData(const QString &data, bool hexMode);

signals:
    void isActiveChanged();
    void externalPortChanged();
    void dataReceived(const QString &data, const QByteArray &rawData);
    void errorOccurred(const QString &error);

private slots:
    void onSocatOutput();
    void onSocatFinished(int exitCode, QProcess::ExitStatus status);
    void onFdReadyRead(int fd);

private:
    void openSideA();

    QProcess m_socat;
    int m_fd = -1;
    QSocketNotifier *m_readNotifier = nullptr;
    QString m_ptyA;
    QString m_ptyB;
    bool m_waitingForPorts = false;
};

#endif // VIRTUALSERIALMANAGER_H
