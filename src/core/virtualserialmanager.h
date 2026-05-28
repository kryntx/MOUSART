#ifndef VIRTUALSERIALMANAGER_H
#define VIRTUALSERIALMANAGER_H

#include <QObject>
#include <QTimer>
#include <QElapsedTimer>
#include <QTextCodec>

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
    // New properties matching SerialPortManager
    Q_PROPERTY(qint64 rxBytes READ rxBytes NOTIFY statsChanged)
    Q_PROPERTY(qint64 txBytes READ txBytes NOTIFY statsChanged)
    Q_PROPERTY(double rxRate READ rxRate NOTIFY statsChanged)
    Q_PROPERTY(double txRate READ txRate NOTIFY statsChanged)
    Q_PROPERTY(bool echoEnabled READ echoEnabled WRITE setEchoEnabled NOTIFY echoEnabledChanged)
    Q_PROPERTY(bool newlineCr READ newlineCr WRITE setNewlineCr NOTIFY newlineChanged)
    Q_PROPERTY(bool newlineLf READ newlineLf WRITE setNewlineLf NOTIFY newlineChanged)
    Q_PROPERTY(QString receiveEncoding READ receiveEncoding WRITE setReceiveEncoding NOTIFY receiveEncodingChanged)

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

    // Stats
    qint64 rxBytes() const { return m_rxBytes; }
    qint64 txBytes() const { return m_txBytes; }
    double rxRate() const;
    double txRate() const;

    // Echo/Encoding/Newline
    bool echoEnabled() const { return m_echoEnabled; }
    void setEchoEnabled(bool enabled);
    bool newlineCr() const { return m_newlineCr; }
    void setNewlineCr(bool v);
    bool newlineLf() const { return m_newlineLf; }
    void setNewlineLf(bool v);
    QString receiveEncoding() const { return m_receiveEncoding; }
    void setReceiveEncoding(const QString &enc);

    Q_INVOKABLE bool startVirtualPort();
    Q_INVOKABLE void stopVirtualPort();
    Q_INVOKABLE qint64 sendData(const QString &data, bool hexMode);
    Q_INVOKABLE void startTimedSend(const QString &data, bool hexMode, int intervalMs, int count = -1);
    Q_INVOKABLE void stopTimedSend();
    Q_INVOKABLE void resetStats();

signals:
    void isActiveChanged();
    void externalPortChanged();
    void dataReceived(const QString &data, const QByteArray &rawData);
    void errorOccurred(const QString &error);
    void timedSendActiveChanged();
    void timedSendCompleted(const QString &data);
    void statsChanged();
    void echoEnabledChanged();
    void newlineChanged();
    void receiveEncodingChanged();

private slots:
    void onTimedSendTick();
#ifndef Q_OS_WIN
    void onSocatOutput();
    void onSocatFinished(int exitCode, QProcess::ExitStatus status);
    void onFdReadyRead(int fd);
#endif

private:
    QString decodeData(const QByteArray &data) const;

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
    int m_timedSendCount = -1;
    int m_timedSendSent = 0;

    // Stats
    qint64 m_rxBytes = 0;
    qint64 m_txBytes = 0;
    qint64 m_rxBytesSnapshot = 0;
    qint64 m_txBytesSnapshot = 0;
    QElapsedTimer m_statsTimer;
    QTimer m_statsUpdateTimer;

    // Settings
    bool m_echoEnabled = false;
    bool m_newlineCr = true;
    bool m_newlineLf = true;
    QString m_receiveEncoding = "UTF-8";
};

#endif // VIRTUALSERIALMANAGER_H
