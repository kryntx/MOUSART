#ifndef CONFIGMANAGER_H
#define CONFIGMANAGER_H

#include <QObject>
#include <QSettings>
#include <QVariantList>
#include <QVariantMap>

class ConfigManager : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QVariantList quickCommands READ quickCommands NOTIFY quickCommandsChanged)
    Q_PROPERTY(QVariantList autoReplyRules READ autoReplyRules NOTIFY autoReplyRulesChanged)
    Q_PROPERTY(QVariantList sendSequences READ sendSequences NOTIFY sendSequencesChanged)
    Q_PROPERTY(QString currentProfile READ currentProfile WRITE setCurrentProfile NOTIFY currentProfileChanged)
    Q_PROPERTY(QStringList profiles READ profiles NOTIFY profilesChanged)

public:
    explicit ConfigManager(QObject *parent = nullptr);

    QVariantList quickCommands() const { return m_quickCommands; }
    QVariantList autoReplyRules() const { return m_autoReplyRules; }
    QVariantList sendSequences() const { return m_sendSequences; }
    QString currentProfile() const { return m_currentProfile; }
    void setCurrentProfile(const QString &profile);
    QStringList profiles() const;

    // Quick commands
    Q_INVOKABLE void addQuickCommand(const QString &name, const QString &data, bool hexMode);
    Q_INVOKABLE void removeQuickCommand(int index);
    Q_INVOKABLE void updateQuickCommand(int index, const QString &name, const QString &data, bool hexMode);
    Q_INVOKABLE void moveQuickCommand(int from, int to);

    // Auto-reply rules
    Q_INVOKABLE void addAutoReplyRule(const QString &name, const QString &match, const QString &response, int delay, bool enabled, bool useRegex);
    Q_INVOKABLE void removeAutoReplyRule(int index);
    Q_INVOKABLE void updateAutoReplyRule(int index, const QString &name, const QString &match, const QString &response, int delay, bool enabled, bool useRegex);
    Q_INVOKABLE void toggleAutoReplyRule(int index, bool enabled);

    // Send sequences
    Q_INVOKABLE void addSendSequence(const QString &name, const QVariantList &steps);
    Q_INVOKABLE void removeSendSequence(int index);
    Q_INVOKABLE void updateSendSequence(int index, const QString &name, const QVariantList &steps);

    // Profiles
    Q_INVOKABLE void saveProfile(const QString &name);
    Q_INVOKABLE void loadProfile(const QString &name);
    Q_INVOKABLE void deleteProfile(const QString &name);

    // Serial config persistence
    Q_INVOKABLE void saveSerialConfig(const QVariantMap &config);
    Q_INVOKABLE QVariantMap loadSerialConfig();

signals:
    void quickCommandsChanged();
    void autoReplyRulesChanged();
    void sendSequencesChanged();
    void currentProfileChanged();
    void profilesChanged();

private:
    void loadDefaults();
    void saveQuickCommands();
    void loadQuickCommands();
    void saveAutoReplyRules();
    void loadAutoReplyRules();
    void saveSendSequences();
    void loadSendSequences();

    QSettings m_settings;
    QString m_currentProfile = "default";
    QVariantList m_quickCommands;
    QVariantList m_autoReplyRules;
    QVariantList m_sendSequences;
};

#endif // CONFIGMANAGER_H
