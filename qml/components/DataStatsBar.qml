import QtQuick 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: statsBar
    color: themeManager.bgTertiary
    radius: 4
    height: 22 * rootWindow.scaleFactor

    property alias rxBytes: rxText.text
    property alias txBytes: txText.text
    property alias rxRate: rxRateText.text
    property alias txRate: txRateText.text

    RowLayout {
        anchors.fill: parent
        anchors.leftMargin: 8
        anchors.rightMargin: 8
        spacing: 12

        Text {
            text: "RX:"
            color: "#4ec9b0"
            font.pixelSize: 9 * rootWindow.scaleFactor
            font.bold: true
            font.family: "monospace"
        }
        Text {
            id: rxText
            color: themeManager.textPrimary
            font.pixelSize: 9 * rootWindow.scaleFactor
            font.family: "monospace"
            text: "0"
        }
        Text {
            id: rxRateText
            color: themeManager.textSecondary
            font.pixelSize: 9 * rootWindow.scaleFactor
            font.family: "monospace"
            text: "0 B/s"
        }

        Item { width: 4 }
        Rectangle { width: 1; height: 12; color: themeManager.border }

        Text {
            text: "TX:"
            color: "#569cd6"
            font.pixelSize: 9 * rootWindow.scaleFactor
            font.bold: true
            font.family: "monospace"
        }
        Text {
            id: txText
            color: themeManager.textPrimary
            font.pixelSize: 9 * rootWindow.scaleFactor
            font.family: "monospace"
            text: "0"
        }
        Text {
            id: txRateText
            color: themeManager.textSecondary
            font.pixelSize: 9 * rootWindow.scaleFactor
            font.family: "monospace"
            text: "0 B/s"
        }

        Item { Layout.fillWidth: true }
    }

    function formatBytes(bytes) {
        if (bytes < 1024) return bytes + " B"
        if (bytes < 1048576) return (bytes / 1024).toFixed(1) + " KB"
        return (bytes / 1048576).toFixed(2) + " MB"
    }

    function formatRate(bps) {
        if (bps < 1024) return bps.toFixed(0) + " B/s"
        if (bps < 1048576) return (bps / 1024).toFixed(1) + " KB/s"
        return (bps / 1048576).toFixed(2) + " MB/s"
    }
}
