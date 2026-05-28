#ifndef SERIALPORTMANAGER_H
#define SERIALPORTMANAGER_H

#include <QObject>
#include <QSerialPort>
#include <QSerialPortInfo>
#include <QTimer>
#include <QElapsedTimer>
#include <QTextCodec>

class SerialPortManager : public QObject
{
    Q_OBJECT
    Q_PROPERTY(bool isOpen READ isOpen NOTIFY isOpenChanged)
    Q_PROPERTY(QString currentPort READ currentPort NOTIFY currentPortChanged)
    Q_PROPERTY(QStringList portList READ portList NOTIFY portListChanged)
    Q_PROPERTY(bool filterSystemTty READ filterSystemTty WRITE setFilterSystemTty NOTIFY filterSystemTtyChanged)
    Q_PROPERTY(bool timedSendActive READ timedSendActive NOTIFY timedSendActiveChanged)
    // New properties
    Q_PROPERTY(bool dtr READ dtr WRITE setDtr NOTIFY dtrChanged)
    Q_PROPERTY(bool rts READ rts WRITE setRts NOTIFY rtsChanged)
    Q_PROPERTY(bool cts READ cts NOTIFY pinStatesChanged)
    Q_PROPERTY(bool dsr READ dsr NOTIFY pinStatesChanged)
    Q_PROPERTY(bool dcd READ dcd NOTIFY pinStatesChanged)
    Q_PROPERTY(bool ri READ ri NOTIFY pinStatesChanged)
    Q_PROPERTY(qint64 rxBytes READ rxBytes NOTIFY statsChanged)
    Q_PROPERTY(qint64 txBytes READ txBytes NOTIFY statsChanged)
    Q_PROPERTY(double rxRate READ rxRate NOTIFY statsChanged)
    Q_PROPERTY(double txRate READ txRate NOTIFY statsChanged)
    Q_PROPERTY(int rxErrors READ rxErrors NOTIFY statsChanged)
    Q_PROPERTY(bool autoReplyEnabled READ autoReplyEnabled WRITE setAutoReplyEnabled NOTIFY autoReplyConfigChanged)
    Q_PROPERTY(QString autoReplyMatch READ autoReplyMatch WRITE setAutoReplyMatch NOTIFY autoReplyConfigChanged)
    Q_PROPERTY(QString autoReplyResponse READ autoReplyResponse WRITE setAutoReplyResponse NOTIFY autoReplyConfigChanged)
    Q_PROPERTY(int autoReplyDelay READ autoReplyDelay WRITE setAutoReplyDelay NOTIFY autoReplyConfigChanged)
    Q_PROPERTY(bool echoEnabled READ echoEnabled WRITE setEchoEnabled NOTIFY echoEnabledChanged)
    Q_PROPERTY(bool newlineCr READ newlineCr WRITE setNewlineCr NOTIFY newlineChanged)
    Q_PROPERTY(bool newlineLf READ newlineLf WRITE setNewlineLf NOTIFY newlineChanged)
    Q_PROPERTY(QString receiveEncoding READ receiveEncoding WRITE setReceiveEncoding NOTIFY receiveEncodingChanged)
    Q_PROPERTY(bool autoSaveEnabled READ autoSaveEnabled WRITE setAutoSaveEnabled NOTIFY autoSaveEnabledChanged)
    Q_PROPERTY(QString autoSavePath READ autoSavePath WRITE setAutoSavePath NOTIFY autoSavePathChanged)

public:
    explicit SerialPortManager(QObject *parent = nullptr);
    ~SerialPortManager();

    // Existing
    bool isOpen() const { return m_port.isOpen(); }
    QString currentPort() const { return m_port.portName(); }
    QStringList portList() const { return m_ports; }
    bool filterSystemTty() const { return m_filterSystemTty; }
    void setFilterSystemTty(bool filter);
    bool timedSendActive() const { return m_timedSendTimer.isActive(); }

    // Pin control
    bool dtr();
    void setDtr(bool state);
    bool rts();
    void setRts(bool state);
    bool cts();
    bool dsr();
    bool dcd();
    bool ri();

    // Stats
    qint64 rxBytes() const { return m_rxBytes; }
    qint64 txBytes() const { return m_txBytes; }
    double rxRate() const;
    double txRate() const;
    int rxErrors() const { return m_rxErrors; }

    // Auto-reply
    bool autoReplyEnabled() const { return m_autoReplyEnabled; }
    void setAutoReplyEnabled(bool enabled);
    QString autoReplyMatch() const { return m_autoReplyMatch; }
    void setAutoReplyMatch(const QString &match);
    QString autoReplyResponse() const { return m_autoReplyResponse; }
    void setAutoReplyResponse(const QString &response);
    int autoReplyDelay() const { return m_autoReplyDelay; }
    void setAutoReplyDelay(int ms);

    // Echo
    bool echoEnabled() const { return m_echoEnabled; }
    void setEchoEnabled(bool enabled);

    // Newline
    bool newlineCr() const { return m_newlineCr; }
    void setNewlineCr(bool v);
    bool newlineLf() const { return m_newlineLf; }
    void setNewlineLf(bool v);

    // Encoding
    QString receiveEncoding() const { return m_receiveEncoding; }
    void setReceiveEncoding(const QString &enc);

    // Auto-save
    bool autoSaveEnabled() const { return m_autoSaveEnabled; }
    void setAutoSaveEnabled(bool enabled);
    QString autoSavePath() const { return m_autoSavePath; }
    void setAutoSavePath(const QString &path);

    Q_INVOKABLE void refreshPorts();
    Q_INVOKABLE bool openPort(const QString &name, int baudRate, int dataBits,
                               int stopBits, int parity, int flowControl);
    Q_INVOKABLE void closePort();
    Q_INVOKABLE qint64 sendData(const QString &data, bool hexMode);
    Q_INVOKABLE QString getErrorString() const;
    Q_INVOKABLE void startTimedSend(const QString &data, bool hexMode, int intervalMs, int count = -1);
    Q_INVOKABLE void stopTimedSend();
    Q_INVOKABLE void resetStats();
    Q_INVOKABLE void saveReceiveLog(const QString &filePath, bool append = true);
    Q_INVOKABLE void updatePinStates();
    Q_INVOKABLE QString sendFileData(const QString &filePath, bool hexMode);
    Q_INVOKABLE qint64 sendRawBytes(const QByteArray &bytes);
    Q_INVOKABLE void startSendSequence(const QStringList &dataList, const QList<int> &delays, bool hexMode, bool loop);
    Q_INVOKABLE void stopSendSequence();
    Q_INVOKABLE bool sendSequenceActive() const { return m_sendSeqTimer.isActive(); }

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
    void dtrChanged();
    void rtsChanged();
    void pinStatesChanged();
    void statsChanged();
    void autoReplyConfigChanged();
    void echoEnabledChanged();
    void newlineChanged();
    void receiveEncodingChanged();
    void autoSaveEnabledChanged();
    void autoSavePathChanged();
    void sendSequenceActiveChanged();
    void sendSequenceCompleted();

private slots:
    void onReadyRead();
    void onTimedSendTick();
    void onStatsTimer();
    void onSendSequenceTick();

private:
    void appendToFile(const QByteArray &data);
    QString decodeData(const QByteArray &data) const;

    QSerialPort m_port;
    QStringList m_ports;
    QTimer m_refreshTimer;
    bool m_filterSystemTty = true;

    // Timed send
    QTimer m_timedSendTimer;
    QString m_timedSendData;
    bool m_timedSendHexMode = false;
    int m_timedSendCount = -1;  // -1 = infinite
    int m_timedSendSent = 0;

    // Stats
    qint64 m_rxBytes = 0;
    qint64 m_txBytes = 0;
    int m_rxErrors = 0;
    qint64 m_rxBytesSnapshot = 0;
    qint64 m_txBytesSnapshot = 0;
    QElapsedTimer m_statsTimer;
    QTimer m_statsUpdateTimer;

    // Auto-reply
    bool m_autoReplyEnabled = false;
    QString m_autoReplyMatch;
    QString m_autoReplyResponse;
    int m_autoReplyDelay = 0;
    QTimer m_autoReplyTimer;
    QByteArray m_autoReplyPendingData;

    // Echo
    bool m_echoEnabled = false;

    // Newline
    bool m_newlineCr = true;
    bool m_newlineLf = true;

    // Encoding
    QString m_receiveEncoding = "UTF-8";

    // Auto-save
    bool m_autoSaveEnabled = false;
    QString m_autoSavePath;

    // Send sequence
    QTimer m_sendSeqTimer;
    QStringList m_sendSeqData;
    QList<int> m_sendSeqDelays;
    bool m_sendSeqHexMode = false;
    bool m_sendSeqLoop = false;
    int m_sendSeqIndex = 0;
};

#endif // SERIALPORTMANAGER_H
