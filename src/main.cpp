#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>
#include "core/thememanager.h"
#include "core/serialportmanager.h"
#include "core/virtualserialmanager.h"
#include "core/configmanager.h"
#include "core/dataanalyzer.h"
#include "core/logfilemanager.h"

int main(int argc, char *argv[])
{
    QCoreApplication::setAttribute(Qt::AA_EnableHighDpiScaling);
    QGuiApplication app(argc, argv);
    app.setApplicationName("MOUSART");
    app.setApplicationVersion("2.0.0");

    ThemeManager themeManager;
    SerialPortManager serialManager;
    VirtualSerialManager virtualManager;
    ConfigManager configManager;
    DataAnalyzer dataAnalyzer;
    LogFileManager logFileManager;

    QQmlApplicationEngine engine;
    engine.addImportPath("qrc:/qml");
    engine.rootContext()->setContextProperty("themeManager", &themeManager);
    engine.rootContext()->setContextProperty("serialManager", &serialManager);
    engine.rootContext()->setContextProperty("virtualManager", &virtualManager);
    engine.rootContext()->setContextProperty("configManager", &configManager);
    engine.rootContext()->setContextProperty("dataAnalyzer", &dataAnalyzer);
    engine.rootContext()->setContextProperty("logFileManager", &logFileManager);

    engine.load(QUrl(QStringLiteral("qrc:/qml/main.qml")));
    if (engine.rootObjects().isEmpty())
        return -1;

    return app.exec();
}
