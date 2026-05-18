import QtQuick 2.15

Rectangle {
    id: toggle
    property string label: ""
    property bool active: false
    signal clicked()

    implicitWidth: 34 * rootWindow.scaleFactor
    implicitHeight: 20 * rootWindow.scaleFactor
    radius: 10
    color: active ? themeManager.accent : themeManager.bgTertiary

    Text {
        anchors.centerIn: parent
        text: toggle.label
        color: toggle.active ? "#ffffff" : themeManager.textSecondary
        font.pixelSize: 8 * rootWindow.scaleFactor
        font.bold: true
    }

    MouseArea {
        anchors.fill: parent
        onClicked: toggle.clicked()
    }
}
