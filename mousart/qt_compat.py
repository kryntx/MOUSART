"""Qt compatibility layer - supports both PyQt6 and PyQt5."""
import sys

try:
    from PyQt6.QtWidgets import *
    from PyQt6.QtCore import *
    from PyQt6.QtGui import *
    QT_VERSION = 6

    # PyQt6 compatibility aliases
    Qt_Orientation_Vertical = Qt.Orientation.Vertical
    Qt_WindowType_FramelessWindowHint = Qt.WindowType.FramelessWindowHint
    Qt_WindowType_Window = Qt.WindowType.Window
    Qt_WidgetAttribute_WA_TranslucentBackground = Qt.WidgetAttribute.WA_TranslucentBackground
    Qt_HighDpiScaleFactorRoundingPolicy_PassThrough = Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    Qt_AlignmentFlag_AlignCenter = Qt.AlignmentFlag.AlignCenter
    Qt_AlignmentFlag_AlignVCenter = Qt.AlignmentFlag.AlignVCenter
    Qt_AlignmentFlag_AlignRight = Qt.AlignmentFlag.AlignRight
    Qt_PenStyle_NoPen = Qt.PenStyle.NoPen
    Qt_PenStyle_SolidLine = Qt.PenStyle.SolidLine
    Qt_PenCapStyle_RoundCap = Qt.PenCapStyle.RoundCap
    Qt_BrushStyle_NoBrush = Qt.BrushStyle.NoBrush
    Qt_CursorShape_ArrowCursor = Qt.CursorShape.ArrowCursor
    Qt_CursorShape_SizeHorCursor = Qt.CursorShape.SizeHorCursor
    Qt_CursorShape_SizeVerCursor = Qt.CursorShape.SizeVerCursor
    Qt_CursorShape_SizeFDiagCursor = Qt.CursorShape.SizeFDiagCursor
    Qt_CursorShape_SizeBDiagCursor = Qt.CursorShape.SizeBDiagCursor
    Qt_CursorShape_SplitVCursor = Qt.CursorShape.SplitVCursor
    Qt_MouseButton_LeftButton = Qt.MouseButton.LeftButton
    Qt_MouseButton_RightButton = Qt.MouseButton.RightButton
    Qt_KeyboardModifier_ControlModifier = Qt.KeyboardModifier.ControlModifier
    Qt_Key_Return = Qt.Key.Key_Return
    Qt_ScrollBarPolicy_ScrollBarAlwaysOff = Qt.ScrollBarPolicy.ScrollBarAlwaysOff
    Qt_ScrollBarPolicy_ScrollBarAsNeeded = Qt.ScrollBarPolicy.ScrollBarAsNeeded
    Qt_TextFormat_PlainText = Qt.TextFormat.PlainText
    Qt_ItemDataRole_DisplayRole = Qt.ItemDataRole.DisplayRole
    Qt_CheckState_Checked = Qt.CheckState.Checked
    Qt_CheckState_Unchecked = Qt.CheckState.Unchecked
    QFrame_Shape_HLine = QFrame.Shape.HLine
    QFrame_Shape_VLine = QFrame.Shape.VLine
    QDialog_DialogCode_Accepted = QDialog.DialogCode.Accepted
    QDialog_DialogCode_Rejected = QDialog.DialogCode.Rejected
    QDialogButtonBox_StandardButton_Ok = QDialogButtonBox.StandardButton.Ok
    QDialogButtonBox_StandardButton_Cancel = QDialogButtonBox.StandardButton.Cancel
    QMessageBox_StandardButton_Yes = QMessageBox.StandardButton.Yes
    QMessageBox_StandardButton_No = QMessageBox.StandardButton.No
    QFileDialog_Option_ReadOnly = QFileDialog.Option.ReadOnly
    QComboBox_InsertPolicy_NoInsert = QComboBox.InsertPolicy.NoInsert
    Qt_TimerType_PreciseTimer = Qt.TimerType.PreciseTimer
    Qt_WindowState_WindowMaximized = Qt.WindowState.WindowMaximized
    Qt_WindowState_WindowNormal = Qt.WindowState.WindowNoState
    QEvent_Type_WindowStateChange = QEvent.Type.WindowStateChange
    QEvent_Type_KeyPress = QEvent.Type.KeyPress
    QMouseEvent_Position = lambda e: e.position()

except ImportError:
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    QT_VERSION = 5

    # PyQt5 compatibility aliases
    Qt_Orientation_Vertical = Qt.Vertical
    Qt_WindowType_FramelessWindowHint = Qt.FramelessWindowHint
    Qt_WindowType_Window = Qt.Window
    Qt_WidgetAttribute_WA_TranslucentBackground = Qt.WA_TranslucentBackground
    Qt_HighDpiScaleFactorRoundingPolicy_PassThrough = None
    Qt_AlignmentFlag_AlignCenter = Qt.AlignCenter
    Qt_AlignmentFlag_AlignVCenter = Qt.AlignVCenter
    Qt_AlignmentFlag_AlignRight = Qt.AlignRight
    Qt_PenStyle_NoPen = Qt.NoPen
    Qt_PenStyle_SolidLine = Qt.SolidLine
    Qt_PenCapStyle_RoundCap = Qt.RoundCap
    Qt_BrushStyle_NoBrush = Qt.NoBrush
    Qt_CursorShape_ArrowCursor = Qt.ArrowCursor
    Qt_CursorShape_SizeHorCursor = Qt.SizeHorCursor
    Qt_CursorShape_SizeVerCursor = Qt.SizeVerCursor
    Qt_CursorShape_SizeFDiagCursor = Qt.SizeFDiagCursor
    Qt_CursorShape_SizeBDiagCursor = Qt.SizeBDiagCursor
    Qt_CursorShape_SplitVCursor = Qt.SplitVCursor
    Qt_MouseButton_LeftButton = Qt.LeftButton
    Qt_MouseButton_RightButton = Qt.RightButton
    Qt_KeyboardModifier_ControlModifier = Qt.ControlModifier
    Qt_Key_Return = Qt.Key_Return
    Qt_ScrollBarPolicy_ScrollBarAlwaysOff = Qt.ScrollBarAlwaysOff
    Qt_ScrollBarPolicy_ScrollBarAsNeeded = Qt.ScrollBarAsNeeded
    Qt_TextFormat_PlainText = Qt.PlainText
    Qt_ItemDataRole_DisplayRole = Qt.DisplayRole
    Qt_CheckState_Checked = Qt.Checked
    Qt_CheckState_Unchecked = Qt.Unchecked
    QFrame_Shape_HLine = QFrame.HLine
    QFrame_Shape_VLine = QFrame.VLine
    QDialog_DialogCode_Accepted = QDialog.Accepted
    QDialog_DialogCode_Rejected = QDialog.Rejected
    QDialogButtonBox_StandardButton_Ok = QDialogButtonBox.Ok
    QDialogButtonBox_StandardButton_Cancel = QDialogButtonBox.Cancel
    QMessageBox_StandardButton_Yes = QMessageBox.Yes
    QMessageBox_StandardButton_No = QMessageBox.No
    QFileDialog_Option_ReadOnly = QFileDialog.ReadOnly
    QComboBox_InsertPolicy_NoInsert = QComboBox.NoInsert
    Qt_TimerType_PreciseTimer = Qt.PreciseTimer
    Qt_WindowState_WindowMaximized = Qt.WindowMaximized
    Qt_WindowState_WindowNormal = Qt.WindowNoState
    QEvent_Type_WindowStateChange = QEvent.WindowStateChange
    QEvent_Type_KeyPress = QEvent.KeyPress
    QMouseEvent_Position = lambda e: e.pos()


def get_qt_version():
    return QT_VERSION
