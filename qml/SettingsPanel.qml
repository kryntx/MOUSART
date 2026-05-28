import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import "components"

Rectangle {
    id: settingsPanel
    color: themeManager.bgSecondary

    property int mode: 0  // 0 = virtual serial, 1 = real serial

    readonly property var baudRates: ["300", "600", "1200", "2400", "4800", "9600", "19200", "38400", "57600", "115200", "230400", "460800", "921600"]
    readonly property var dataBitsList: ["5", "6", "7", "8"]
    readonly property var stopBitsList: ["1", "1.5", "2"]
    readonly property var parityList: ["None", "Odd", "Even", "Mark", "Space"]
    readonly property var flowControlList: ["None", "Hardware", "Software"]
    readonly property var encodingList: ["UTF-8", "GBK", "GB18030", "Latin-1", "ASCII"]

    property string currentBaudRate: "115200"
    property int selectedDataBits: 3
    property int selectedStopBits: 0
    property int selectedParity: 0
    property int selectedFlow: 0
    property int selectedPort: 0
    property int selectedEncoding: 0

    ScrollView {
        anchors.fill: parent
        anchors.margins: 10
        clip: true

        ColumnLayout {
            width: settingsPanel.width - 20
            spacing: 8

            // Mode selector
            Text {
                text: qsTr("模式 Mode")
                color: themeManager.textSecondary
                font.pixelSize: 11 * rootWindow.scaleFactor
                font.bold: true
            }

            RowLayout {
                Layout.fillWidth: true
                spacing: 4

                ModeButton {
                    label: qsTr("模拟串口")
                    sublabel: "Virtual"
                    isActive: settingsPanel.mode === 0
                    Layout.fillWidth: true
                    onClicked: settingsPanel.mode = 0
                }

                ModeButton {
                    label: qsTr("串口调试")
                    sublabel: "Debug"
                    isActive: settingsPanel.mode === 1
                    Layout.fillWidth: true
                    onClicked: settingsPanel.mode = 1
                }
            }

            Rectangle { Layout.fillWidth: true; Layout.preferredHeight: 1; color: themeManager.border }

            // Virtual serial port controls
            ColumnLayout {
                Layout.fillWidth: true
                spacing: 8
                visible: settingsPanel.mode === 0

                Text {
                    text: qsTr("虚拟串口 Virtual Port")
                    color: themeManager.textSecondary
                    font.pixelSize: 11 * rootWindow.scaleFactor
                    font.bold: true
                }

                Text {
                    text: qsTr("MOUSART 作为串口A端收发数据，\nB端供外部程序或设备连接")
                    color: themeManager.textSecondary
                    font.pixelSize: 10 * rootWindow.scaleFactor
                    wrapMode: Text.Wrap
                    Layout.fillWidth: true
                }

                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: virtualManager.isActive ? extPortCol.implicitHeight + 12 : 0
                    visible: virtualManager.isActive
                    radius: 6
                    color: themeManager.bgTertiary

                    Column {
                        id: extPortCol
                        anchors.left: parent.left
                        anchors.right: parent.right
                        anchors.margins: 8
                        anchors.verticalCenter: parent.verticalCenter
                        spacing: 4

                        Text {
                            text: qsTr("外部端口 (B端)")
                            color: themeManager.textSecondary
                            font.pixelSize: 10 * rootWindow.scaleFactor
                        }
                        Text {
                            text: virtualManager.externalPort
                            color: themeManager.accent
                            font.pixelSize: 14 * rootWindow.scaleFactor
                            font.family: "monospace"
                            font.bold: true
                        }
                        Text {
                            text: qsTr("将此路径提供给外部程序连接")
                            color: themeManager.textSecondary
                            font.pixelSize: 9 * rootWindow.scaleFactor
                        }
                    }
                }

                // Encoding for virtual mode
                Text {
                    text: qsTr("接收编码 Encoding")
                    color: themeManager.textSecondary
                    font.pixelSize: 10 * rootWindow.scaleFactor
                }
                StyledComboBox {
                    Layout.fillWidth: true
                    model: settingsPanel.encodingList
                    currentIndex: settingsPanel.selectedEncoding
                    onCurrentIndexChanged: {
                        settingsPanel.selectedEncoding = currentIndex
                        virtualManager.receiveEncoding = settingsPanel.encodingList[currentIndex]
                    }
                }

                // Newline options for virtual
                RowLayout {
                    Layout.fillWidth: true
                    spacing: 6
                    Text { text: qsTr("发送换行"); color: themeManager.textSecondary; font.pixelSize: 10 * rootWindow.scaleFactor }
                    Item { Layout.fillWidth: true }
                    SmallToggle { label: "CR"; active: virtualManager.newlineCr; onClicked: virtualManager.newlineCr = !virtualManager.newlineCr }
                    SmallToggle { label: "LF"; active: virtualManager.newlineLf; onClicked: virtualManager.newlineLf = !virtualManager.newlineLf }
                }

                ActionButton {
                    label: virtualManager.isActive ? qsTr("停止 Stop") : qsTr("启动 Start")
                    isActive: virtualManager.isActive
                    Layout.fillWidth: true
                    Layout.preferredHeight: 34 * rootWindow.scaleFactor
                    onClicked: {
                        if (virtualManager.isActive)
                            virtualManager.stopVirtualPort()
                        else
                            virtualManager.startVirtualPort()
                    }
                }
            }

            // Real serial port controls
            ColumnLayout {
                Layout.fillWidth: true
                spacing: 8
                visible: settingsPanel.mode === 1

                Text {
                    text: qsTr("串口参数 Serial Config")
                    color: themeManager.textSecondary
                    font.pixelSize: 11 * rootWindow.scaleFactor
                    font.bold: true
                }

                // Port selector
                Text { text: qsTr("端口 Port"); color: themeManager.textSecondary; font.pixelSize: 10 * rootWindow.scaleFactor }
                RowLayout {
                    Layout.fillWidth: true
                    spacing: 4

                    StyledComboBox {
                        id: portCombo
                        Layout.fillWidth: true
                        model: serialManager.portList
                        currentIndex: Math.min(settingsPanel.selectedPort, serialManager.portList.length - 1)
                        onCurrentIndexChanged: settingsPanel.selectedPort = currentIndex
                    }

                    Rectangle {
                        Layout.preferredWidth: 32 * rootWindow.scaleFactor
                        Layout.preferredHeight: 32 * rootWindow.scaleFactor
                        radius: 6
                        color: refreshBtnMouse.containsMouse ? themeManager.bgTertiary : themeManager.bgPrimary
                        border.color: themeManager.border

                        Text {
                            anchors.centerIn: parent
                            text: "↻"
                            color: themeManager.textPrimary
                            font.pixelSize: 16 * rootWindow.scaleFactor
                        }

                        MouseArea {
                            id: refreshBtnMouse
                            anchors.fill: parent
                            hoverEnabled: true
                            onClicked: serialManager.refreshPorts()
                        }
                    }
                }

                // Port filter toggle
                RowLayout {
                    Layout.fillWidth: true
                    spacing: 6
                    Text { text: qsTr("过滤系统tty"); color: themeManager.textSecondary; font.pixelSize: 10 * rootWindow.scaleFactor }
                    Item { Layout.fillWidth: true }
                    Rectangle {
                        Layout.preferredWidth: 36 * rootWindow.scaleFactor
                        Layout.preferredHeight: 18 * rootWindow.scaleFactor
                        radius: 9
                        color: serialManager.filterSystemTty ? themeManager.accent : themeManager.bgTertiary
                        border.color: themeManager.border
                        Rectangle {
                            width: parent.height - 4; height: width; radius: width / 2
                            y: 2; x: serialManager.filterSystemTty ? parent.width - width - 2 : 2
                            color: "#ffffff"
                            Behavior on x { NumberAnimation { duration: 120 } }
                        }
                        MouseArea { anchors.fill: parent; onClicked: serialManager.filterSystemTty = !serialManager.filterSystemTty }
                    }
                }

                Text { text: qsTr("波特率 Baud Rate"); color: themeManager.textSecondary; font.pixelSize: 10 * rootWindow.scaleFactor }
                EditableComboBox {
                    id: baudCombo
                    Layout.fillWidth: true
                    model: settingsPanel.baudRates
                    currentIndex: 7
                    editText: settingsPanel.currentBaudRate
                    onEditTextChanged: settingsPanel.currentBaudRate = editText
                }

                Text { text: qsTr("数据位 Data Bits"); color: themeManager.textSecondary; font.pixelSize: 10 * rootWindow.scaleFactor }
                StyledComboBox { Layout.fillWidth: true; model: settingsPanel.dataBitsList; currentIndex: settingsPanel.selectedDataBits; onCurrentIndexChanged: settingsPanel.selectedDataBits = currentIndex }

                Text { text: qsTr("停止位 Stop Bits"); color: themeManager.textSecondary; font.pixelSize: 10 * rootWindow.scaleFactor }
                StyledComboBox { Layout.fillWidth: true; model: settingsPanel.stopBitsList; currentIndex: settingsPanel.selectedStopBits; onCurrentIndexChanged: settingsPanel.selectedStopBits = currentIndex }

                Text { text: qsTr("校验位 Parity"); color: themeManager.textSecondary; font.pixelSize: 10 * rootWindow.scaleFactor }
                StyledComboBox { Layout.fillWidth: true; model: settingsPanel.parityList; currentIndex: settingsPanel.selectedParity; onCurrentIndexChanged: settingsPanel.selectedParity = currentIndex }

                Text { text: qsTr("流控 Flow Control"); color: themeManager.textSecondary; font.pixelSize: 10 * rootWindow.scaleFactor }
                StyledComboBox { Layout.fillWidth: true; model: settingsPanel.flowControlList; currentIndex: settingsPanel.selectedFlow; onCurrentIndexChanged: settingsPanel.selectedFlow = currentIndex }

                Text { text: qsTr("接收编码 Encoding"); color: themeManager.textSecondary; font.pixelSize: 10 * rootWindow.scaleFactor }
                StyledComboBox {
                    Layout.fillWidth: true
                    model: settingsPanel.encodingList
                    currentIndex: settingsPanel.selectedEncoding
                    onCurrentIndexChanged: {
                        settingsPanel.selectedEncoding = currentIndex
                        serialManager.receiveEncoding = settingsPanel.encodingList[currentIndex]
                    }
                }

                // Newline options
                RowLayout {
                    Layout.fillWidth: true
                    spacing: 6
                    Text { text: qsTr("发送换行"); color: themeManager.textSecondary; font.pixelSize: 10 * rootWindow.scaleFactor }
                    Item { Layout.fillWidth: true }
                    SmallToggle { label: "CR"; active: serialManager.newlineCr; onClicked: serialManager.newlineCr = !serialManager.newlineCr }
                    SmallToggle { label: "LF"; active: serialManager.newlineLf; onClicked: serialManager.newlineLf = !serialManager.newlineLf }
                }

                // Pin control bar
                PinControlBar {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 24 * rootWindow.scaleFactor
                    visible: serialManager.isOpen
                    dtrState: serialManager.dtr
                    rtsState: serialManager.rts
                    ctsState: serialManager.cts
                    dsrState: serialManager.dsr
                    dcdState: serialManager.dcd
                    riState: serialManager.ri
                    onDtrToggled: function(state) { serialManager.dtr = state }
                    onRtsToggled: function(state) { serialManager.rts = state }
                }

                ActionButton {
                    label: serialManager.isOpen ? qsTr("关闭 Close") : qsTr("打开 Open")
                    isActive: serialManager.isOpen
                    Layout.fillWidth: true
                    Layout.preferredHeight: 36 * rootWindow.scaleFactor
                    onClicked: {
                        if (serialManager.isOpen) {
                            serialManager.closePort()
                        } else {
                            if (portCombo.currentIndex >= 0 && portCombo.currentIndex < serialManager.portList.length) {
                                var dataBitsMap = [5, 6, 7, 8]
                                var stopBitsMap = [1, 3, 2]
                                var parityMap = [0, 3, 2, 4, 1]
                                var flowMap = [0, 1, 2]
                                serialManager.openPort(
                                    serialManager.portList[portCombo.currentIndex],
                                    parseInt(settingsPanel.currentBaudRate) || 9600,
                                    dataBitsMap[settingsPanel.selectedDataBits],
                                    stopBitsMap[settingsPanel.selectedStopBits],
                                    parityMap[settingsPanel.selectedParity],
                                    flowMap[settingsPanel.selectedFlow]
                                )
                            }
                        }
                    }
                }
            }

            // Auto-reply section (visible in both modes)
            AutoReplyPanel {
                Layout.fillWidth: true
                Layout.preferredHeight: 140 * rootWindow.scaleFactor
                visible: settingsPanel.mode === 1
                enabled: serialManager.autoReplyEnabled
                matchText: serialManager.autoReplyMatch
                responseText: serialManager.autoReplyResponse
                delayMs: serialManager.autoReplyDelay
                onToggled: function(e) { serialManager.autoReplyEnabled = e }
                onMatchChanged: function(t) { serialManager.autoReplyMatch = t }
                onResponseChanged: function(t) { serialManager.autoReplyResponse = t }
                onDelayChanged: function(ms) { serialManager.autoReplyDelay = ms }
            }

            // Profile management
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: profileCol.implicitHeight + 12
                radius: 6
                color: themeManager.bgTertiary

                ColumnLayout {
                    id: profileCol
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.margins: 6
                    spacing: 4

                    RowLayout {
                        Layout.fillWidth: true
                        spacing: 4
                        Text {
                            text: qsTr("配置 Profile")
                            color: themeManager.textSecondary
                            font.pixelSize: 9 * rootWindow.scaleFactor
                            font.bold: true
                        }
                        Item { Layout.fillWidth: true }
                        SmallButton {
                            label: qsTr("保存")
                            onClicked: configManager.saveProfile(configManager.currentProfile)
                        }
                    }

                    StyledComboBox {
                        Layout.fillWidth: true
                        model: configManager.profiles
                        onCurrentTextChanged: {
                            if (currentText && currentText !== configManager.currentProfile)
                                configManager.loadProfile(currentText)
                        }
                    }
                }
            }

            Item { Layout.fillHeight: true }

            // Status bar
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 28 * rootWindow.scaleFactor
                radius: 4
                color: themeManager.bgTertiary

                Text {
                    anchors.centerIn: parent
                    text: {
                        if (settingsPanel.mode === 0) {
                            return virtualManager.isActive ? qsTr("已就绪 Ready") : qsTr("未启动 Inactive")
                        }
                        return serialManager.isOpen ? qsTr("已连接 Connected") : qsTr("未连接 Disconnected")
                    }
                    color: {
                        if (settingsPanel.mode === 0) {
                            return virtualManager.isActive ? themeManager.accent : themeManager.textSecondary
                        }
                        return serialManager.isOpen ? themeManager.accent : themeManager.textSecondary
                    }
                    font.pixelSize: 11 * rootWindow.scaleFactor
                }
            }
        }
    }
}
