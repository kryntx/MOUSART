"""Configuration persistence - quick commands, auto-reply rules, profiles."""
import json
import os
from mousart.qt_compat import *

from mousart.utils.constants import DEFAULT_QUICK_COMMANDS, DEFAULT_MAX_LOG_ENTRIES


class ConfigManager(QObject):
    """Manages application configuration, quick commands, and profiles."""

    quick_commands_changed = pyqtSignal()
    auto_reply_rules_changed = pyqtSignal()
    send_sequences_changed = pyqtSignal()
    current_profile_changed = pyqtSignal()
    profiles_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._settings = QSettings("MOUSART", "MOUSART")
        self._current_profile = self._settings.value("currentProfile", "default")
        self._quick_commands = []
        self._auto_reply_rules = []
        self._send_sequences = []
        self._load_quick_commands()
        self._load_auto_reply_rules()
        self._load_send_sequences()

    @property
    def quick_commands(self):
        return self._quick_commands

    @property
    def auto_reply_rules(self):
        return self._auto_reply_rules

    @property
    def send_sequences(self):
        return self._send_sequences

    @property
    def current_profile(self):
        return self._current_profile

    @current_profile.setter
    def current_profile(self, profile):
        if self._current_profile == profile:
            return
        self._current_profile = profile
        self._settings.setValue("currentProfile", profile)
        self.current_profile_changed.emit()

    @property
    def max_log_entries(self) -> int:
        val = self._settings.value("maxLogEntries", DEFAULT_MAX_LOG_ENTRIES)
        try:
            return int(val)
        except (TypeError, ValueError):
            return DEFAULT_MAX_LOG_ENTRIES

    @max_log_entries.setter
    def max_log_entries(self, value: int):
        if self.max_log_entries == value:
            return
        self._settings.setValue("maxLogEntries", value)

    def get_profiles(self) -> list:
        result = ["default"]
        config_dir = os.path.join(os.path.expanduser("~"), ".mousart", "profiles")
        if os.path.isdir(config_dir):
            for f in sorted(os.listdir(config_dir)):
                if f.endswith(".json"):
                    name = f[:-5]
                    if name != "default" and name not in result:
                        result.append(name)
        return result

    # Quick Commands
    def addQuickCommand(self, name: str, data: str, hex_mode: bool):
        self._quick_commands.append({"name": name, "data": data, "hex": hex_mode})
        self._save_quick_commands()
        self.quick_commands_changed.emit()

    def removeQuickCommand(self, index: int):
        if 0 <= index < len(self._quick_commands):
            self._quick_commands.pop(index)
            self._save_quick_commands()
            self.quick_commands_changed.emit()

    def updateQuickCommand(self, index: int, name: str, data: str, hex_mode: bool):
        if 0 <= index < len(self._quick_commands):
            self._quick_commands[index] = {"name": name, "data": data, "hex": hex_mode}
            self._save_quick_commands()
            self.quick_commands_changed.emit()

    def moveQuickCommand(self, frm: int, to: int):
        if (0 <= frm < len(self._quick_commands) and 0 <= to < len(self._quick_commands)):
            cmd = self._quick_commands.pop(frm)
            self._quick_commands.insert(to, cmd)
            self._save_quick_commands()
            self.quick_commands_changed.emit()

    # Auto-reply Rules
    def addAutoReplyRule(self, name: str, match: str, response: str,
                         delay: int, enabled: bool, use_regex: bool):
        self._auto_reply_rules.append({
            "name": name, "match": match, "response": response,
            "delay": delay, "enabled": enabled, "regex": use_regex
        })
        self._save_auto_reply_rules()
        self.auto_reply_rules_changed.emit()

    def removeAutoReplyRule(self, index: int):
        if 0 <= index < len(self._auto_reply_rules):
            self._auto_reply_rules.pop(index)
            self._save_auto_reply_rules()
            self.auto_reply_rules_changed.emit()

    def updateAutoReplyRule(self, index: int, name: str, match: str,
                            response: str, delay: int, enabled: bool, use_regex: bool):
        if 0 <= index < len(self._auto_reply_rules):
            self._auto_reply_rules[index] = {
                "name": name, "match": match, "response": response,
                "delay": delay, "enabled": enabled, "regex": use_regex
            }
            self._save_auto_reply_rules()
            self.auto_reply_rules_changed.emit()

    def toggleAutoReplyRule(self, index: int, enabled: bool):
        if 0 <= index < len(self._auto_reply_rules):
            self._auto_reply_rules[index]["enabled"] = enabled
            self._save_auto_reply_rules()
            self.auto_reply_rules_changed.emit()

    # Send Sequences
    def addSendSequence(self, name: str, steps: list):
        self._send_sequences.append({"name": name, "steps": steps})
        self._save_send_sequences()
        self.send_sequences_changed.emit()

    def removeSendSequence(self, index: int):
        if 0 <= index < len(self._send_sequences):
            self._send_sequences.pop(index)
            self._save_send_sequences()
            self.send_sequences_changed.emit()

    def updateSendSequence(self, index: int, name: str, steps: list):
        if 0 <= index < len(self._send_sequences):
            self._send_sequences[index] = {"name": name, "steps": steps}
            self._save_send_sequences()
            self.send_sequences_changed.emit()

    # Profiles
    def saveProfile(self, name: str):
        config_dir = os.path.join(os.path.expanduser("~"), ".mousart", "profiles")
        os.makedirs(config_dir, exist_ok=True)
        path = os.path.join(config_dir, f"{name}.json")

        profile = {
            "serialConfig": self.loadSerialConfig(),
            "quickCommands": self._quick_commands,
            "autoReplyRules": self._auto_reply_rules,
            "sendSequences": self._send_sequences,
        }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(profile, f, ensure_ascii=False, indent=2)
        self.profiles_changed.emit()

    def loadProfile(self, name: str):
        config_dir = os.path.join(os.path.expanduser("~"), ".mousart", "profiles")
        path = os.path.join(config_dir, f"{name}.json")
        if not os.path.isfile(path):
            return

        with open(path, "r", encoding="utf-8") as f:
            profile = json.load(f)

        if "serialConfig" in profile:
            self.saveSerialConfig(profile["serialConfig"])

        if "quickCommands" in profile:
            self._quick_commands = profile["quickCommands"]
            self._save_quick_commands()
            self.quick_commands_changed.emit()

        if "autoReplyRules" in profile:
            self._auto_reply_rules = profile["autoReplyRules"]
            self._save_auto_reply_rules()
            self.auto_reply_rules_changed.emit()

        if "sendSequences" in profile:
            self._send_sequences = profile["sendSequences"]
            self._save_send_sequences()
            self.send_sequences_changed.emit()

        self.current_profile = name

    def deleteProfile(self, name: str):
        if name == "default":
            return
        config_dir = os.path.join(os.path.expanduser("~"), ".mousart", "profiles")
        path = os.path.join(config_dir, f"{name}.json")
        if os.path.isfile(path):
            os.remove(path)
        self.profiles_changed.emit()

    # Serial config persistence
    def saveSerialConfig(self, config: dict):
        self._settings.beginGroup("SerialConfig")
        for key, value in config.items():
            self._settings.setValue(key, value)
        self._settings.endGroup()

    def loadSerialConfig(self) -> dict:
        config = {}
        self._settings.beginGroup("SerialConfig")
        for key in self._settings.childKeys():
            config[key] = self._settings.value(key)
        self._settings.endGroup()
        return config

    # Private helpers
    def _save_quick_commands(self):
        data = json.dumps(self._quick_commands, ensure_ascii=False)
        self._settings.setValue("quickCommands", data)

    def _load_quick_commands(self):
        data = self._settings.value("quickCommands", "")
        if not data:
            self._quick_commands = list(DEFAULT_QUICK_COMMANDS)
            self._save_quick_commands()
            return
        try:
            self._quick_commands = json.loads(data)
        except (json.JSONDecodeError, TypeError):
            self._quick_commands = list(DEFAULT_QUICK_COMMANDS)

    def _save_auto_reply_rules(self):
        data = json.dumps(self._auto_reply_rules, ensure_ascii=False)
        self._settings.setValue("autoReplyRules", data)

    def _load_auto_reply_rules(self):
        data = self._settings.value("autoReplyRules", "")
        if not data:
            return
        try:
            self._auto_reply_rules = json.loads(data)
        except (json.JSONDecodeError, TypeError):
            self._auto_reply_rules = []

    def _save_send_sequences(self):
        data = json.dumps(self._send_sequences, ensure_ascii=False)
        self._settings.setValue("sendSequences", data)

    def _load_send_sequences(self):
        data = self._settings.value("sendSequences", "")
        if not data:
            return
        try:
            self._send_sequences = json.loads(data)
        except (json.JSONDecodeError, TypeError):
            self._send_sequences = []
