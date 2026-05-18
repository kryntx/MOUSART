import QtQuick 2.15
import QtQuick.Controls 2.15

ComboBox {
    id: editableCombo
    editable: true
    implicitHeight: 32 * rootWindow.scaleFactor

    property string currentTextValue: editText

    background: Rectangle {
        radius: 6
        color: themeManager.bgPrimary
        border.color: editableCombo.pressed ? themeManager.accent : themeManager.border
        border.width: 1
    }

    contentItem: TextField {
        text: editableCombo.editText
        color: themeManager.textPrimary
        font.pixelSize: 12 * rootWindow.scaleFactor
        verticalAlignment: Text.AlignVCenter
        leftPadding: 8
        background: null
        validator: IntValidator { bottom: 1; top: 9999999 }

        onEditingFinished: editableCombo.editText = text
    }

    delegate: ItemDelegate {
        width: editableCombo.width
        height: 30 * rootWindow.scaleFactor

        contentItem: Text {
            text: modelData
            color: themeManager.textPrimary
            font.pixelSize: 12 * rootWindow.scaleFactor
            verticalAlignment: Text.AlignVCenter
            leftPadding: 8
        }

        background: Rectangle {
            color: parent.hovered ? themeManager.accent : themeManager.bgSecondary
            radius: 2
        }

        onClicked: {
            editableCombo.currentIndex = index
            editableCombo.editText = modelData
            editableCombo.popup.close()
        }
    }

    popup: Popup {
        y: editableCombo.height
        width: editableCombo.width
        implicitHeight: contentItem.implicitHeight + 2
        padding: 1

        contentItem: ListView {
            implicitHeight: contentHeight
            model: editableCombo.popup.visible ? editableCombo.delegateModel : null
            currentIndex: editableCombo.highlightedIndex
            clip: true

            ScrollIndicator.vertical: ScrollIndicator {}
        }

        background: Rectangle {
            radius: 6
            color: themeManager.bgSecondary
            border.color: themeManager.border
        }
    }
}
