"""Permission error dialog for Linux dialout group issues."""
import grp
import os
import subprocess

from mousart.qt_compat import *
from mousart.ui.widgets.small_button import SmallButton


class PermissionDialog(QDialog):
    """Dialog shown when a serial port permission error occurs on Linux."""

    def __init__(self, port_name: str, in_dialout_group: bool,
                 parent=None, theme_manager=None):
        super().__init__(parent)
        self._theme_manager = theme_manager
        self._port_name = port_name
        self._in_dialout_group = in_dialout_group

        self.setWindowTitle("权限错误 Permission Error")
        self.setMinimumSize(520, 420)
        self.resize(560, 480)

        self._build_ui()
        self._apply_theme()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        # -- Error icon / header --
        header_layout = QHBoxLayout()
        icon_label = QLabel("⚠")  # warning sign
        icon_label.setFixedWidth(30)
        icon_label.setAlignment(Qt_AlignmentFlag_AlignCenter)
        icon_label.setStyleSheet("font-size: 24px; color: #e5c07b;")
        header_layout.addWidget(icon_label)

        title_label = QLabel(
            f"无法打开串口 Cannot open port: {self._port_name}"
        )
        title_label.setStyleSheet(
            "font-size: 13px; font-weight: bold; color: #e5c07b;"
        )
        header_layout.addWidget(title_label, 1)
        layout.addLayout(header_layout)

        # -- Explanation --
        explanation = QLabel(
            "当前用户没有访问该串口设备的权限。\n"
            "Your user does not have permission to access this serial device."
        )
        explanation.setWordWrap(True)
        layout.addWidget(explanation)

        # -- Current groups info --
        groups_box = QGroupBox("当前用户组 Your Groups")
        groups_layout = QVBoxLayout(groups_box)
        try:
            import grp as _grp
            current_groups = os.getgroups()
            group_names = []
            for gid in current_groups:
                try:
                    group_names.append(_grp.getgrgid(gid).gr_name)
                except KeyError:
                    group_names.append(str(gid))
            groups_text = ", ".join(sorted(group_names))
        except OSError:
            groups_text = "(unable to determine)"

        groups_label = QLabel(groups_text)
        groups_label.setWordWrap(True)
        groups_label.setStyleSheet("font-family: monospace; font-size: 11px;")
        groups_layout.addWidget(groups_label)

        dialout_status = QLabel(
            "dialout 组: 已加入"
            if self._in_dialout_group
            else "dialout 组: 未加入 (NOT a member)"
        )
        dialout_color = "#98c379" if self._in_dialout_group else "#e06c75"
        dialout_status.setStyleSheet(
            f"font-weight: bold; color: {dialout_color};"
        )
        groups_layout.addWidget(dialout_status)
        layout.addWidget(groups_box)

        # -- Fix instructions --
        fix_box = QGroupBox("修复步骤 Fix Steps")
        fix_layout = QVBoxLayout(fix_box)

        # Step 1: command
        cmd_layout = QHBoxLayout()
        cmd_label = QLabel(
            "1. 运行以下命令 Run this command:"
        )
        cmd_layout.addWidget(cmd_label)
        fix_layout.addLayout(cmd_layout)

        cmd_row = QHBoxLayout()
        self._cmd_line = QLineEdit("sudo usermod -aG dialout $USER")
        self._cmd_line.setReadOnly(True)
        cmd_row.addWidget(self._cmd_line, 1)

        self._copy_btn = SmallButton(
            "复制命令 Copy", theme_manager=self._theme_manager, accent=True
        )
        self._copy_btn.clicked_custom.connect(self._copy_command)
        cmd_row.addWidget(self._copy_btn)
        fix_layout.addLayout(cmd_row)

        # Step 2
        step2 = QLabel(
            "2. 注销并重新登录，或运行 Log out and back in, or run:\n"
            "   newgrp dialout"
        )
        step2.setWordWrap(True)
        fix_layout.addWidget(step2)

        # Step 3
        step3 = QLabel(
            "3. 重新尝试连接 Try connecting again."
        )
        step3.setWordWrap(True)
        fix_layout.addWidget(step3)

        layout.addWidget(fix_box, 1)

        # -- Bottom buttons --
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)

        self._temp_fix_btn = SmallButton(
            "临时修复 Temporary Fix (pkexec chmod 666)",
            theme_manager=self._theme_manager,
        )
        self._temp_fix_btn.clicked_custom.connect(self._run_temp_fix)
        btn_layout.addWidget(self._temp_fix_btn)

        btn_layout.addStretch()

        self._close_btn = SmallButton(
            "关闭 Close", theme_manager=self._theme_manager
        )
        self._close_btn.clicked_custom.connect(self.accept)
        btn_layout.addWidget(self._close_btn)

        layout.addLayout(btn_layout)

    def _copy_command(self):
        """Copy the fix command to clipboard."""
        clipboard = QApplication.clipboard()
        if clipboard:
            clipboard.setText("sudo usermod -aG dialout $USER")
            self._copy_btn.setText("已复制 Copied!")
            QTimer.singleShot(1500, lambda: self._copy_btn.setText(
                "复制命令 Copy"
            ))

    def _run_temp_fix(self):
        """Run pkexec chmod 666 as a temporary fix."""
        try:
            result = subprocess.run(
                ["pkexec", "chmod", "666", self._port_name],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                self._temp_fix_btn.setText("修复成功 Fixed!")
                self._temp_fix_btn.set_btn_enabled(False)
            else:
                self._temp_fix_btn.setText("失败 Failed")
                QTimer.singleShot(
                    2000,
                    lambda: self._temp_fix_btn.setText(
                        "临时修复 Temporary Fix (pkexec chmod 666)"
                    ),
                )
        except FileNotFoundError:
            self._temp_fix_btn.setText("pkexec 不可用")
            QTimer.singleShot(
                2000,
                lambda: self._temp_fix_btn.setText(
                    "临时修复 Temporary Fix (pkexec chmod 666)"
                ),
            )

    def _apply_theme(self):
        if self._theme_manager:
            bg = self._theme_manager.get_color_hex("bgSecondary")
            bg_tert = self._theme_manager.get_color_hex("bgTertiary")
            border = self._theme_manager.get_color_hex("border")
            text = self._theme_manager.get_color_hex("textPrimary")
            text_sec = self._theme_manager.get_color_hex("textSecondary")
            self.setStyleSheet(f"""
                QDialog {{
                    background: {bg};
                    border: 1px solid {border};
                    border-radius: 8px;
                }}
                QLabel {{
                    color: {text};
                }}
                QGroupBox {{
                    color: {text};
                    border: 1px solid {border};
                    border-radius: 6px;
                    margin-top: 6px;
                    padding-top: 14px;
                    font-weight: bold;
                }}
                QGroupBox::title {{
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 4px;
                }}
                QLineEdit {{
                    background: {bg_tert};
                    color: {text};
                    border: 1px solid {border};
                    border-radius: 4px;
                    padding: 4px 8px;
                    font-family: monospace;
                    font-size: 11px;
                }}
            """)
