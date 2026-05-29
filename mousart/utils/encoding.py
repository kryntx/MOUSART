"""Encoding conversion utilities."""
import codecs


def decode_data(data: bytes, encoding: str = "UTF-8") -> str:
    """Decode bytes to string using the specified encoding."""
    if encoding == "ASCII":
        result = []
        for b in data:
            if 0x20 <= b <= 0x7E:
                result.append(chr(b))
            else:
                result.append(f"\\x{b:02x}")
        return "".join(result)

    try:
        if encoding in ("UTF-8", "utf-8"):
            return data.decode("utf-8", errors="replace")
        codec = codecs.lookup(encoding)
        return codec.decode(data)[0]
    except (LookupError, UnicodeDecodeError):
        return data.decode("utf-8", errors="replace")


def encode_string(text: str, encoding: str = "UTF-8") -> bytes:
    """Encode string to bytes using the specified encoding."""
    if encoding == "ASCII":
        result = bytearray()
        for ch in text:
            cp = ord(ch)
            if 0x20 <= cp <= 0x7E:
                result.append(cp)
            else:
                result.extend(ch.encode("ascii", errors="replace"))
        return bytes(result)

    try:
        if encoding in ("UTF-8", "utf-8"):
            return text.encode("utf-8")
        codec = codecs.lookup(encoding)
        return codec.encode(text)[0]
    except (LookupError, UnicodeEncodeError):
        return text.encode("utf-8")
