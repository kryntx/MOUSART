import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Layouts 1.15
import "components"

Rectangle {
    id: titleBar
    color: themeManager.titleBar

    // Bottom border line
    Rectangle {
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        height: 1
        color: themeManager.border
    }

    RowLayout {
        anchors.fill: parent
        anchors.leftMargin: 12
        anchors.rightMargin: 4
        spacing: 8

        // App icon - drawn with Canvas
        Canvas {
            id: appIcon
            width: 20 * rootWindow.scaleFactor
            height: 20 * rootWindow.scaleFactor
            Layout.alignment: Qt.AlignVCenter

            onPaint: {
                var ctx = getContext("2d")
                ctx.clearRect(0, 0, width, height)
                ctx.strokeStyle = themeManager.accent
                ctx.lineWidth = 2
                ctx.lineCap = "round"

                var cx = width / 2
                var cy = height / 2
                ctx.beginPath()
                ctx.moveTo(2, cy)
                ctx.bezierCurveTo(cx * 0.5, cy - 6, cx, cy + 6, width - 2, cy)
                ctx.stroke()

                ctx.beginPath()
                ctx.arc(cx, cy, 2, 0, Math.PI * 2)
                ctx.fillStyle = themeManager.accent
                ctx.fill()
            }
        }

        Text {
            text: "MOUSART"
            color: themeManager.textPrimary
            font.pixelSize: 13 * rootWindow.scaleFactor
            font.bold: true
            font.family: "Segoe UI, sans-serif"
            Layout.alignment: Qt.AlignVCenter
        }

        Item { Layout.fillWidth: true }

        // Font scale control
        Text {
            text: "A"
            color: themeManager.textSecondary
            font.pixelSize: 10 * rootWindow.scaleFactor
            Layout.alignment: Qt.AlignVCenter
        }

        Rectangle {
            width: 80 * rootWindow.scaleFactor
            height: 4
            radius: 2
            color: themeManager.bgTertiary
            Layout.alignment: Qt.AlignVCenter

            Rectangle {
                width: parent.width * ((themeManager.fontScale - 0.8) / 0.7)
                height: parent.height
                radius: 2
                color: themeManager.accent
            }

            MouseArea {
                anchors.fill: parent
                anchors.margins: -6
                onClicked: {
                    var ratio = mouseX / parent.width
                    themeManager.fontScale = 0.8 + ratio * 0.7
                }
            }
        }

        Text {
            text: "A"
            color: themeManager.textSecondary
            font.pixelSize: 18 * rootWindow.scaleFactor
            Layout.alignment: Qt.AlignVCenter
        }

        // Theme toggle button
        Rectangle {
            width: 30 * rootWindow.scaleFactor
            height: 24 * rootWindow.scaleFactor
            radius: 4
            color: themeToggleArea.containsMouse ? themeManager.bgTertiary : "transparent"
            Layout.alignment: Qt.AlignVCenter

            Canvas {
                id: themeIcon
                anchors.centerIn: parent
                width: 16 * rootWindow.scaleFactor
                height: 16 * rootWindow.scaleFactor

                onPaint: {
                    var ctx = getContext("2d")
                    ctx.clearRect(0, 0, width, height)
                    var cx = width / 2
                    var cy = height / 2
                    var r = width * 0.35

                    if (themeManager.theme === "dark") {
                        ctx.fillStyle = themeManager.textPrimary
                        ctx.beginPath()
                        ctx.arc(cx, cy, r, -Math.PI * 0.5, Math.PI * 0.5)
                        ctx.arc(cx + r * 0.4, cy - r * 0.3, r * 0.7, Math.PI * 0.5, -Math.PI * 0.5, true)
                        ctx.fill()
                    } else {
                        ctx.strokeStyle = themeManager.textPrimary
                        ctx.lineWidth = 1.5
                        ctx.beginPath()
                        ctx.arc(cx, cy, r * 0.5, 0, Math.PI * 2)
                        ctx.stroke()

                        for (var i = 0; i < 8; i++) {
                            var angle = i * Math.PI / 4
                            ctx.beginPath()
                            ctx.moveTo(cx + Math.cos(angle) * r * 0.7, cy + Math.sin(angle) * r * 0.7)
                            ctx.lineTo(cx + Math.cos(angle) * r, cy + Math.sin(angle) * r)
                            ctx.stroke()
                        }
                    }
                }
            }

            Connections {
                target: themeManager
                function onColorsChanged() { themeIcon.requestPaint() }
            }

            MouseArea {
                id: themeToggleArea
                anchors.fill: parent
                hoverEnabled: true
                onClicked: {
                    themeManager.theme = themeManager.theme === "dark" ? "light" : "dark"
                }
            }
        }

        Item { width: 8 }

        // Minimize button
        WindowButton {
            id: minimizeBtn
            buttonType: "minimize"
            Layout.alignment: Qt.AlignVCenter
            onClicked: rootWindow.showMinimized()
        }

        // Maximize button
        WindowButton {
            id: maximizeBtn
            buttonType: rootWindow.isMaximized ? "restore" : "maximize"
            Layout.alignment: Qt.AlignVCenter
            onClicked: {
                if (rootWindow.isMaximized) {
                    rootWindow.showNormal()
                    rootWindow.isMaximized = false
                } else {
                    rootWindow.showMaximized()
                    rootWindow.isMaximized = true
                }
            }
        }

        // Close button
        WindowButton {
            id: closeBtn
            buttonType: "close"
            Layout.alignment: Qt.AlignVCenter
            onClicked: Qt.quit()
        }
    }

    // Drag to move window
    MouseArea {
        anchors.fill: parent
        z: -1
        onPressed: {
            if (rootWindow.visibility === Window.Maximized) {
                var ratio = mouseX / rootWindow.width
                rootWindow.showNormal()
                rootWindow.isMaximized = false
                rootWindow.x = mouseX - rootWindow.width * ratio
                rootWindow.y = mouseY - 20
            }
            rootWindow.startSystemMove()
        }
        onDoubleClicked: {
            if (rootWindow.isMaximized) {
                rootWindow.showNormal()
                rootWindow.isMaximized = false
            } else {
                rootWindow.showMaximized()
                rootWindow.isMaximized = true
            }
        }
    }
}
