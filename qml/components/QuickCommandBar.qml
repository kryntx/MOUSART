import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15

Rectangle {
    id: quickCmdBar
    color: themeManager.bgSecondary
    border.color: themeManager.border
    border.width: 1
    radius: 6

    property bool hexSend: false
    signal sendCommand(string data, bool hexMode)
    signal addRequested()
    signal editRequested(int index)

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 4
        spacing: 2

        RowLayout {
            Layout.fillWidth: true
            spacing: 4

            Text {
                text: qsTr("快捷命令")
                color: themeManager.textSecondary
                font.pixelSize: 9 * rootWindow.scaleFactor
                font.bold: true
            }

            Item { Layout.fillWidth: true }

            SmallButton {
                label: "+"
                onClicked: quickCmdBar.addRequested()
            }
        }

        Flow {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 4

            Repeater {
                model: configManager.quickCommands

                Rectangle {
                    width: Math.max(cmdText.implicitWidth + 16, 60) * rootWindow.scaleFactor
                    height: 22 * rootWindow.scaleFactor
                    radius: 4
                    color: cmdMouse.containsMouse ? themeManager.accent : themeManager.bgTertiary
                    border.color: themeManager.border
                    border.width: 1

                    Text {
                        id: cmdText
                        anchors.centerIn: parent
                        text: modelData.name || modelData
                        color: cmdMouse.containsMouse ? "#ffffff" : themeManager.textPrimary
                        font.pixelSize: 9 * rootWindow.scaleFactor
                        elide: Text.ElideRight
                        width: parent.width - 8
                        horizontalAlignment: Text.AlignHCenter
                    }

                    MouseArea {
                        id: cmdMouse
                        anchors.fill: parent
                        hoverEnabled: true
                        acceptedButtons: Qt.LeftButton | Qt.RightButton

                        onClicked: {
                            if (mouse.button === Qt.LeftButton) {
                                var cmd = configManager.quickCommands[index]
                                quickCmdBar.sendCommand(cmd.data, cmd.hex)
                            } else if (mouse.button === Qt.RightButton) {
                                quickCmdBar.editRequested(index)
                            }
                        }
                    }
                }
            }
        }
    }
}
