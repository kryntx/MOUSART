import QtQuick 2.15

Rectangle {
    id: btn
    property string label: ""
    property bool accent: false
    property bool btnEnabled: true
    signal clicked()

    implicitWidth: btnText.implicitWidth + 14 * rootWindow.scaleFactor
    implicitHeight: 20 * rootWindow.scaleFactor
    radius: 10
    color: {
        if (!btnEnabled) return themeManager.bgTertiary
        if (accent) {
            return btnMouse.pressed ? Qt.darker(themeManager.accent, 1.1) :
                   btnMouse.containsMouse ? Qt.lighter(themeManager.accent, 1.1) : themeManager.accent
        }
        return btnMouse.containsMouse ? themeManager.bgTertiary : "transparent"
    }
    border.color: (!accent && btnEnabled) ? themeManager.border : "transparent"
    border.width: 1

    Text {
        id: btnText
        anchors.centerIn: parent
        text: btn.label
        color: {
            if (!btn.btnEnabled) return themeManager.textSecondary
            return btn.accent ? "#ffffff" : themeManager.textPrimary
        }
        font.pixelSize: 9 * rootWindow.scaleFactor
        font.bold: btn.accent
    }

    MouseArea {
        id: btnMouse
        anchors.fill: parent
        hoverEnabled: true
        onClicked: if (btn.btnEnabled) btn.clicked()
    }
}
