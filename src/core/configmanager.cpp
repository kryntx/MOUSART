#include "configmanager.h"
#include <QJsonDocument>
#include <QJsonArray>
#include <QJsonObject>
#include <QFile>
#include <QDir>

ConfigManager::ConfigManager(QObject *parent)
    : QObject(parent), m_settings("MOUSART", "MOUSART")
{
    loadQuickCommands();
    loadAutoReplyRules();
    loadSendSequences();
    m_currentProfile = m_settings.value("currentProfile", "default").toString();
}

void ConfigManager::setCurrentProfile(const QString &profile)
{
    if (m_currentProfile == profile) return;
    m_currentProfile = profile;
    m_settings.setValue("currentProfile", profile);
    emit currentProfileChanged();
}

QStringList ConfigManager::profiles() const
{
    QStringList result;
    result << "default";
    QString configDir = QDir::homePath() + "/.mousart/profiles";
    QDir dir(configDir);
    if (dir.exists()) {
        for (const QString &entry : dir.entryList(QStringList() << "*.json", QDir::Files)) {
            QString name = entry;
            name.chop(5); // remove .json
            if (name != "default" && !result.contains(name))
                result << name;
        }
    }
    return result;
}

// Quick Commands
void ConfigManager::addQuickCommand(const QString &name, const QString &data, bool hexMode)
{
    QVariantMap cmd;
    cmd["name"] = name;
    cmd["data"] = data;
    cmd["hex"] = hexMode;
    m_quickCommands.append(cmd);
    saveQuickCommands();
    emit quickCommandsChanged();
}

void ConfigManager::removeQuickCommand(int index)
{
    if (index < 0 || index >= m_quickCommands.size()) return;
    m_quickCommands.removeAt(index);
    saveQuickCommands();
    emit quickCommandsChanged();
}

void ConfigManager::updateQuickCommand(int index, const QString &name, const QString &data, bool hexMode)
{
    if (index < 0 || index >= m_quickCommands.size()) return;
    QVariantMap cmd;
    cmd["name"] = name;
    cmd["data"] = data;
    cmd["hex"] = hexMode;
    m_quickCommands[index] = cmd;
    saveQuickCommands();
    emit quickCommandsChanged();
}

void ConfigManager::moveQuickCommand(int from, int to)
{
    if (from < 0 || from >= m_quickCommands.size()) return;
    if (to < 0 || to >= m_quickCommands.size()) return;
    m_quickCommands.move(from, to);
    saveQuickCommands();
    emit quickCommandsChanged();
}

// Auto-reply Rules
void ConfigManager::addAutoReplyRule(const QString &name, const QString &match, const QString &response, int delay, bool enabled, bool useRegex)
{
    QVariantMap rule;
    rule["name"] = name;
    rule["match"] = match;
    rule["response"] = response;
    rule["delay"] = delay;
    rule["enabled"] = enabled;
    rule["regex"] = useRegex;
    m_autoReplyRules.append(rule);
    saveAutoReplyRules();
    emit autoReplyRulesChanged();
}

void ConfigManager::removeAutoReplyRule(int index)
{
    if (index < 0 || index >= m_autoReplyRules.size()) return;
    m_autoReplyRules.removeAt(index);
    saveAutoReplyRules();
    emit autoReplyRulesChanged();
}

void ConfigManager::updateAutoReplyRule(int index, const QString &name, const QString &match, const QString &response, int delay, bool enabled, bool useRegex)
{
    if (index < 0 || index >= m_autoReplyRules.size()) return;
    QVariantMap rule;
    rule["name"] = name;
    rule["match"] = match;
    rule["response"] = response;
    rule["delay"] = delay;
    rule["enabled"] = enabled;
    rule["regex"] = useRegex;
    m_autoReplyRules[index] = rule;
    saveAutoReplyRules();
    emit autoReplyRulesChanged();
}

void ConfigManager::toggleAutoReplyRule(int index, bool enabled)
{
    if (index < 0 || index >= m_autoReplyRules.size()) return;
    QVariantMap rule = m_autoReplyRules[index].toMap();
    rule["enabled"] = enabled;
    m_autoReplyRules[index] = rule;
    saveAutoReplyRules();
    emit autoReplyRulesChanged();
}

// Send Sequences
void ConfigManager::addSendSequence(const QString &name, const QVariantList &steps)
{
    QVariantMap seq;
    seq["name"] = name;
    seq["steps"] = steps;
    m_sendSequences.append(seq);
    saveSendSequences();
    emit sendSequencesChanged();
}

void ConfigManager::removeSendSequence(int index)
{
    if (index < 0 || index >= m_sendSequences.size()) return;
    m_sendSequences.removeAt(index);
    saveSendSequences();
    emit sendSequencesChanged();
}

void ConfigManager::updateSendSequence(int index, const QString &name, const QVariantList &steps)
{
    if (index < 0 || index >= m_sendSequences.size()) return;
    QVariantMap seq;
    seq["name"] = name;
    seq["steps"] = steps;
    m_sendSequences[index] = seq;
    saveSendSequences();
    emit sendSequencesChanged();
}

// Profiles
void ConfigManager::saveProfile(const QString &name)
{
    QString configDir = QDir::homePath() + "/.mousart/profiles";
    QDir().mkpath(configDir);
    QString filePath = configDir + "/" + name + ".json";

    QJsonObject profile;
    profile["serialConfig"] = QJsonObject::fromVariantMap(loadSerialConfig());

    QJsonArray cmds;
    for (const auto &cmd : m_quickCommands) {
        cmds.append(QJsonObject::fromVariantMap(cmd.toMap()));
    }
    profile["quickCommands"] = cmds;

    QJsonArray rules;
    for (const auto &rule : m_autoReplyRules) {
        rules.append(QJsonObject::fromVariantMap(rule.toMap()));
    }
    profile["autoReplyRules"] = rules;

    QJsonArray seqs;
    for (const auto &seq : m_sendSequences) {
        seqs.append(QJsonObject::fromVariantMap(seq.toMap()));
    }
    profile["sendSequences"] = seqs;

    QFile file(filePath);
    if (file.open(QIODevice::WriteOnly)) {
        file.write(QJsonDocument(profile).toJson());
        file.close();
    }
    emit profilesChanged();
}

void ConfigManager::loadProfile(const QString &name)
{
    QString configDir = QDir::homePath() + "/.mousart/profiles";
    QString filePath = configDir + "/" + name + ".json";
    QFile file(filePath);
    if (!file.open(QIODevice::ReadOnly)) return;

    QJsonDocument doc = QJsonDocument::fromJson(file.readAll());
    file.close();
    QJsonObject profile = doc.object();

    if (profile.contains("serialConfig")) {
        saveSerialConfig(profile["serialConfig"].toObject().toVariantMap());
    }

    if (profile.contains("quickCommands")) {
        m_quickCommands.clear();
        for (const auto &v : profile["quickCommands"].toArray()) {
            m_quickCommands.append(v.toObject().toVariantMap());
        }
        saveQuickCommands();
        emit quickCommandsChanged();
    }

    if (profile.contains("autoReplyRules")) {
        m_autoReplyRules.clear();
        for (const auto &v : profile["autoReplyRules"].toArray()) {
            m_autoReplyRules.append(v.toObject().toVariantMap());
        }
        saveAutoReplyRules();
        emit autoReplyRulesChanged();
    }

    if (profile.contains("sendSequences")) {
        m_sendSequences.clear();
        for (const auto &v : profile["sendSequences"].toArray()) {
            m_sendSequences.append(v.toObject().toVariantMap());
        }
        saveSendSequences();
        emit sendSequencesChanged();
    }

    setCurrentProfile(name);
}

void ConfigManager::deleteProfile(const QString &name)
{
    if (name == "default") return;
    QString configDir = QDir::homePath() + "/.mousart/profiles";
    QFile::remove(configDir + "/" + name + ".json");
    emit profilesChanged();
}

// Serial config persistence
void ConfigManager::saveSerialConfig(const QVariantMap &config)
{
    m_settings.beginGroup("SerialConfig");
    for (auto it = config.begin(); it != config.end(); ++it) {
        m_settings.setValue(it.key(), it.value());
    }
    m_settings.endGroup();
}

QVariantMap ConfigManager::loadSerialConfig()
{
    QVariantMap config;
    m_settings.beginGroup("SerialConfig");
    for (const QString &key : m_settings.childKeys()) {
        config[key] = m_settings.value(key);
    }
    m_settings.endGroup();
    return config;
}

// Private helpers
void ConfigManager::saveQuickCommands()
{
    QJsonArray arr;
    for (const auto &cmd : m_quickCommands) {
        arr.append(QJsonObject::fromVariantMap(cmd.toMap()));
    }
    m_settings.setValue("quickCommands", QJsonDocument(arr).toJson(QJsonDocument::Compact));
}

void ConfigManager::loadQuickCommands()
{
    QByteArray data = m_settings.value("quickCommands").toByteArray();
    if (data.isEmpty()) {
        // Add default commands
        addQuickCommand("AT", "AT\r\n", false);
        addQuickCommand("AT+RST", "AT+RST\r\n", false);
        addQuickCommand("Ping", "FF 01 02 03", true);
        return;
    }
    QJsonDocument doc = QJsonDocument::fromJson(data);
    for (const auto &v : doc.array()) {
        m_quickCommands.append(v.toObject().toVariantMap());
    }
}

void ConfigManager::saveAutoReplyRules()
{
    QJsonArray arr;
    for (const auto &rule : m_autoReplyRules) {
        arr.append(QJsonObject::fromVariantMap(rule.toMap()));
    }
    m_settings.setValue("autoReplyRules", QJsonDocument(arr).toJson(QJsonDocument::Compact));
}

void ConfigManager::loadAutoReplyRules()
{
    QByteArray data = m_settings.value("autoReplyRules").toByteArray();
    if (data.isEmpty()) return;
    QJsonDocument doc = QJsonDocument::fromJson(data);
    for (const auto &v : doc.array()) {
        m_autoReplyRules.append(v.toObject().toVariantMap());
    }
}

void ConfigManager::saveSendSequences()
{
    QJsonArray arr;
    for (const auto &seq : m_sendSequences) {
        arr.append(QJsonObject::fromVariantMap(seq.toMap()));
    }
    m_settings.setValue("sendSequences", QJsonDocument(arr).toJson(QJsonDocument::Compact));
}

void ConfigManager::loadSendSequences()
{
    QByteArray data = m_settings.value("sendSequences").toByteArray();
    if (data.isEmpty()) return;
    QJsonDocument doc = QJsonDocument::fromJson(data);
    for (const auto &v : doc.array()) {
        m_sendSequences.append(v.toObject().toVariantMap());
    }
}
