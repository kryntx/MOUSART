#include "thememanager.h"

ThemeManager::ThemeManager(QObject *parent)
    : QObject(parent), m_settings("MOUSART", "MOUSART")
{
    loadSettings();
}

void ThemeManager::setTheme(const QString &theme)
{
    if (m_theme == theme) return;
    m_theme = theme;
    saveSettings();
    emit themeChanged();
    emit colorsChanged();
}

void ThemeManager::setFontScale(qreal scale)
{
    scale = qBound(0.8, scale, 1.5);
    if (qFuzzyCompare(m_fontScale, scale)) return;
    m_fontScale = scale;
    saveSettings();
    emit fontScaleChanged();
}

QColor ThemeManager::bgPrimary() const
{
    return m_theme == "dark" ? QColor("#1a1a2e") : QColor("#f0f0f5");
}

QColor ThemeManager::bgSecondary() const
{
    return m_theme == "dark" ? QColor("#16213e") : QColor("#ffffff");
}

QColor ThemeManager::bgTertiary() const
{
    return m_theme == "dark" ? QColor("#0f3460") : QColor("#e8e8ed");
}

QColor ThemeManager::textPrimary() const
{
    return m_theme == "dark" ? QColor("#e0e0e0") : QColor("#1a1a2e");
}

QColor ThemeManager::textSecondary() const
{
    return m_theme == "dark" ? QColor("#8899aa") : QColor("#666677");
}

QColor ThemeManager::accent() const
{
    return m_theme == "dark" ? QColor("#00d4aa") : QColor("#0088cc");
}

QColor ThemeManager::border() const
{
    return m_theme == "dark" ? QColor("#2a2a4a") : QColor("#ccccdd");
}

QColor ThemeManager::receiveBg() const
{
    return m_theme == "dark" ? QColor("#0d1117") : QColor("#fafafa");
}

QColor ThemeManager::sendBg() const
{
    return m_theme == "dark" ? QColor("#161b22") : QColor("#ffffff");
}

QColor ThemeManager::titleBar() const
{
    return m_theme == "dark" ? QColor("#1a1a2e") : QColor("#e8e8ed");
}

void ThemeManager::loadSettings()
{
    m_theme = m_settings.value("theme", "dark").toString();
    m_fontScale = m_settings.value("fontScale", 1.0).toReal();
}

void ThemeManager::saveSettings()
{
    m_settings.setValue("theme", m_theme);
    m_settings.setValue("fontScale", m_fontScale);
}
