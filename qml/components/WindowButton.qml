import QtQuick 2.15

Rectangle {
    id: winBtn
    property string buttonType: "minimize"
    signal clicked()

    width: 36 * rootWindow.scaleFactor
    height: 28 * rootWindow.scaleFactor
    color: {
        if (buttonType === "close") {
            return btnMouse.pressed ? "#e81123" : (btnMouse.containsMouse ? "#c42b1c" : "transparent")
        }
        return btnMouse.pressed ? themeManager.bgTertiary : (btnMouse.containsMouse ? themeManager.bgTertiary : "transparent")
    }
    radius: 4

    Canvas {
        id: btnCanvas
        anchors.centerIn: parent
        width: 12 * rootWindow.scaleFactor
        height: 12 * rootWindow.scaleFactor

        onPaint: {
            var ctx = getContext("2d")
            ctx.clearRect(0, 0, width, height)
            ctx.strokeStyle = (winBtn.buttonType === "close" && btnMouse.containsMouse)
                ? "#ffffff"
                : themeManager.textPrimary
            ctx.lineWidth = 1.5
            ctx.lineCap = "round"

            var w = width
            var h = height
            var m = 2

            if (winBtn.buttonType === "minimize") {
                ctx.beginPath()
                ctx.moveTo(m, h / 2)
                ctx.lineTo(w - m, h / 2)
                ctx.stroke()
            } else if (winBtn.buttonType === "maximize") {
                ctx.beginPath()
                ctx.rect(m, m, w - m * 2, h - m * 2)
                ctx.stroke()
            } else if (winBtn.buttonType === "restore") {
                ctx.beginPath()
                ctx.rect(m + 2, m, w - m * 2 - 2, h - m * 2 - 2)
                ctx.stroke()
                ctx.beginPath()
                ctx.moveTo(m, m + 4)
                ctx.lineTo(m, h - m)
                ctx.lineTo(w - m - 4, h - m)
                ctx.stroke()
            } else if (winBtn.buttonType === "close") {
                ctx.beginPath()
                ctx.moveTo(m, m)
                ctx.lineTo(w - m, h - m)
                ctx.stroke()
                ctx.beginPath()
                ctx.moveTo(w - m, m)
                ctx.lineTo(m, h - m)
                ctx.stroke()
            }
        }
    }

    Connections {
        target: themeManager
        function onColorsChanged() { btnCanvas.requestPaint() }
    }

    Connections {
        target: rootWindow
        function onIsMaximizedChanged() { btnCanvas.requestPaint() }
    }

    MouseArea {
        id: btnMouse
        anchors.fill: parent
        hoverEnabled: true
        onContainsMouseChanged: btnCanvas.requestPaint()
        onClicked: winBtn.clicked()
    }
}
