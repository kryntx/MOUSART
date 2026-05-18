import QtQuick 2.15

Rectangle {
    id: modeBtn
    property string label: ""
    property string sublabel: ""
    property bool isActive: false
    signal clicked()

    implicitHeight: 48 * rootWindow.scaleFactor
    radius: 8
    color: isActive ? themeManager.accent : (modeBtnMouse.containsMouse ? themeManager.bgTertiary : themeManager.bgPrimary)
    border.color: isActive ? themeManager.accent : themeManager.border
    border.width: 1

    Column {
        anchors.centerIn: parent
        spacing: 2

        Text {
            anchors.horizontalCenter: parent.horizontalCenter
            text: modeBtn.label
            color: isActive ? "#ffffff" : themeManager.textPrimary
            font.pixelSize: 12 * rootWindow.scaleFactor
            font.bold: isActive
        }

        Text {
            anchors.horizontalCenter: parent.horizontalCenter
            text: modeBtn.sublabel
            color: isActive ? Qt.rgba(1, 1, 1, 0.7) : themeManager.textSecondary
            font.pixelSize: 9 * rootWindow.scaleFactor
        }
    }

    MouseArea {
        id: modeBtnMouse
        anchors.fill: parent
        hoverEnabled: true
        onClicked: modeBtn.clicked()
    }

    Behavior on color { ColorAnimation { duration: 150 } }
}
