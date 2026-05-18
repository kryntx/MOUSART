import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import "components"

Rectangle {
    id: dataPanel
    color: themeManager.bgPrimary

    property real receiveHeight: height * 0.6
    property bool hexDisplay: false
    property bool hexSend: false
    property bool showTimestamp: true
    property int currentMode: settingsPanel.mode
    property int timedSendInterval: 1000

    function doSend() {
        var area = currentMode === 0 ? virtualSendArea : debugSendArea
        if (area.text.length === 0) return false
        var result
        if (currentMode === 0)
            result = virtualManager.sendData(area.text, dataPanel.hexSend)
        else
            result = serialManager.sendData(area.text, dataPanel.hexSend)
        if (result > 0) {
            dataPanel.addLogEntry("TX", area.text)
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
        if (model.count > 500) model.remove(0, model.count - 500)
        if (model === (currentMode === 0 ? virtualLogModel : debugLogModel))
            logView.positionViewAtEnd()
    }

    onCurrentModeChanged: logView.positionViewAtEnd()

    function formatHex(rawData) {
        var display = ""
        for (var i = 0; i < rawData.length; i++) {
            if (i > 0) display += " "
            var b = rawData[i] & 0xFF
            var hex = b.toString(16).toUpperCase()
            if (hex.length < 2) hex = "0" + hex
            display += hex
        }
        return display
    }

    Connections {
        target: serialManager
        function onDataReceived(data, rawData) {
            dataPanel.addLogEntry("RX", dataPanel.hexDisplay ? dataPanel.formatHex(rawData) : data, debugLogModel)
        }
        function onErrorOccurred(error) {
            dataPanel.addLogEntry("ERR", error, debugLogModel)
        }
        function onTimedSendCompleted(data) {
            dataPanel.addLogEntry("TX", data, debugLogModel)
        }
    }

    Connections {
        target: virtualManager
        function onDataReceived(data, rawData) {
            dataPanel.addLogEntry("RX", dataPanel.hexDisplay ? dataPanel.formatHex(rawData) : data, virtualLogModel)
        }
        function onErrorOccurred(error) {
            dataPanel.addLogEntry("ERR", error, virtualLogModel)
        }
        function onIsActiveChanged() {
            if (virtualManager.isActive) {
                dataPanel.addLogEntry("INFO", "虚拟串口已启动 " + virtualManager.externalPort, virtualLogModel)
            } else {
                dataPanel.addLogEntry("INFO", "虚拟串口已关闭", virtualLogModel)
            }
        }
        function onTimedSendCompleted(data) {
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
            Layout.minimumHeight: 60
            color: themeManager.receiveBg
            border.color: themeManager.border
            border.width: 1
            radius: 6

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 2
                spacing: 0

                RowLayout {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 26
                    spacing: 4

                    Text {
                        text: currentMode === 0 ? qsTr("模拟串口") : qsTr("串口调试")
                        color: themeManager.textSecondary
                        font.pixelSize: 10 * rootWindow.scaleFactor
                        font.bold: true
                        Layout.leftMargin: 6
                    }

                    Item { Layout.fillWidth: true }

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

                    SmallButton {
                        label: qsTr("清空")
                        onClicked: {
                            if (currentMode === 0) virtualLogModel.clear()
                            else debugLogModel.clear()
                        }
                    }

                    Item { width: 2 }
                }

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
                        color: index % 2 === 0 ? "transparent" : Qt.rgba(1,1,1,0.02)

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
                                color: themeManager.textPrimary
                                font.pixelSize: 11 * rootWindow.scaleFactor
                                font.family: "monospace"
                                width: logRow.parent.width - (dataPanel.showTimestamp ? 120 : 36)
                                wrapMode: Text.Wrap
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
                width: 32
                height: 2
                radius: 1
                color: dragHandleMouse.containsMouse ? themeManager.accent : themeManager.border
            }

            MouseArea {
                id: dragHandleMouse
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: Qt.SplitVCursor

                property real startY: 0
                property real startHeight: 0

                onPressed: {
                    startY = mapToItem(dataPanel, mouseX, mouseY).y
                    startHeight = dataPanel.receiveHeight
                }
                onPositionChanged: {
                    if (!pressed) return
                    var globalPos = mapToItem(dataPanel, mouseX, mouseY)
                    dataPanel.receiveHeight = Math.max(60, Math.min(dataPanel.height - 80, startHeight + (globalPos.y - startY)))
                }
            }
        }

        // Send area
        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.minimumHeight: 60
            color: themeManager.sendBg
            border.color: themeManager.border
            border.width: 1
            radius: 6

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 2
                spacing: 0

                RowLayout {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 26
                    spacing: 4

                    Text {
                        text: qsTr("发送")
                        color: themeManager.textSecondary
                        font.pixelSize: 10 * rootWindow.scaleFactor
                        font.bold: true
                        Layout.leftMargin: 6
                    }

                    Item { Layout.fillWidth: true }

                    SmallToggle {
                        label: "HEX"
                        active: dataPanel.hexSend
                        onClicked: dataPanel.hexSend = !dataPanel.hexSend
                    }

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
                                    if (!isNaN(val) && val >= 1)
                                        dataPanel.timedSendInterval = val
                                    else
                                        text = dataPanel.timedSendInterval.toString()
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
                                    var area = virtualSendArea
                                    if (area.text.length > 0)
                                        virtualManager.startTimedSend(area.text, dataPanel.hexSend, dataPanel.timedSendInterval)
                                } else {
                                    virtualManager.stopTimedSend()
                                }
                            } else {
                                if (!serialManager.timedSendActive && serialManager.isOpen) {
                                    var area2 = debugSendArea
                                    if (area2.text.length > 0)
                                        serialManager.startTimedSend(area2.text, dataPanel.hexSend, dataPanel.timedSendInterval)
                                } else {
                                    serialManager.stopTimedSend()
                                }
                            }
                        }
                    }

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
                                if (text.length > 0 && virtualManager.isActive)
                                    dataPanel.doSend()
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
                                if (text.length > 0 && serialManager.isOpen)
                                    dataPanel.doSend()
                                event.accepted = true
                            } else {
                                event.accepted = false
                            }
                        }
                    }
                }
            }
        }
    }
}
