import QtQuick 2.15
import QtQuick.Controls 2.15

ComboBox {
    id: styledCombo
    implicitHeight: 32 * rootWindow.scaleFactor

    background: Rectangle {
        radius: 6
        color: themeManager.bgPrimary
        border.color: styledCombo.pressed ? themeManager.accent : themeManager.border
        border.width: 1
    }

    contentItem: Text {
        text: styledCombo.displayText
        color: themeManager.textPrimary
        font.pixelSize: 12 * rootWindow.scaleFactor
        verticalAlignment: Text.AlignVCenter
        leftPadding: 8
    }

    delegate: ItemDelegate {
        width: styledCombo.width
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
            styledCombo.currentIndex = index
            styledCombo.popup.close()
        }
    }

    popup: Popup {
        y: styledCombo.height
        width: styledCombo.width
        implicitHeight: contentItem.implicitHeight + 2
        padding: 1

        contentItem: ListView {
            implicitHeight: contentHeight
            model: styledCombo.popup.visible ? styledCombo.delegateModel : null
            currentIndex: styledCombo.highlightedIndex
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
