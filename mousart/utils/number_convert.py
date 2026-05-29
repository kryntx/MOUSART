"""Number base conversion utilities."""


def to_binary(hex_or_dec: str) -> str:
    """Convert hex or decimal string to binary representation."""
    try:
        if hex_or_dec.startswith(("0x", "0X")):
            value = int(hex_or_dec, 16)
        else:
            value = int(hex_or_dec, 10)
    except ValueError:
        return ""

    bin_str = bin(value)[2:]
    # Pad to multiple of 8
    while len(bin_str) % 8 != 0:
        bin_str = "0" + bin_str
    # Add spaces every 8 bits
    parts = [bin_str[i:i + 8] for i in range(0, len(bin_str), 8)]
    return " ".join(parts)


def to_decimal(hex_or_bin: str) -> str:
    """Convert hex or binary string to decimal representation."""
    try:
        text = hex_or_bin.strip()
        if text.startswith(("0x", "0X")):
            return str(int(text, 16))
        # Check if binary
        cleaned = text.replace(" ", "")
        if cleaned and all(c in "01" for c in cleaned):
            return str(int(cleaned, 2))
        return str(int(text, 10))
    except ValueError:
        return ""


def to_hex(dec_or_bin: str) -> str:
    """Convert decimal or binary string to hex representation."""
    try:
        text = dec_or_bin.strip()
        # Check if binary
        cleaned = text.replace(" ", "")
        if cleaned and all(c in "01" for c in cleaned) and len(cleaned) > 1:
            value = int(cleaned, 2)
        else:
            value = int(text, 10)
        return f"0x{value:X}"
    except ValueError:
        return ""
