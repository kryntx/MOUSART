"""Data analysis utilities - encoding, checksums, Modbus, filtering."""
import re
from PyQt6.QtCore import QObject, pyqtSignal

from mousart.utils.encoding import decode_data, encode_string
from mousart.utils.checksum import calc_sum8, calc_xor8, calc_crc16_modbus, calc_crc32
from mousart.utils.modbus import build_modbus_rtu_frame, parse_modbus_rtu_frame
from mousart.utils.number_convert import to_binary, to_decimal, to_hex
from mousart.utils.hex_display import hex_to_formatted_display, bytes_to_hex, hex_to_bytes


class DataAnalyzer(QObject):
    """Stateless data analysis utility exposed to the UI."""

    error_occurred = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    # Hex conversion
    def bytesToHex(self, data: bytes, separator: str = " ") -> str:
        return bytes_to_hex(data, separator)

    def hexToBytes(self, hex_str: str) -> bytes:
        return hex_to_bytes(hex_str)

    def hexToFormattedDisplay(self, data: bytes) -> str:
        return hex_to_formatted_display(data)

    # Encoding
    def convertEncoding(self, data: bytes, from_enc: str, to_enc: str) -> str:
        text = decode_data(data, from_enc)
        if to_enc in ("UTF-8", "Unicode"):
            return text
        encoded = encode_string(text, to_enc)
        return bytes_to_hex(encoded, " ")

    def encodeString(self, text: str, encoding: str) -> bytes:
        return encode_string(text, encoding)

    def decodeBytes(self, data: bytes, encoding: str) -> str:
        return decode_data(data, encoding)

    # Checksums
    def calcSum8(self, data: bytes) -> int:
        return calc_sum8(data)

    def calcXor8(self, data: bytes) -> int:
        return calc_xor8(data)

    def calcCRC16Modbus(self, data: bytes) -> int:
        return calc_crc16_modbus(data)

    def calcCRC32(self, data: bytes) -> int:
        return calc_crc32(data)

    # Number conversion
    def toBinary(self, hex_or_dec: str) -> str:
        return to_binary(hex_or_dec)

    def toDecimal(self, hex_or_bin: str) -> str:
        return to_decimal(hex_or_bin)

    def toHex(self, dec_or_bin: str) -> str:
        return to_hex(dec_or_bin)

    # String utilities
    def escapeString(self, text: str) -> str:
        result = []
        for ch in text:
            if ch == '\\':
                result.append('\\\\')
            elif ch == '\r':
                result.append('\\r')
            elif ch == '\n':
                result.append('\\n')
            elif ch == '\t':
                result.append('\\t')
            elif ch == '\0':
                result.append('\\0')
            elif ord(ch) < 0x20:
                result.append(f'\\x{ord(ch):02x}')
            else:
                result.append(ch)
        return ''.join(result)

    def unescapeString(self, text: str) -> str:
        result = []
        i = 0
        while i < len(text):
            if text[i] == '\\' and i + 1 < len(text):
                i += 1
                c = text[i]
                if c == 'r':
                    result.append('\r')
                elif c == 'n':
                    result.append('\n')
                elif c == 't':
                    result.append('\t')
                elif c == '0':
                    result.append('\0')
                elif c == '\\':
                    result.append('\\')
                elif c == 'x':
                    if i + 2 < len(text):
                        hex_str = text[i + 1:i + 3]
                        try:
                            result.append(chr(int(hex_str, 16)))
                            i += 2
                        except ValueError:
                            result.append('\\x')
                    else:
                        result.append('\\x')
                else:
                    result.append('\\')
                    result.append(c)
            else:
                result.append(text[i])
            i += 1
        return ''.join(result)

    def textToHex(self, text: str) -> str:
        return bytes_to_hex(text.encode('utf-8'), " ")

    def hexToText(self, hex_str: str) -> str:
        data = hex_to_bytes(hex_str)
        return data.decode('utf-8', errors='replace')

    # Modbus
    def buildModbusRtuFrame(self, slave_addr: int, func_code: int,
                            start_addr: int, quantity: int) -> bytes:
        return build_modbus_rtu_frame(slave_addr, func_code, start_addr, quantity)

    def parseModbusRtuFrame(self, frame: bytes) -> str:
        return parse_modbus_rtu_frame(frame)

    # Filtering
    def matchFilter(self, data: str, filter_str: str, use_regex: bool) -> bool:
        if not filter_str:
            return True
        if use_regex:
            try:
                return bool(re.search(filter_str, data, re.IGNORECASE))
            except re.error:
                return False
        return filter_str.lower() in data.lower()
