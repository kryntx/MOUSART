#include "dataanalyzer.h"
#include <QTextCodec>
#include <QRegularExpression>

const quint16 DataAnalyzer::crc16Table[256] = {
    0x0000, 0xC0C1, 0xC181, 0x0140, 0xC301, 0x03C0, 0x0280, 0xC241,
    0xC601, 0x06C0, 0x0780, 0xC741, 0x0500, 0xC5C1, 0xC481, 0x0440,
    0xCC01, 0x0CC0, 0x0D80, 0xCD41, 0x0F00, 0xCFC1, 0xCE81, 0x0E40,
    0x0A00, 0xCAC1, 0xCB81, 0x0B40, 0xC901, 0x09C0, 0x0880, 0xC841,
    0xD801, 0x18C0, 0x1980, 0xD941, 0x1B00, 0xDBC1, 0xDA81, 0x1A40,
    0x1E00, 0xDEC1, 0xDF81, 0x1F40, 0xDD01, 0x1DC0, 0x1C80, 0xDC41,
    0x1400, 0xD4C1, 0xD581, 0x1540, 0xD701, 0x17C0, 0x1680, 0xD641,
    0xD201, 0x12C0, 0x1380, 0xD341, 0x1100, 0xD1C1, 0xD081, 0x1040,
    0xF001, 0x30C0, 0x3180, 0xF141, 0x3300, 0xF3C1, 0xF281, 0x3240,
    0x3600, 0xF6C1, 0xF781, 0x3740, 0xF501, 0x35C0, 0x3480, 0xF441,
    0x3C00, 0xFCC1, 0xFD81, 0x3D40, 0xFF01, 0x3FC0, 0x3E80, 0xFE41,
    0xFA01, 0x3AC0, 0x3B80, 0xFB41, 0x3900, 0xF9C1, 0xF881, 0x3840,
    0x2800, 0xE8C1, 0xE981, 0x2940, 0xEB01, 0x2BC0, 0x2A80, 0xEA41,
    0xEE01, 0x2EC0, 0x2F80, 0xEF41, 0x2D00, 0xEDC1, 0xEC81, 0x2C40,
    0xE401, 0x24C0, 0x2580, 0xE541, 0x2700, 0xE7C1, 0xE681, 0x2640,
    0x2200, 0xE2C1, 0xE381, 0x2340, 0xE101, 0x21C0, 0x2080, 0xE041,
    0xA001, 0x60C0, 0x6180, 0xA141, 0x6300, 0xA3C1, 0xA281, 0x6240,
    0x6600, 0xA6C1, 0xA781, 0x6740, 0xA501, 0x65C0, 0x6480, 0xA441,
    0x6C00, 0xACC1, 0xAD81, 0x6D40, 0xAF01, 0x6FC0, 0x6E80, 0xAE41,
    0xAA01, 0x6AC0, 0x6B80, 0xAB41, 0x6900, 0xA9C1, 0xA881, 0x6840,
    0x7800, 0xB8C1, 0xB981, 0x7940, 0xBB01, 0x7BC0, 0x7A80, 0xBA41,
    0xBE01, 0x7EC0, 0x7F80, 0xBF41, 0x7D00, 0xBDC1, 0xBC81, 0x7C40,
    0xB401, 0x74C0, 0x7580, 0xB541, 0x7700, 0xB7C1, 0xB681, 0x7640,
    0x7200, 0xB2C1, 0xB381, 0x7340, 0xB101, 0x71C0, 0x7080, 0xB041,
    0x5000, 0x90C1, 0x9181, 0x5140, 0x9301, 0x53C0, 0x5280, 0x9241,
    0x9601, 0x56C0, 0x5780, 0x9741, 0x5500, 0x95C1, 0x9481, 0x5440,
    0x9C01, 0x5CC0, 0x5D80, 0x9D41, 0x5F00, 0x9FC1, 0x9E81, 0x5E40,
    0x5A00, 0x9AC1, 0x9B81, 0x5B40, 0x9901, 0x59C0, 0x5880, 0x9841,
    0x8801, 0x48C0, 0x4980, 0x8941, 0x4B00, 0x8BC1, 0x8A81, 0x4A40,
    0x4E00, 0x8EC1, 0x8F81, 0x4F40, 0x8D01, 0x4DC0, 0x4C80, 0x8C41,
    0x4400, 0x84C1, 0x8581, 0x4540, 0x8701, 0x47C0, 0x4680, 0x8641,
    0x8201, 0x42C0, 0x4380, 0x8341, 0x4100, 0x81C1, 0x8081, 0x4040
};

DataAnalyzer::DataAnalyzer(QObject *parent)
    : QObject(parent)
{
}

QString DataAnalyzer::bytesToHex(const QByteArray &data, const QString &separator) const
{
    QString result;
    for (int i = 0; i < data.size(); i++) {
        if (i > 0) result += separator;
        result += QString("%1").arg((quint8)data[i], 2, 16, QChar('0')).toUpper();
    }
    return result;
}

QByteArray DataAnalyzer::hexToBytes(const QString &hex) const
{
    QString cleaned = hex;
    cleaned.remove(' ').remove('\n').remove('\r').remove('\t');
    return QByteArray::fromHex(cleaned.toUtf8());
}

QString DataAnalyzer::hexToFormattedDisplay(const QByteArray &data) const
{
    // HEX + ASCII side by side display
    // Format: 00000000  48 65 6C 6C 6F 20 57 6F  72 6C 64 21 0A          |Hello World!.|
    QString result;
    for (int offset = 0; offset < data.size(); offset += 16) {
        // Address
        result += QString("%1  ").arg(offset, 8, 16, QChar('0')).toUpper();

        // Hex bytes
        QString ascii;
        for (int i = 0; i < 16; i++) {
            if (offset + i < data.size()) {
                quint8 byte = (quint8)data[offset + i];
                result += QString("%1 ").arg(byte, 2, 16, QChar('0')).toUpper();
                ascii += (byte >= 0x20 && byte <= 0x7E) ? QChar(byte) : QChar('.');
            } else {
                result += "   ";
                ascii += " ";
            }
            if (i == 7) result += " ";
        }
        result += " |" + ascii + "|\n";
    }
    return result;
}

QString DataAnalyzer::convertEncoding(const QByteArray &data, const QString &fromEncoding, const QString &toEncoding) const
{
    QTextCodec *fromCodec = QTextCodec::codecForName(fromEncoding.toUtf8());
    if (!fromCodec) return QString();

    QString unicode = fromCodec->toUnicode(data);

    if (toEncoding == "UTF-8" || toEncoding == "Unicode") {
        return unicode;
    }

    QTextCodec *toCodec = QTextCodec::codecForName(toEncoding.toUtf8());
    if (!toCodec) return unicode;

    QByteArray encoded = toCodec->fromUnicode(unicode);
    return QString::fromUtf8(encoded.toHex(' '));
}

QByteArray DataAnalyzer::encodeString(const QString &text, const QString &encoding) const
{
    if (encoding == "UTF-8") return text.toUtf8();
    if (encoding == "Latin-1") return text.toLatin1();

    QTextCodec *codec = QTextCodec::codecForName(encoding.toUtf8());
    if (codec) return codec->fromUnicode(text);
    return text.toUtf8();
}

QString DataAnalyzer::decodeBytes(const QByteArray &data, const QString &encoding) const
{
    if (encoding == "UTF-8") return QString::fromUtf8(data);
    if (encoding == "Latin-1") return QString::fromLatin1(data);
    if (encoding == "ASCII") {
        QString result;
        for (char c : data) {
            if (c >= 0x20 && c <= 0x7E) result += QChar(c);
            else result += QString("\\x%1").arg((quint8)c, 2, 16, QChar('0'));
        }
        return result;
    }

    QTextCodec *codec = QTextCodec::codecForName(encoding.toUtf8());
    if (codec) return codec->toUnicode(data);
    return QString::fromUtf8(data);
}

quint8 DataAnalyzer::calcSum8(const QByteArray &data) const
{
    quint8 sum = 0;
    for (char c : data) sum += (quint8)c;
    return sum;
}

quint8 DataAnalyzer::calcXor8(const QByteArray &data) const
{
    quint8 x = 0;
    for (char c : data) x ^= (quint8)c;
    return x;
}

quint16 DataAnalyzer::calcCRC16Modbus(const QByteArray &data) const
{
    quint16 crc = 0xFFFF;
    for (int i = 0; i < data.size(); i++) {
        crc = (crc >> 8) ^ crc16Table[(crc ^ (quint8)data[i]) & 0xFF];
    }
    return crc;
}

quint32 DataAnalyzer::calcCRC32(const QByteArray &data) const
{
    quint32 crc = 0xFFFFFFFF;
    for (int i = 0; i < data.size(); i++) {
        crc ^= (quint8)data[i];
        for (int j = 0; j < 8; j++) {
            if (crc & 1) crc = (crc >> 1) ^ 0xEDB88320;
            else crc >>= 1;
        }
    }
    return crc ^ 0xFFFFFFFF;
}

QString DataAnalyzer::toBinary(const QString &hexOrDec) const
{
    bool ok;
    quint64 value;
    if (hexOrDec.startsWith("0x") || hexOrDec.startsWith("0X")) {
        value = hexOrDec.toULongLong(&ok, 16);
    } else {
        value = hexOrDec.toULongLong(&ok, 10);
    }
    if (!ok) return "";

    QString bin = QString::number(value, 2);
    // Pad to multiple of 8
    while (bin.length() % 8 != 0) bin.prepend("0");
    // Add spaces every 8 bits
    QString result;
    for (int i = 0; i < bin.length(); i++) {
        if (i > 0 && i % 8 == 0) result += " ";
        result += bin[i];
    }
    return result;
}

QString DataAnalyzer::toDecimal(const QString &hexOrBin) const
{
    bool ok;
    quint64 value;
    if (hexOrBin.startsWith("0x") || hexOrBin.startsWith("0X")) {
        value = hexOrBin.toULongLong(&ok, 16);
    } else if (hexOrBin.contains(" ") || hexOrBin.length() > 1) {
        // Try binary
        QString bin = hexOrBin;
        bin.remove(" ");
        bool allBinary = true;
        for (QChar c : bin) {
            if (c != '0' && c != '1') { allBinary = false; break; }
        }
        if (allBinary && !bin.isEmpty()) {
            value = bin.toULongLong(&ok, 2);
        } else {
            value = hexOrBin.toULongLong(&ok, 10);
        }
    } else {
        value = hexOrBin.toULongLong(&ok, 10);
    }
    if (!ok) return "";
    return QString::number(value);
}

QString DataAnalyzer::toHex(const QString &decOrBin) const
{
    bool ok;
    quint64 value;
    if (decOrBin.contains(" ") || (decOrBin.length() > 1 && !decOrBin.contains(QRegularExpression("[89a-fA-F]")))) {
        QString bin = decOrBin;
        bin.remove(" ");
        bool allBinary = true;
        for (QChar c : bin) {
            if (c != '0' && c != '1') { allBinary = false; break; }
        }
        if (allBinary && !bin.isEmpty()) {
            value = bin.toULongLong(&ok, 2);
        } else {
            value = decOrBin.toULongLong(&ok, 10);
        }
    } else {
        value = decOrBin.toULongLong(&ok, 10);
    }
    if (!ok) return "";
    return "0x" + QString::number(value, 16).toUpper();
}

QString DataAnalyzer::escapeString(const QString &text) const
{
    QString result;
    for (int i = 0; i < text.length(); i++) {
        QChar c = text[i];
        if (c == '\\') result += "\\\\";
        else if (c == '\r') result += "\\r";
        else if (c == '\n') result += "\\n";
        else if (c == '\t') result += "\\t";
        else if (c == '\0') result += "\\0";
        else if (c.unicode() < 0x20) result += QString("\\x%1").arg(c.unicode(), 2, 16, QChar('0'));
        else result += c;
    }
    return result;
}

QString DataAnalyzer::unescapeString(const QString &text) const
{
    QString result;
    for (int i = 0; i < text.length(); i++) {
        if (text[i] == '\\' && i + 1 < text.length()) {
            i++;
            switch (text[i].toLatin1()) {
            case 'r': result += '\r'; break;
            case 'n': result += '\n'; break;
            case 't': result += '\t'; break;
            case '0': result += '\0'; break;
            case '\\': result += '\\'; break;
            case 'x': {
                if (i + 2 < text.length()) {
                    QString hex = text.mid(i + 1, 2);
                    bool ok;
                    char byte = hex.toUInt(&ok, 16);
                    if (ok) {
                        result += QChar(byte);
                        i += 2;
                    } else {
                        result += "\\x";
                    }
                } else {
                    result += "\\x";
                }
                break;
            }
            default: result += "\\"; result += text[i]; break;
            }
        } else {
            result += text[i];
        }
    }
    return result;
}

QString DataAnalyzer::textToHex(const QString &text) const
{
    return bytesToHex(text.toUtf8(), " ");
}

QString DataAnalyzer::hexToText(const QString &hex) const
{
    QByteArray bytes = hexToBytes(hex);
    return QString::fromUtf8(bytes);
}

QByteArray DataAnalyzer::buildModbusRtuFrame(quint8 slaveAddr, quint8 funcCode, quint16 startAddr, quint16 quantity) const
{
    QByteArray frame;
    frame.append(static_cast<char>(slaveAddr));
    frame.append(static_cast<char>(funcCode));
    frame.append(static_cast<char>((startAddr >> 8) & 0xFF));
    frame.append(static_cast<char>(startAddr & 0xFF));
    frame.append(static_cast<char>((quantity >> 8) & 0xFF));
    frame.append(static_cast<char>(quantity & 0xFF));

    quint16 crc = calcCRC16Modbus(frame);
    frame.append(static_cast<char>(crc & 0xFF));
    frame.append(static_cast<char>((crc >> 8) & 0xFF));

    return frame;
}

QString DataAnalyzer::parseModbusRtuFrame(const QByteArray &frame) const
{
    if (frame.size() < 4) return "帧长度不足";

    quint8 addr = (quint8)frame[0];
    quint8 func = (quint8)frame[1];

    QString result = QString("地址: %1 (0x%2)\n")
        .arg(addr).arg(addr, 2, 16, QChar('0'));

    QStringList funcNames = {
        "读线圈", "读离散输入", "读保持寄存器", "读输入寄存器",
        "写单个线圈", "写单个寄存器", "读异常状态", "诊断",
        "", "", "获取通信事件计数器", "获取通信事件日志",
        "", "", "", "",
        "写多个线圈", "写多个寄存器", "报告服务器ID", "",
        "读文件记录", "写文件记录", "掩码写寄存器", "读/写多个寄存器",
        "读FIFO队列"
    };

    QString funcName = (func < funcNames.size() && !funcNames[func].isEmpty()) ? funcNames[func] : "未知功能码";
    result += QString("功能码: 0x%1 (%2)\n").arg(func, 2, 16, QChar('0')).arg(funcName);

    if (func & 0x80) {
        // Error response
        if (frame.size() >= 3) {
            quint8 excCode = (quint8)frame[2];
            QStringList excNames = {"", "非法功能码", "非法数据地址", "非法数据值",
                                    "从站设备故障", "确认", "从站设备忙", "否定确认",
                                    "存储奇偶性差错", "", "", "网关路径不可用",
                                    "网关目标设备响应失败"};
            QString excName = (excCode < excNames.size()) ? excNames[excCode] : "未知";
            result += QString("异常码: %1 (%2)").arg(excCode).arg(excName);
        }
    } else {
        if (func == 0x03 || func == 0x04) {
            // Read registers response
            if (frame.size() >= 3) {
                quint8 byteCount = (quint8)frame[2];
                result += QString("字节数: %1\n").arg(byteCount);
                if (frame.size() >= 3 + byteCount) {
                    result += "数据: ";
                    for (int i = 0; i < byteCount; i += 2) {
                        if (i + 1 < byteCount) {
                            quint16 val = ((quint8)frame[3 + i] << 8) | (quint8)frame[3 + i + 1];
                            result += QString("[%1]=%2 ").arg(i / 2).arg(val);
                        }
                    }
                }
            }
        } else if (func == 0x01 || func == 0x02) {
            // Read coils/discrete inputs response
            if (frame.size() >= 3) {
                quint8 byteCount = (quint8)frame[2];
                result += QString("字节数: %1\n数据: ").arg(byteCount);
                for (int i = 0; i < byteCount; i++) {
                    quint8 val = (quint8)frame[3 + i];
                    result += QString("0x%1 ").arg(val, 2, 16, QChar('0'));
                }
            }
        }
    }

    // Verify CRC if frame is long enough
    if (frame.size() >= 4) {
        QByteArray dataPart = frame.left(frame.size() - 2);
        quint16 calcCrc = calcCRC16Modbus(dataPart);
        quint16 frameCrc = (quint8)frame[frame.size() - 2] | ((quint8)frame[frame.size() - 1] << 8);
        result += QString("\nCRC: 0x%1 %2").arg(frameCrc, 4, 16, QChar('0')).arg(calcCrc == frameCrc ? "(校验通过)" : "(校验失败!)");
    }

    return result;
}

bool DataAnalyzer::matchFilter(const QString &data, const QString &filter, bool useRegex) const
{
    if (filter.isEmpty()) return true;
    if (useRegex) {
        QRegularExpression re(filter, QRegularExpression::CaseInsensitiveOption);
        return re.match(data).hasMatch();
    }
    return data.contains(filter, Qt::CaseInsensitive);
}
