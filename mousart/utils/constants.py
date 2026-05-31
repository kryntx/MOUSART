"""Constants and mapping tables for MOUSART."""

BAUD_RATES = [
    "300", "600", "1200", "2400", "4800", "9600",
    "19200", "38400", "57600", "115200", "230400", "460800", "921600"
]

DATA_BITS_LIST = ["5", "6", "7", "8"]
DATA_BITS_MAP = {"5": 5, "6": 6, "7": 7, "8": 8}

STOP_BITS_LIST = ["1", "1.5", "2"]
# Map UI index to serial.STOPBITS value
STOP_BITS_MAP = {0: 1, 1: 1.5, 2: 2}

PARITY_LIST = ["None", "Odd", "Even", "Mark", "Space"]
PARITY_MAP = {0: "N", 1: "O", 2: "E", 3: "M", 4: "S"}

FLOW_CONTROL_LIST = ["None", "Hardware", "Software"]
FLOW_MAP = {0: "none", 1: "hardware", 2: "software"}

ENCODING_LIST = ["自动 Auto", "UTF-8", "GBK", "GB18030", "Latin-1", "ASCII"]

# Modbus function code names
MODBUS_FUNC_NAMES = {
    0x01: "读线圈 (Read Coils)",
    0x02: "读离散输入 (Read Discrete Inputs)",
    0x03: "读保持寄存器 (Read Holding Registers)",
    0x04: "读输入寄存器 (Read Input Registers)",
    0x05: "写单个线圈 (Write Single Coil)",
    0x06: "写单个寄存器 (Write Single Register)",
    0x0F: "写多个线圈 (Write Multiple Coils)",
    0x10: "写多个寄存器 (Write Multiple Registers)",
}

MODBUS_EXCEPTION_NAMES = {
    1: "非法功能码 (Illegal Function)",
    2: "非法数据地址 (Illegal Data Address)",
    3: "非法数据值 (Illegal Data Value)",
    4: "从站设备故障 (Slave Device Failure)",
    5: "确认 (Acknowledge)",
    6: "从站设备忙 (Slave Device Busy)",
    7: "否定确认 (Negative Acknowledge)",
    8: "存储奇偶性差错 (Memory Parity Error)",
    10: "网关路径不可用 (Gateway Path Unavailable)",
    11: "网关目标设备响应失败 (Gateway Target Device Failed)",
}

# System TTY prefixes to filter
SYSTEM_TTY_PREFIXES = ("ttyS", "ttyAMA", "ttyO")

# Default quick commands
DEFAULT_QUICK_COMMANDS = [
    {"name": "AT", "data": "AT\r\n", "hex": False},
    {"name": "AT+RST", "data": "AT+RST\r\n", "hex": False},
    {"name": "Ping", "data": "FF 01 02 03", "hex": True},
]

SOCAT_ENABLED = True

DEFAULT_MAX_LOG_ENTRIES = 5000
LOG_ENTRIES_RANGE = (1000, 100000)
MAX_RECORD_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Modbus function code options for UI
MODBUS_FC_OPTIONS = [
    ("03 读保持寄存器", 3),
    ("04 读输入寄存器", 4),
    ("01 读线圈", 1),
    ("02 读离散输入", 2),
    ("06 写单寄存器", 6),
    ("05 写单线圈", 5),
    ("10 写多寄存器", 16),
    ("0F 写多线圈", 15),
]
