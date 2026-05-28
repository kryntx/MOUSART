#ifndef LOGFILEMANAGER_H
#define LOGFILEMANAGER_H

#include <QObject>
#include <QVariantList>

class LogFileManager : public QObject
{
    Q_OBJECT
    Q_PROPERTY(bool isRecording READ isRecording NOTIFY isRecordingChanged)
    Q_PROPERTY(QString currentLogFile READ currentLogFile NOTIFY currentLogFileChanged)
    Q_PROPERTY(qint64 recordedBytes READ recordedBytes NOTIFY recordedBytesChanged)

public:
    explicit LogFileManager(QObject *parent = nullptr);

    bool isRecording() const { return m_isRecording; }
    QString currentLogFile() const { return m_currentLogFile; }
    qint64 recordedBytes() const { return m_recordedBytes; }

    // Save log data to file
    Q_INVOKABLE bool saveLogToFile(const QString &filePath, const QVariantList &logEntries, bool append = false);
    Q_INVOKABLE bool saveRawToFile(const QString &filePath, const QByteArray &data, bool append = false);

    // Export formats
    Q_INVOKABLE bool exportToCsv(const QString &filePath, const QVariantList &logEntries);
    Q_INVOKABLE bool exportToTxt(const QString &filePath, const QVariantList &logEntries);

    // Auto-record control
    Q_INVOKABLE void startRecording(const QString &directory = "");
    Q_INVOKABLE void stopRecording();
    Q_INVOKABLE void recordData(const QString &direction, const QByteArray &rawData, const QString &displayText = "");

    // Get save file path from user via native dialog
    Q_INVOKABLE QString getSaveFilePath(const QString &defaultName, const QString &filter);
    Q_INVOKABLE QString getOpenFilePath(const QString &title, const QString &filter);
    Q_INVOKABLE bool saveLogToFileWithDialog(const QVariantList &logEntries);
    Q_INVOKABLE QString getSaveLogPath();
    Q_INVOKABLE QString getSendFilePath();

signals:
    void isRecordingChanged();
    void currentLogFileChanged();
    void recordedBytesChanged();
    void errorOccurred(const QString &error);

private:
    bool m_isRecording = false;
    QString m_currentLogFile;
    QString m_recordDirectory;
    qint64 m_recordedBytes = 0;
    int m_fileIndex = 0;
    qint64 m_maxFileSize = 10 * 1024 * 1024; // 10MB per file
};

#endif // LOGFILEMANAGER_H
