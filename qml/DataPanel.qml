import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import "components"

Rectangle {
    id: dataPanel
    color: themeManager.bgPrimary

    property real receiveHeight: height * 0.55
    property bool hexDisplay: false
    property bool hexSend: false
    property bool showTimestamp: true
    property bool showDirection: true
    property int currentMode: settingsPanel.mode
    property int timedSendInterval: 1000
    property int timedSendCount: -1  // -1 = infinite
    property bool echoEnabled: false
    property string filterText: ""
    property bool filterRegex: false
    property bool pauseDisplay: false
    property string searchText: ""
    property bool showModbusPanel: false

    function doSend() {
        var area = currentMode === 0 ? virtualSendArea : debugSendArea
        if (area.text.length === 0) return false
        var result
        if (currentMode === 0)
            result = virtualManager.sendData(area.text, dataPanel.hexSend)
        else
            result = serialManager.sendData(area.text, dataPanel.hexSend)
        if (result > 0) {
            if (dataPanel.echoEnabled) {
                dataPanel.addLogEntry("TX", dataPanel.hexSend ? dataAnalyzer.textToHex(area.text) : area.text)
            }
            return true
        }
        return false
    }

    function addLogEntry(type, data, toModel) {
        var model = toModel || (currentMode === 0 ? virtualLogModel : debugLogModel)
        model.append({
            "logTime": Qt.formatDateTime(new Date(), "hh:mm:ss.zzz"),
            "logType": type,
            "logData": data
        })
        if (model.count > 2000) model.remove(0, model.count - 2000)
        if (!dataPanel.pauseDisplay && model === (currentMode === 0 ? virtualLogModel : debugLogModel))
            logView.positionViewAtEnd()
    }

    onCurrentModeChanged: logView.positionViewAtEnd()

    function formatHex(rawData) {
        return dataAnalyzer.bytesToHex(rawData, " ")
    }

    function formatRate(bps) {
        if (bps < 1024) return bps.toFixed(0) + " B/s"
        if (bps < 1048576) return (bps / 1024).toFixed(1) + " KB/s"
        return (bps / 1048576).toFixed(2) + " MB/s"
    }

    function formatBytes(bytes) {
        if (bytes < 1024) return bytes + " B"
        if (bytes < 1048576) return (bytes / 1024).toFixed(1) + " KB"
        return (bytes / 1048576).toFixed(2) + " MB"
    }

    function getLogEntries() {
        var model = currentMode === 0 ? virtualLogModel : debugLogModel
        var entries = []
        for (var i = 0; i < model.count; i++) {
            entries.push({
                "logTime": model.get(i).logTime,
                "logType": model.get(i).logType,
                "logData": model.get(i).logData
            })
        }
        return entries
    }

    Connections {
        target: serialManager
        function onDataReceived(data, rawData) {
            var displayData = dataPanel.hexDisplay ? dataPanel.formatHex(rawData) : data
            if (dataPanel.filterText.length > 0) {
                if (!dataAnalyzer.matchFilter(displayData, dataPanel.filterText, dataPanel.filterRegex))
                    return
            }
            dataPanel.addLogEntry("RX", displayData, debugLogModel)
            if (logFileManager.isRecording)
                logFileManager.recordData("RX", rawData, displayData)
        }
        function onErrorOccurred(error) {
            dataPanel.addLogEntry("ERR", error, debugLogModel)
        }
        function onTimedSendCompleted(data) {
            if (dataPanel.echoEnabled)
                dataPanel.addLogEntry("TX", data, debugLogModel)
        }
        function onPortOpened(portName) {
            dataPanel.addLogEntry("SYS", qsTr("已连接: ") + portName, debugLogModel)
        }
        function onPortClosed() {
            dataPanel.addLogEntry("SYS", qsTr("已断开"), debugLogModel)
        }
    }

    Connections {
        target: virtualManager
        function onDataReceived(data, rawData) {
            var displayData = dataPanel.hexDisplay ? dataPanel.formatHex(rawData) : data
            if (dataPanel.filterText.length > 0) {
                if (!dataAnalyzer.matchFilter(displayData, dataPanel.filterText, dataPanel.filterRegex))
                    return
            }
            dataPanel.addLogEntry("RX", displayData, virtualLogModel)
            if (logFileManager.isRecording)
                logFileManager.recordData("RX", rawData, displayData)
        }
        function onErrorOccurred(error) {
            dataPanel.addLogEntry("ERR", error, virtualLogModel)
        }
        function onIsActiveChanged() {
            if (virtualManager.isActive)
                dataPanel.addLogEntry("INFO", "虚拟串口已启动 " + virtualManager.externalPort, virtualLogModel)
            else
                dataPanel.addLogEntry("INFO", "虚拟串口已关闭", virtualLogModel)
        }
        function onTimedSendCompleted(data) {
            if (dataPanel.echoEnabled)
                dataPanel.addLogEntry("TX", data, virtualLogModel)
        }
    }

    ListModel { id: virtualLogModel }
    ListModel { id: debugLogModel }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 6
        spacing: 0

        // Receive area
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: dataPanel.receiveHeight
            Layout.minimumHeight: 80
            color: themeManager.receiveBg
            border.color: themeManager.border
            border.width: 1
            radius: 6

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 2
                spacing: 0

                // Receive toolbar
                RowLayout {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 26
                    spacing: 3

                    Text {
                        text: currentMode === 0 ? qsTr("模拟串口") : qsTr("串口调试")
                        color: themeManager.textSecondary
                        font.pixelSize: 10 * rootWindow.scaleFactor
                        font.bold: true
                        Layout.leftMargin: 6
                    }

                    SmallToggle {
                        label: "HEX"
                        active: dataPanel.hexDisplay
                        onClicked: dataPanel.hexDisplay = !dataPanel.hexDisplay
                    }

                    SmallToggle {
                        label: qsTr("时间")
                        active: dataPanel.showTimestamp
                        onClicked: dataPanel.showTimestamp = !dataPanel.showTimestamp
                    }

                    SmallToggle {
                        label: "↕"
                        active: dataPanel.showDirection
                        onClicked: dataPanel.showDirection = !dataPanel.showDirection
                    }

                    SmallToggle {
                        label: qsTr("暂停")
                        active: dataPanel.pauseDisplay
                        onClicked: dataPanel.pauseDisplay = !dataPanel.pauseDisplay
                    }

                    Rectangle { width: 1; height: 14; color: themeManager.border }

                    // Search field
                    Rectangle {
                        width: 100 * rootWindow.scaleFactor
                        height: 18 * rootWindow.scaleFactor
                        radius: 9
                        color: themeManager.bgTertiary
                        border.color: searchInput.activeFocus ? themeManager.accent : "transparent"
                        border.width: 1

                        TextInput {
                            id: searchInput
                            anchors.fill: parent
                            anchors.leftMargin: 6
                            anchors.rightMargin: 6
                            verticalAlignment: TextInput.AlignVCenter
                            text: dataPanel.searchText
                            color: themeManager.textPrimary
                            font.pixelSize: 9 * rootWindow.scaleFactor
                            clip: true
                            onTextChanged: dataPanel.searchText = text
                        }
                    }

                    SmallButton {
                        label: dataPanel.filterText.length > 0 ? qsTr("过滤✓") : qsTr("过滤")
                        accent: dataPanel.filterText.length > 0
                        onClicked: filterMenu.popup()
                    }

                    Menu {
                        id: filterMenu
                        MenuItem {
                            text: qsTr("清除过滤")
                            onTriggered: dataPanel.filterText = ""
                        }
                        MenuItem {
                            text: qsTr("仅含关键字...")
                            onTriggered: {
                                dataPanel.filterText = dataPanel.searchText
                                dataPanel.filterRegex = false
                            }
                        }
                        MenuItem {
                            text: qsTr("正则匹配...")
                            onTriggered: {
                                dataPanel.filterText = dataPanel.searchText
                                dataPanel.filterRegex = true
                            }
                        }
                    }

                    Item { Layout.fillWidth: true }

                    SmallButton {
                        label: qsTr("保存")
                        onClicked: {
                            var path = logFileManager.getSaveLogPath()
                            if (path && path.length > 0) {
                                var entries = dataPanel.getLogEntries()
                                if (path.endsWith(".csv"))
                                    logFileManager.exportToCsv(path, entries)
                                else
                                    logFileManager.saveLogToFile(path, entries)
                            }
                        }
                    }

                    SmallToggle {
                        label: qsTr("录制")
                        active: logFileManager.isRecording
                        onClicked: {
                            if (logFileManager.isRecording)
                                logFileManager.stopRecording()
                            else
                                logFileManager.startRecording()
                        }
                    }

                    SmallButton {
                        label: qsTr("清空")
                        onClicked: {
                            if (currentMode === 0) virtualLogModel.clear()
                            else debugLogModel.clear()
                        }
                    }

                    Item { width: 2 }
                }

                // Log view
                ListView {
                    id: logView
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    clip: true
                    model: currentMode === 0 ? virtualLogModel : debugLogModel
                    spacing: 1

                    delegate: Rectangle {
                        width: logView.width
                        height: logRow.height + 2
                        color: {
                            if (model.logType === "ERR") return Qt.rgba(0.9, 0.2, 0.2, 0.1)
                            if (index % 2 === 0) return "transparent"
                            return Qt.rgba(1,1,1,0.02)
                        }

                        Row {
                            id: logRow
                            anchors.left: parent.left
                            anchors.right: parent.right
                            anchors.leftMargin: 6
                            anchors.rightMargin: 6
                            anchors.verticalCenter: parent.verticalCenter
                            spacing: 6

                            Text {
                                visible: dataPanel.showTimestamp
                                text: model.logTime
                                color: themeManager.textSecondary
                                font.pixelSize: 11 * rootWindow.scaleFactor
                                font.family: "monospace"
                            }

                            Text {
                                visible: dataPanel.showDirection
                                width: 16
                                horizontalAlignment: Text.AlignHCenter
                                text: {
                                    switch(model.logType) {
                                        case "RX": return "<<"
                                        case "TX": return ">>"
                                        case "ERR": return "!!"
                                        case "INFO": return "i"
                                        case "SYS": return "#"
                                        default: return "?"
                                    }
                                }
                                color: {
                                    switch(model.logType) {
                                        case "RX": return "#4ec9b0"
                                        case "TX": return "#569cd6"
                                        case "ERR": return "#f44747"
                                        case "INFO": return "#dcdcaa"
                                        case "SYS": return "#9cdcfe"
                                        default: return themeManager.textSecondary
                                    }
                                }
                                font.pixelSize: 11 * rootWindow.scaleFactor
                                font.bold: true
                                font.family: "monospace"
                            }

                            Text {
                                text: model.logData
                                color: {
                                    if (model.logType === "ERR") return "#f44747"
                                    return themeManager.textPrimary
                                }
                                font.pixelSize: 11 * rootWindow.scaleFactor
                                font.family: "monospace"
                                width: logRow.parent.width - (dataPanel.showTimestamp ? 120 : 36) - (dataPanel.showDirection ? 22 : 0)
                                wrapMode: Text.Wrap
                                textFormat: Text.PlainText
                            }
                        }
                    }

                    ScrollBar.vertical: ScrollBar { policy: ScrollBar.AsNeeded }
                }
            }
        }

        // Drag handle
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 6
            color: "transparent"

            Rectangle {
                anchors.centerIn: parent
                width: 32; height: 2; radius: 1
                color: dragHandleMouse.containsMouse ? themeManager.accent : themeManager.border
            }

            MouseArea {
                id: dragHandleMouse
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: Qt.SplitVCursor
                property real startY: 0
                property real startHeight: 0
                onPressed: { startY = mapToItem(dataPanel, mouseX, mouseY).y; startHeight = dataPanel.receiveHeight }
                onPositionChanged: {
                    if (!pressed) return
                    var globalPos = mapToItem(dataPanel, mouseX, mouseY)
                    dataPanel.receiveHeight = Math.max(80, Math.min(dataPanel.height - 100, startHeight + (globalPos.y - startY)))
                }
            }
        }

        // Send area
        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.minimumHeight: 80
            color: themeManager.sendBg
            border.color: themeManager.border
            border.width: 1
            radius: 6

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 2
                spacing: 0

                // Send toolbar
                RowLayout {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 26
                    spacing: 3

                    Text {
                        text: qsTr("发送")
                        color: themeManager.textSecondary
                        font.pixelSize: 10 * rootWindow.scaleFactor
                        font.bold: true
                        Layout.leftMargin: 6
                    }

                    SmallToggle {
                        label: "HEX"
                        active: dataPanel.hexSend
                        onClicked: dataPanel.hexSend = !dataPanel.hexSend
                    }

                    SmallToggle {
                        label: qsTr("回显")
                        active: dataPanel.echoEnabled
                        onClicked: dataPanel.echoEnabled = !dataPanel.echoEnabled
                    }

                    Rectangle { width: 1; height: 14; color: themeManager.border }

                    // Timed send interval
                    Rectangle {
                        width: 72 * rootWindow.scaleFactor
                        height: 20 * rootWindow.scaleFactor
                        radius: 10
                        color: themeManager.bgTertiary
                        border.color: timedSendInput.activeFocus ? themeManager.accent : "transparent"
                        border.width: 1

                        Row {
                            anchors.fill: parent
                            anchors.leftMargin: 8
                            anchors.rightMargin: 2
                            spacing: 0

                            TextInput {
                                id: timedSendInput
                                width: parent.width - msLabel.width - parent.spacing
                                height: parent.height
                                verticalAlignment: TextInput.AlignVCenter
                                text: dataPanel.timedSendInterval.toString()
                                color: themeManager.textPrimary
                                font.pixelSize: 9 * rootWindow.scaleFactor
                                font.family: "monospace"
                                validator: IntValidator { bottom: 1; top: 3600000 }
                                inputMethodHints: Qt.ImhDigitsOnly
                                onEditingFinished: {
                                    var val = parseInt(text)
                                    if (!isNaN(val) && val >= 1) dataPanel.timedSendInterval = val
                                    else text = dataPanel.timedSendInterval.toString()
                                }
                            }

                            Text {
                                id: msLabel
                                height: parent.height
                                verticalAlignment: Text.AlignVCenter
                                text: "ms"
                                color: themeManager.textSecondary
                                font.pixelSize: 9 * rootWindow.scaleFactor
                            }
                        }
                    }

                    SmallToggle {
                        label: qsTr("定时")
                        active: currentMode === 0 ? virtualManager.timedSendActive : serialManager.timedSendActive
                        onClicked: {
                            if (currentMode === 0) {
                                if (!virtualManager.timedSendActive && virtualManager.isActive) {
                                    if (virtualSendArea.text.length > 0)
                                        virtualManager.startTimedSend(virtualSendArea.text, dataPanel.hexSend, dataPanel.timedSendInterval, dataPanel.timedSendCount)
                                } else {
                                    virtualManager.stopTimedSend()
                                }
                            } else {
                                if (!serialManager.timedSendActive && serialManager.isOpen) {
                                    if (debugSendArea.text.length > 0)
                                        serialManager.startTimedSend(debugSendArea.text, dataPanel.hexSend, dataPanel.timedSendInterval, dataPanel.timedSendCount)
                                } else {
                                    serialManager.stopTimedSend()
                                }
                            }
                        }
                    }

                    SmallButton {
                        label: qsTr("文件")
                        onClicked: {
                            var path = logFileManager.getSendFilePath()
                            if (path && path.length > 0) {
                                var result
                                if (currentMode === 0)
                                    result = "N/A"
                                else
                                    result = serialManager.sendFileData(path, dataPanel.hexSend)
                                dataPanel.addLogEntry("INFO", qsTr("文件发送: ") + result)
                            }
                        }
                    }

                    SmallToggle {
                        label: "Modbus"
                        active: dataPanel.showModbusPanel
                        onClicked: dataPanel.showModbusPanel = !dataPanel.showModbusPanel
                    }

                    Item { Layout.fillWidth: true }

                    SmallButton {
                        label: qsTr("发送")
                        accent: true
                        btnEnabled: {
                            return (currentMode === 0 && virtualManager.isActive) ||
                                   (currentMode === 1 && serialManager.isOpen)
                        }
                        onClicked: dataPanel.doSend()
                    }

                    Item { width: 2 }
                }

                // Modbus helper panel
                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: dataPanel.showModbusPanel ? modbusRow.implicitHeight + 12 : 0
                    visible: dataPanel.showModbusPanel
                    color: themeManager.bgTertiary
                    clip: true

                    RowLayout {
                        id: modbusRow
                        anchors.fill: parent
                        anchors.margins: 6
                        spacing: 6

                        Text { text: "Addr:"; color: themeManager.textSecondary; font.pixelSize: 9 * rootWindow.scaleFactor }
                        TextField {
                            id: modbusAddr
                            Layout.preferredWidth: 36; Layout.preferredHeight: 22
                            text: "1"; color: themeManager.textPrimary; font.pixelSize: 10
                            background: Rectangle { radius: 4; color: themeManager.bgPrimary; border.color: themeManager.border }
                        }
                        Text { text: "FC:"; color: themeManager.textSecondary; font.pixelSize: 9 * rootWindow.scaleFactor }
                        ComboBox {
                            id: modbusFcCombo
                            Layout.preferredWidth: 100; Layout.preferredHeight: 22
                            model: ["03 读保持", "04 读输入", "01 读线圈", "06 写单寄存器"]
                            property var fcValues: [3, 4, 1, 6]
                        }
                        Text { text: "Addr:"; color: themeManager.textSecondary; font.pixelSize: 9 * rootWindow.scaleFactor }
                        TextField {
                            id: modbusStartAddr
                            Layout.preferredWidth: 50; Layout.preferredHeight: 22
                            text: "0"; color: themeManager.textPrimary; font.pixelSize: 10
                            background: Rectangle { radius: 4; color: themeManager.bgPrimary; border.color: themeManager.border }
                        }
                        Text { text: "Qty:"; color: themeManager.textSecondary; font.pixelSize: 9 * rootWindow.scaleFactor }
                        TextField {
                            id: modbusQty
                            Layout.preferredWidth: 36; Layout.preferredHeight: 22
                            text: "1"; color: themeManager.textPrimary; font.pixelSize: 10
                            background: Rectangle { radius: 4; color: themeManager.bgPrimary; border.color: themeManager.border }
                        }
                        SmallButton {
                            label: qsTr("构建")
                            accent: true
                            onClicked: {
                                var addr = parseInt(modbusAddr.text) || 1
                                var fc = modbusFcCombo.fcValues[modbusFcCombo.currentIndex] || 3
                                var start = parseInt(modbusStartAddr.text) || 0
                                var qty = parseInt(modbusQty.text) || 1
                                var frame = dataAnalyzer.buildModbusRtuFrame(addr, fc, start, qty)
                                var area = currentMode === 0 ? virtualSendArea : debugSendArea
                                area.text = dataAnalyzer.bytesToHex(frame, " ")
                            }
                        }
                        Item { Layout.fillWidth: true }
                    }
                }

                // Virtual mode send area
                ScrollView {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    visible: currentMode === 0

                    TextArea {
                        id: virtualSendArea
                        placeholderText: qsTr("Ctrl+Enter 发送")
                        color: themeManager.textPrimary
                        font.pixelSize: 12 * rootWindow.scaleFactor
                        font.family: "monospace"
                        wrapMode: TextArea.Wrap
                        selectByMouse: true
                        background: null

                        Keys.onReturnPressed: {
                            if (event.modifiers & Qt.ControlModifier) {
                                if (text.length > 0 && virtualManager.isActive) dataPanel.doSend()
                                event.accepted = true
                            } else {
                                event.accepted = false
                            }
                        }
                    }
                }

                // Debug mode send area
                ScrollView {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    visible: currentMode === 1

                    TextArea {
                        id: debugSendArea
                        placeholderText: qsTr("Ctrl+Enter 发送")
                        color: themeManager.textPrimary
                        font.pixelSize: 12 * rootWindow.scaleFactor
                        font.family: "monospace"
                        wrapMode: TextArea.Wrap
                        selectByMouse: true
                        background: null

                        Keys.onReturnPressed: {
                            if (event.modifiers & Qt.ControlModifier) {
                                if (text.length > 0 && serialManager.isOpen) dataPanel.doSend()
                                event.accepted = true
                            } else {
                                event.accepted = false
                            }
                        }
                    }
                }
            }
        }

        // Quick commands bar
        QuickCommandBar {
            Layout.fillWidth: true
            Layout.preferredHeight: 50 * rootWindow.scaleFactor
            hexSend: dataPanel.hexSend
            onSendCommand: function(data, hexMode) {
                if (currentMode === 0) {
                    if (virtualManager.isActive) {
                        virtualManager.sendData(data, hexMode)
                        dataPanel.addLogEntry("TX", hexMode ? dataAnalyzer.textToHex(data) : data, virtualLogModel)
                    }
                } else {
                    if (serialManager.isOpen) {
                        serialManager.sendData(data, hexMode)
                        if (dataPanel.echoEnabled)
                            dataPanel.addLogEntry("TX", hexMode ? dataAnalyzer.textToHex(data) : data, debugLogModel)
                    }
                }
            }
            onAddRequested: quickCmdDialog.open()
            onEditRequested: function(index) {
                var cmd = configManager.quickCommands[index]
                quickCmdEditIndex = index
                quickCmdEditName.text = cmd.name
                quickCmdEditData.text = cmd.data
                quickCmdEditHex.checked = cmd.hex
                quickCmdEditDialog.open()
            }
        }

        // Data stats bar
        DataStatsBar {
            Layout.fillWidth: true
            Layout.preferredHeight: 22 * rootWindow.scaleFactor
            rxBytes: {
                var bytes = currentMode === 0 ? virtualManager.rxBytes : serialManager.rxBytes
                return formatBytes(bytes)
            }
            txBytes: {
                var bytes = currentMode === 0 ? virtualManager.txBytes : serialManager.txBytes
                return formatBytes(bytes)
            }
            rxRate: formatRate(currentMode === 0 ? virtualManager.rxRate : serialManager.rxRate)
            txRate: formatRate(currentMode === 0 ? virtualManager.txRate : serialManager.txRate)
        }
    }

    // Quick command add dialog
    Dialog {
        id: quickCmdDialog
        title: qsTr("添加快捷命令")
        modal: true
        anchors.centerIn: parent
        width: 300
        standardButtons: Dialog.Ok | Dialog.Cancel

        ColumnLayout {
            anchors.fill: parent
            spacing: 8
            Text { text: qsTr("名称"); color: themeManager.textPrimary }
            TextField { id: quickCmdName; Layout.fillWidth: true; placeholderText: "AT" }
            Text { text: qsTr("数据"); color: themeManager.textPrimary }
            TextField { id: quickCmdData; Layout.fillWidth: true; placeholderText: "AT\\r\\n" }
            CheckBox { id: quickCmdHex; text: "HEX模式"; checked: false }
        }

        onAccepted: {
            if (quickCmdName.text.length > 0)
                configManager.addQuickCommand(quickCmdName.text, quickCmdData.text, quickCmdHex.checked)
            quickCmdName.text = ""
            quickCmdData.text = ""
            quickCmdHex.checked = false
        }
    }

    // Quick command edit dialog
    property int quickCmdEditIndex: -1
    Dialog {
        id: quickCmdEditDialog
        title: qsTr("编辑快捷命令")
        modal: true
        anchors.centerIn: parent
        width: 300
        standardButtons: Dialog.Ok | Dialog.Cancel

        ColumnLayout {
            anchors.fill: parent
            spacing: 8
            Text { text: qsTr("名称"); color: themeManager.textPrimary }
            TextField { id: quickCmdEditName; Layout.fillWidth: true }
            Text { text: qsTr("数据"); color: themeManager.textPrimary }
            TextField { id: quickCmdEditData; Layout.fillWidth: true }
            CheckBox { id: quickCmdEditHex; text: "HEX模式" }
        }

        onAccepted: {
            if (quickCmdEditIndex >= 0)
                configManager.updateQuickCommand(quickCmdEditIndex, quickCmdEditName.text, quickCmdEditData.text, quickCmdEditHex.checked)
        }
        onRejected: quickCmdEditIndex = -1
    }
}
