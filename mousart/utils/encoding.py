"""Encoding conversion utilities."""
import codecs


def auto_decode(data: bytes) -> str:
    """Auto-detect encoding and decode bytes to string.

    Detection order:
    1. BOM markers (UTF-8, UTF-16 LE, UTF-16 BE)
    2. UTF-8 strict mode
    3. GBK heuristic (>30% of bytes match GBK byte-pair pattern)
    4. UTF-8 with errors="replace" as fallback
    """
    if not data:
        return ""

    # 1. Check for BOM markers
    if data[:3] == b'\xef\xbb\xbf':
        return data[3:].decode("utf-8", errors="replace")
    if data[:2] == b'\xff\xfe':
        return data[2:].decode("utf-16-le", errors="replace")
    if data[:2] == b'\xfe\xff':
        return data[2:].decode("utf-16-be", errors="replace")

    # 2. Try UTF-8 strict mode
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        pass

    # 3. Heuristic: check for GBK byte-pair pattern
    #    GBK first byte: 0x81-0xFE, second byte: 0x40-0xFE (excluding 0x7F)
    if len(data) >= 2:
        gbk_pairs = 0
        total_pairs = 0
        i = 0
        while i < len(data) - 1:
            b1 = data[i]
            b2 = data[i + 1]
            if 0x81 <= b1 <= 0xFE and 0x40 <= b2 <= 0xFE and b2 != 0x7F:
                gbk_pairs += 1
                i += 2
            else:
                i += 1
            total_pairs += 1

        if total_pairs > 0 and (gbk_pairs / total_pairs) > 0.30:
            try:
                return data.decode("gbk")
            except (UnicodeDecodeError, LookupError):
                pass

    # 4. Fallback: UTF-8 with replacement
    return data.decode("utf-8", errors="replace")


def decode_data(data: bytes, encoding: str = "UTF-8") -> str:
    """Decode bytes to string using the specified encoding."""
    if encoding in ("Auto", "自动", "自动 Auto"):
        return auto_decode(data)

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
