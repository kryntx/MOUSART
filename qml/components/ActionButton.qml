import QtQuick 2.15

Rectangle {
    id: actionBtn
    property string label: ""
    property bool isActive: false
    signal clicked()

    radius: 8
    color: {
        if (isActive) {
            return actionBtnMouse.pressed ? Qt.darker("#e74c3c", 1.1) : (actionBtnMouse.containsMouse ? Qt.lighter("#e74c3c", 1.1) : "#e74c3c")
        }
        return actionBtnMouse.pressed ? Qt.darker(themeManager.accent, 1.1) : (actionBtnMouse.containsMouse ? Qt.lighter(themeManager.accent, 1.1) : themeManager.accent)
    }

    Text {
        anchors.centerIn: parent
        text: actionBtn.label
        color: "#ffffff"
        font.pixelSize: 13 * rootWindow.scaleFactor
        font.bold: true
    }

    MouseArea {
        id: actionBtnMouse
        anchors.fill: parent
        hoverEnabled: true
        onClicked: actionBtn.clicked()
    }

    Behavior on color { ColorAnimation { duration: 150 } }
}
