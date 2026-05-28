import QtQuick 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: pinBar
    color: themeManager.bgSecondary
    border.color: themeManager.border
    border.width: 1
    radius: 6

    property bool dtrState: false
    property bool rtsState: false
    property bool ctsState: false
    property bool dsrState: false
    property bool dcdState: false
    property bool riState: false

    signal dtrToggled(bool state)
    signal rtsToggled(bool state)

    RowLayout {
        anchors.fill: parent
        anchors.leftMargin: 6
        anchors.rightMargin: 6
        spacing: 8

        Text {
            text: "PIN"
            color: themeManager.textSecondary
            font.pixelSize: 9 * rootWindow.scaleFactor
            font.bold: true
        }

        // DTR toggle
        Rectangle {
            width: 42 * rootWindow.scaleFactor
            height: 18 * rootWindow.scaleFactor
            radius: 9
            color: pinBar.dtrState ? themeManager.accent : themeManager.bgTertiary
            border.color: themeManager.border

            Text {
                anchors.centerIn: parent
                text: "DTR"
                color: pinBar.dtrState ? "#ffffff" : themeManager.textSecondary
                font.pixelSize: 8 * rootWindow.scaleFactor
                font.bold: true
            }

            MouseArea {
                anchors.fill: parent
                onClicked: pinBar.dtrToggled(!pinBar.dtrState)
            }
        }

        // RTS toggle
        Rectangle {
            width: 42 * rootWindow.scaleFactor
            height: 18 * rootWindow.scaleFactor
            radius: 9
            color: pinBar.rtsState ? themeManager.accent : themeManager.bgTertiary
            border.color: themeManager.border

            Text {
                anchors.centerIn: parent
                text: "RTS"
                color: pinBar.rtsState ? "#ffffff" : themeManager.textSecondary
                font.pixelSize: 8 * rootWindow.scaleFactor
                font.bold: true
            }

            MouseArea {
                anchors.fill: parent
                onClicked: pinBar.rtsToggled(!pinBar.rtsState)
            }
        }

        Rectangle { width: 1; height: 14; color: themeManager.border }

        // Status indicators
        Repeater {
            model: [
                { label: "CTS", active: pinBar.ctsState },
                { label: "DSR", active: pinBar.dsrState },
                { label: "DCD", active: pinBar.dcdState },
                { label: "RI", active: pinBar.riState }
            ]

            Row {
                spacing: 3
                Rectangle {
                    width: 6; height: 6; radius: 3
                    anchors.verticalCenter: parent.verticalCenter
                    color: modelData.active ? "#4ec9b0" : themeManager.bgTertiary
                    border.color: themeManager.border
                    border.width: 1
                }
                Text {
                    text: modelData.label
                    color: themeManager.textSecondary
                    font.pixelSize: 8 * rootWindow.scaleFactor
                    font.family: "monospace"
                }
            }
        }

        Item { Layout.fillWidth: true }
    }
}
