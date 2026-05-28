import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15

Rectangle {
    id: autoReplyPanel
    color: themeManager.bgSecondary
    border.color: themeManager.border
    border.width: 1
    radius: 6

    property bool enabled: false
    property string matchText: ""
    property string responseText: ""
    property int delayMs: 0

    signal toggled(bool enabled)
    signal matchChanged(string text)
    signal responseChanged(string text)
    signal delayChanged(int ms)

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 6
        spacing: 4

        RowLayout {
            Layout.fillWidth: true
            spacing: 4

            Text {
                text: qsTr("自动应答")
                color: themeManager.textSecondary
                font.pixelSize: 9 * rootWindow.scaleFactor
                font.bold: true
            }

            Item { Layout.fillWidth: true }

            Rectangle {
                Layout.preferredWidth: 36 * rootWindow.scaleFactor
                Layout.preferredHeight: 16 * rootWindow.scaleFactor
                radius: 8
                color: autoReplyPanel.enabled ? themeManager.accent : themeManager.bgTertiary
                border.color: themeManager.border

                Rectangle {
                    width: parent.height - 4
                    height: width
                    radius: width / 2
                    y: 2
                    x: autoReplyPanel.enabled ? parent.width - width - 2 : 2
                    color: "#ffffff"
                    Behavior on x { NumberAnimation { duration: 120 } }
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: autoReplyPanel.toggled(!autoReplyPanel.enabled)
                }
            }
        }

        Text {
            text: qsTr("匹配关键字")
            color: themeManager.textSecondary
            font.pixelSize: 8 * rootWindow.scaleFactor
        }

        TextField {
            id: matchField
            Layout.fillWidth: true
            Layout.preferredHeight: 22 * rootWindow.scaleFactor
            text: autoReplyPanel.matchText
            placeholderText: qsTr("输入匹配字符串...")
            color: themeManager.textPrimary
            font.pixelSize: 10 * rootWindow.scaleFactor
            background: Rectangle {
                radius: 4
                color: themeManager.bgPrimary
                border.color: matchField.activeFocus ? themeManager.accent : themeManager.border
            }
            onEditingFinished: autoReplyPanel.matchChanged(text)
        }

        Text {
            text: qsTr("应答数据")
            color: themeManager.textSecondary
            font.pixelSize: 8 * rootWindow.scaleFactor
        }

        TextField {
            id: responseField
            Layout.fillWidth: true
            Layout.preferredHeight: 22 * rootWindow.scaleFactor
            text: autoReplyPanel.responseText
            placeholderText: qsTr("收到匹配数据时自动回复...")
            color: themeManager.textPrimary
            font.pixelSize: 10 * rootWindow.scaleFactor
            background: Rectangle {
                radius: 4
                color: themeManager.bgPrimary
                border.color: responseField.activeFocus ? themeManager.accent : themeManager.border
            }
            onEditingFinished: autoReplyPanel.responseChanged(text)
        }

        RowLayout {
            Layout.fillWidth: true
            spacing: 4

            Text {
                text: qsTr("延迟ms")
                color: themeManager.textSecondary
                font.pixelSize: 8 * rootWindow.scaleFactor
            }

            TextField {
                id: delayField
                Layout.preferredWidth: 50 * rootWindow.scaleFactor
                Layout.preferredHeight: 20 * rootWindow.scaleFactor
                text: autoReplyPanel.delayMs.toString()
                color: themeManager.textPrimary
                font.pixelSize: 9 * rootWindow.scaleFactor
                validator: IntValidator { bottom: 0; top: 60000 }
                background: Rectangle {
                    radius: 4
                    color: themeManager.bgPrimary
                    border.color: delayField.activeFocus ? themeManager.accent : themeManager.border
                }
                onEditingFinished: {
                    var val = parseInt(text)
                    if (!isNaN(val)) autoReplyPanel.delayChanged(val)
                }
            }

            Item { Layout.fillWidth: true }
        }
    }
}
