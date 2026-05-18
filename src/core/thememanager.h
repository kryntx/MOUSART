#ifndef THEMEMANAGER_H
#define THEMEMANAGER_H

#include <QObject>
#include <QColor>
#include <QSettings>

class ThemeManager : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QString theme READ theme WRITE setTheme NOTIFY themeChanged)
    Q_PROPERTY(qreal fontScale READ fontScale WRITE setFontScale NOTIFY fontScaleChanged)
    Q_PROPERTY(QColor bgPrimary READ bgPrimary NOTIFY colorsChanged)
    Q_PROPERTY(QColor bgSecondary READ bgSecondary NOTIFY colorsChanged)
    Q_PROPERTY(QColor bgTertiary READ bgTertiary NOTIFY colorsChanged)
    Q_PROPERTY(QColor textPrimary READ textPrimary NOTIFY colorsChanged)
    Q_PROPERTY(QColor textSecondary READ textSecondary NOTIFY colorsChanged)
    Q_PROPERTY(QColor accent READ accent NOTIFY colorsChanged)
    Q_PROPERTY(QColor border READ border NOTIFY colorsChanged)
    Q_PROPERTY(QColor receiveBg READ receiveBg NOTIFY colorsChanged)
    Q_PROPERTY(QColor sendBg READ sendBg NOTIFY colorsChanged)
    Q_PROPERTY(QColor titleBar READ titleBar NOTIFY colorsChanged)

public:
    explicit ThemeManager(QObject *parent = nullptr);

    QString theme() const { return m_theme; }
    void setTheme(const QString &theme);

    qreal fontScale() const { return m_fontScale; }
    void setFontScale(qreal scale);

    QColor bgPrimary() const;
    QColor bgSecondary() const;
    QColor bgTertiary() const;
    QColor textPrimary() const;
    QColor textSecondary() const;
    QColor accent() const;
    QColor border() const;
    QColor receiveBg() const;
    QColor sendBg() const;
    QColor titleBar() const;

signals:
    void themeChanged();
    void fontScaleChanged();
    void colorsChanged();

private:
    void loadSettings();
    void saveSettings();

    QString m_theme = "dark";
    qreal m_fontScale = 1.0;
    QSettings m_settings;
};

#endif // THEMEMANAGER_H
