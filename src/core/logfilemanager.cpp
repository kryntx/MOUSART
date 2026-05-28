#include "logfilemanager.h"
#include <QFile>
#include <QTextStream>
#include <QDateTime>
#include <QDir>
#include <QFileDialog>
#include <QCoreApplication>

LogFileManager::LogFileManager(QObject *parent)
    : QObject(parent)
{
}

bool LogFileManager::saveLogToFile(const QString &filePath, const QVariantList &logEntries, bool append)
{
    QFile file(filePath);
    QIODevice::OpenMode mode = QIODevice::WriteOnly | QIODevice::Text;
    if (append) mode |= QIODevice::Append;

    if (!file.open(mode)) {
        emit errorOccurred(tr("无法保存文件: ") + file.errorString());
        return false;
    }

    QTextStream ts(&file);
    ts.setCodec("UTF-8");

    if (!append) {
        ts << "MOUSART Log Export - " << QDateTime::currentDateTime().toString("yyyy-MM-dd hh:mm:ss") << "\n";
        ts << QString("=").repeated(80) << "\n\n";
    }

    for (const auto &entry : logEntries) {
        QVariantMap map = entry.toMap();
        QString time = map.value("logTime").toString();
        QString type = map.value("logType").toString();
        QString data = map.value("logData").toString();

        ts << "[" << time << "] ";

        if (type == "RX") ts << "<< RX: ";
        else if (type == "TX") ts << ">> TX: ";
        else if (type == "ERR") ts << "!! ERR: ";
        else if (type == "INFO") ts << "i  INFO: ";
        else if (type == "SYS") ts << "#  SYS: ";
        else ts << "   ";

        ts << data << "\n";
    }

    file.close();
    return true;
}

bool LogFileManager::saveRawToFile(const QString &filePath, const QByteArray &data, bool append)
{
    QFile file(filePath);
    QIODevice::OpenMode mode = QIODevice::WriteOnly;
    if (append) mode |= QIODevice::Append;

    if (!file.open(mode)) {
        emit errorOccurred(tr("无法保存文件: ") + file.errorString());
        return false;
    }

    file.write(data);
    file.close();
    return true;
}

bool LogFileManager::exportToCsv(const QString &filePath, const QVariantList &logEntries)
{
    QFile file(filePath);
    if (!file.open(QIODevice::WriteOnly | QIODevice::Text)) {
        emit errorOccurred(tr("无法保存文件: ") + file.errorString());
        return false;
    }

    QTextStream ts(&file);
    ts.setCodec("UTF-8");
    ts << "Time,Type,Direction,Data\n";

    for (const auto &entry : logEntries) {
        QVariantMap map = entry.toMap();
        QString time = map.value("logTime").toString();
        QString type = map.value("logType").toString();
        QString data = map.value("logData").toString();

        // Escape CSV
        data.replace("\"", "\"\"");

        QString direction;
        if (type == "RX") direction = "RX";
        else if (type == "TX") direction = "TX";
        else direction = "SYSTEM";

        ts << "\"" << time << "\",\"" << type << "\",\"" << direction << "\",\"" << data << "\"\n";
    }

    file.close();
    return true;
}

bool LogFileManager::exportToTxt(const QString &filePath, const QVariantList &logEntries)
{
    return saveLogToFile(filePath, logEntries, false);
}

void LogFileManager::startRecording(const QString &directory)
{
    if (m_isRecording) stopRecording();

    m_recordDirectory = directory;
    if (m_recordDirectory.isEmpty()) {
        m_recordDirectory = QDir::homePath() + "/mousart_logs";
    }
    QDir().mkpath(m_recordDirectory);

    m_fileIndex = 0;
    m_recordedBytes = 0;
    m_isRecording = true;
    m_currentLogFile = m_recordDirectory + "/mousart_rec_" +
                       QDateTime::currentDateTime().toString("yyyyMMdd_hhmmss") + ".log";

    emit isRecordingChanged();
    emit currentLogFileChanged();
    emit recordedBytesChanged();
}

void LogFileManager::stopRecording()
{
    m_isRecording = false;
    m_currentLogFile.clear();
    emit isRecordingChanged();
    emit currentLogFileChanged();
}

void LogFileManager::recordData(const QString &direction, const QByteArray &rawData, const QString &displayText)
{
    if (!m_isRecording) return;

    // Check file size and rotate
    if (m_recordedBytes >= m_maxFileSize) {
        m_fileIndex++;
        m_recordedBytes = 0;
        m_currentLogFile = m_recordDirectory + "/mousart_rec_" +
                           QDateTime::currentDateTime().toString("yyyyMMdd_hhmmss") +
                           QString("_%1").arg(m_fileIndex) + ".log";
        emit currentLogFileChanged();
    }

    QFile file(m_currentLogFile);
    if (file.open(QIODevice::Append | QIODevice::Text)) {
        QTextStream ts(&file);
        ts.setCodec("UTF-8");
        ts << "[" << QDateTime::currentDateTime().toString("hh:mm:ss.zzz") << "] "
           << direction << ": "
           << (displayText.isEmpty() ? QString::fromUtf8(rawData) : displayText)
           << "\n";
        file.close();
        m_recordedBytes += rawData.size();
        emit recordedBytesChanged();
    }
}

QString LogFileManager::getSaveFilePath(const QString &defaultName, const QString &filter)
{
    return QFileDialog::getSaveFileName(nullptr, tr("保存文件"),
        QDir::homePath() + "/" + defaultName, filter);
}

QString LogFileManager::getOpenFilePath(const QString &title, const QString &filter)
{
    return QFileDialog::getOpenFileName(nullptr, title, QDir::homePath(), filter);
}

bool LogFileManager::saveLogToFileWithDialog(const QVariantList &logEntries)
{
    QString path = getSaveFilePath(
        "mousart_log_" + QDateTime::currentDateTime().toString("yyyyMMdd_hhmmss") + ".txt",
        tr("Text files (*.txt);;CSV files (*.csv);;All files (*)"));
    if (path.isEmpty()) return false;

    if (path.endsWith(".csv"))
        return exportToCsv(path, logEntries);
    return saveLogToFile(path, logEntries, false);
}

QString LogFileManager::getSaveLogPath()
{
    return getSaveFilePath(
        "mousart_log_" + QDateTime::currentDateTime().toString("yyyyMMdd_hhmmss") + ".txt",
        tr("Text files (*.txt);;CSV files (*.csv);;All files (*)"));
}

QString LogFileManager::getSendFilePath()
{
    return getOpenFilePath(tr("选择发送文件"), tr("All files (*)"));
}
