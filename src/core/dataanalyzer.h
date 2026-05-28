#ifndef DATAANALYZER_H
#define DATAANALYZER_H

#include <QObject>
#include <QByteArray>

class DataAnalyzer : public QObject
{
    Q_OBJECT

public:
    explicit DataAnalyzer(QObject *parent = nullptr);

    // Hex conversion
    Q_INVOKABLE QString bytesToHex(const QByteArray &data, const QString &separator = " ") const;
    Q_INVOKABLE QByteArray hexToBytes(const QString &hex) const;
    Q_INVOKABLE QString hexToFormattedDisplay(const QByteArray &data) const; // HEX + ASCII side by side

    // Encoding conversion
    Q_INVOKABLE QString convertEncoding(const QByteArray &data, const QString &fromEncoding, const QString &toEncoding) const;
    Q_INVOKABLE QByteArray encodeString(const QString &text, const QString &encoding) const;
    Q_INVOKABLE QString decodeBytes(const QByteArray &data, const QString &encoding) const;

    // Checksum calculation
    Q_INVOKABLE quint8 calcSum8(const QByteArray &data) const;
    Q_INVOKABLE quint8 calcXor8(const QByteArray &data) const;
    Q_INVOKABLE quint16 calcCRC16Modbus(const QByteArray &data) const;
    Q_INVOKABLE quint32 calcCRC32(const QByteArray &data) const;

    // Number conversion
    Q_INVOKABLE QString toBinary(const QString &hexOrDec) const;
    Q_INVOKABLE QString toDecimal(const QString &hexOrBin) const;
    Q_INVOKABLE QString toHex(const QString &decOrBin) const;

    // String utilities
    Q_INVOKABLE QString escapeString(const QString &text) const;
    Q_INVOKABLE QString unescapeString(const QString &text) const;
    Q_INVOKABLE QString textToHex(const QString &text) const;
    Q_INVOKABLE QString hexToText(const QString &hex) const;

    // Modbus frame builder
    Q_INVOKABLE QByteArray buildModbusRtuFrame(quint8 slaveAddr, quint8 funcCode, quint16 startAddr, quint16 quantity) const;
    Q_INVOKABLE QString parseModbusRtuFrame(const QByteArray &frame) const;

    // Data filtering
    Q_INVOKABLE bool matchFilter(const QString &data, const QString &filter, bool useRegex) const;

signals:
    void errorOccurred(const QString &error);

private:
    static const quint16 crc16Table[256];
    static bool crc16TableInitialized;
    static void initCRC16Table();
};

#endif // DATAANALYZER_H
