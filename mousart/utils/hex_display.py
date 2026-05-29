"""HEX + ASCII side-by-side display formatter."""


def hex_to_formatted_display(data: bytes) -> str:
    """Format bytes as HEX + ASCII side-by-side display.

    Format: 00000000  48 65 6C 6C 6F 20 57 6F  72 6C 64 21 0A          |Hello World!.|
    """
    lines = []
    for offset in range(0, len(data), 16):
        # Address
        line = f"{offset:08X}  "

        # Hex bytes
        ascii_chars = []
        for i in range(16):
            if offset + i < len(data):
                byte = data[offset + i]
                line += f"{byte:02X} "
                ascii_chars.append(chr(byte) if 0x20 <= byte <= 0x7E else ".")
            else:
                line += "   "
                ascii_chars.append(" ")
            if i == 7:
                line += " "

        ascii_str = "".join(ascii_chars)
        line += f" |{ascii_str}|"
        lines.append(line)

    return "\n".join(lines)


def bytes_to_hex(data: bytes, separator: str = " ") -> str:
    """Convert bytes to hex string with separator."""
    return separator.join(f"{b:02X}" for b in data)


def hex_to_bytes(hex_str: str) -> bytes:
    """Convert hex string to bytes, ignoring spaces and newlines."""
    cleaned = hex_str.replace(" ", "").replace("\n", "").replace("\r", "").replace("\t", "")
    try:
        return bytes.fromhex(cleaned)
    except ValueError:
        return b""
