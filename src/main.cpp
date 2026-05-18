#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>
#include "core/thememanager.h"
#include "core/serialportmanager.h"
#include "core/virtualserialmanager.h"

int main(int argc, char *argv[])
{
    QCoreApplication::setAttribute(Qt::AA_EnableHighDpiScaling);
    QGuiApplication app(argc, argv);
    app.setApplicationName("MOUSART");
    app.setApplicationVersion("1.0.0");

    ThemeManager themeManager;
    SerialPortManager serialManager;
    VirtualSerialManager virtualManager;

    // Register B-side virtual port in serial port list when virtual port starts
    QObject::connect(&virtualManager, &VirtualSerialManager::isActiveChanged, [&]() {
        if (virtualManager.isActive()) {
            serialManager.setExternalVirtualPort(virtualManager.externalPort());
        } else {
            serialManager.clearExternalVirtualPort();
        }
    });

    QQmlApplicationEngine engine;
    engine.addImportPath("qrc:/qml");
    engine.rootContext()->setContextProperty("themeManager", &themeManager);
    engine.rootContext()->setContextProperty("serialManager", &serialManager);
    engine.rootContext()->setContextProperty("virtualManager", &virtualManager);

    engine.load(QUrl(QStringLiteral("qrc:/qml/main.qml")));
    if (engine.rootObjects().isEmpty())
        return -1;

    return app.exec();
}
