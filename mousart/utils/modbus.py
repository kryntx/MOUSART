"""Modbus RTU frame builder and parser."""
from mousart.utils.checksum import calc_crc16_modbus
from mousart.utils.constants import MODBUS_FUNC_NAMES, MODBUS_EXCEPTION_NAMES


def build_modbus_rtu_frame(slave_addr: int, func_code: int,
                           start_addr: int, quantity: int) -> bytes:
    """Build a Modbus RTU request frame."""
    frame = bytearray()
    frame.append(slave_addr & 0xFF)
    frame.append(func_code & 0xFF)
    frame.append((start_addr >> 8) & 0xFF)
    frame.append(start_addr & 0xFF)
    frame.append((quantity >> 8) & 0xFF)
    frame.append(quantity & 0xFF)

    crc = calc_crc16_modbus(bytes(frame))
    frame.append(crc & 0xFF)
    frame.append((crc >> 8) & 0xFF)
    return bytes(frame)


def parse_modbus_rtu_frame(frame: bytes) -> str:
    """Parse a Modbus RTU frame and return a human-readable description."""
    if len(frame) < 4:
        return "帧长度不足 (Frame too short)"

    addr = frame[0]
    func = frame[1]

    result = f"地址: {addr} (0x{addr:02X})\n"

    func_name = MODBUS_FUNC_NAMES.get(func, f"未知功能码 (0x{func:02X})")
    result += f"功能码: 0x{func:02X} ({func_name})\n"

    if func & 0x80:
        # Error response
        if len(frame) >= 3:
            exc_code = frame[2]
            exc_name = MODBUS_EXCEPTION_NAMES.get(exc_code, "未知")
            result += f"异常码: {exc_code} ({exc_name})"
    elif func in (0x03, 0x04):
        # Read registers response
        if len(frame) >= 3:
            byte_count = frame[2]
            result += f"字节数: {byte_count}\n"
            if len(frame) >= 3 + byte_count:
                result += "数据: "
                for i in range(0, byte_count, 2):
                    if i + 1 < byte_count:
                        val = (frame[3 + i] << 8) | frame[3 + i + 1]
                        result += f"[{i // 2}]={val} "
    elif func in (0x01, 0x02):
        # Read coils/discrete inputs response
        if len(frame) >= 3:
            byte_count = frame[2]
            result += f"字节数: {byte_count}\n数据: "
            for i in range(byte_count):
                if 3 + i < len(frame):
                    result += f"0x{frame[3 + i]:02X} "

    # Verify CRC
    if len(frame) >= 4:
        data_part = frame[:-2]
        calc_crc = calc_crc16_modbus(data_part)
        frame_crc = frame[-2] | (frame[-1] << 8)
        crc_ok = calc_crc == frame_crc
        result += f"\nCRC: 0x{frame_crc:04X} {'(校验通过)' if crc_ok else '(校验失败!)'}"

    return result
