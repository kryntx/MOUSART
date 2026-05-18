import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Window {
    id: rootWindow
    width: 1000
    height: 700
    minimumWidth: 700
    minimumHeight: 500
    visible: true
    title: "MOUSART"
    color: "transparent"
    flags: Qt.FramelessWindowHint | Qt.Window

    property bool isMaximized: false
    property real scaleFactor: themeManager.fontScale

    Rectangle {
        id: windowFrame
        anchors.fill: parent
        anchors.margins: rootWindow.isMaximized ? 0 : 6
        radius: rootWindow.isMaximized ? 0 : 12
        color: themeManager.bgPrimary
        clip: true

        border.color: themeManager.border
        border.width: rootWindow.isMaximized ? 0 : 1

        ColumnLayout {
            anchors.fill: parent
            spacing: 0

            TitleBar {
                id: titleBar
                Layout.fillWidth: true
                Layout.preferredHeight: 40 * rootWindow.scaleFactor
            }

            RowLayout {
                Layout.fillWidth: true
                Layout.fillHeight: true
                spacing: 0

                SettingsPanel {
                    id: settingsPanel
                    Layout.fillHeight: true
                    Layout.preferredWidth: 280 * rootWindow.scaleFactor
                    Layout.minimumWidth: 220 * rootWindow.scaleFactor
                }

                Rectangle {
                    Layout.fillHeight: true
                    Layout.preferredWidth: 1
                    color: themeManager.border
                }

                DataPanel {
                    id: dataPanel
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                }
            }
        }
    }

    // Resize handles for edges
    MouseArea {
        id: resizeHandle
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        width: 16
        height: 16
        cursorShape: Qt.SizeFDiagCursor
        enabled: !rootWindow.isMaximized

        property real startX: 0
        property real startY: 0
        property real startW: 0
        property real startH: 0

        onPressed: {
            startX = mouseX
            startY = mouseY
            startW = rootWindow.width
            startH = rootWindow.height
        }
        onPositionChanged: {
            rootWindow.width = Math.max(rootWindow.minimumWidth, startW + (mouseX - startX))
            rootWindow.height = Math.max(rootWindow.minimumHeight, startH + (mouseY - startY))
        }
    }

    // Right edge resize
    MouseArea {
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.rightMargin: 0
        width: 4
        cursorShape: Qt.SizeHorCursor
        enabled: !rootWindow.isMaximized

        property real startX: 0
        property real startW: 0

        onPressed: { startX = mouseX; startW = rootWindow.width }
        onPositionChanged: {
            rootWindow.width = Math.max(rootWindow.minimumWidth, startW + (mouseX - startX))
        }
    }

    // Bottom edge resize
    MouseArea {
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        height: 4
        cursorShape: Qt.SizeVerCursor
        enabled: !rootWindow.isMaximized

        property real startY: 0
        property real startH: 0

        onPressed: { startY = mouseY; startH = rootWindow.height }
        onPositionChanged: {
            rootWindow.height = Math.max(rootWindow.minimumHeight, startH + (mouseY - startY))
        }
    }

    // Shadow effect
    Rectangle {
        id: shadowRect
        anchors.fill: parent
        anchors.margins: -2
        z: -1
        visible: !rootWindow.isMaximized
        color: "transparent"
        border.color: Qt.rgba(0, 0, 0, 0.15)
        border.width: 8
        radius: 16
    }
}
