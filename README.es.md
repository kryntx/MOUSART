# MOUSART
## Depurador de puerto serie completo

<div align="center">

**[简体中文](README.md)** | **[English](README.en.md)** | **[繁體中文](README.zh-TW.md)** | **[日本語](README.ja.md)** | **[한국어](README.ko.md)** | **[Deutsch](README.de.md)** | **[Français](README.fr.md)** | **Español** | **[Русский](README.ru.md)**

</div>

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows-blue)](https://github.com/kryntx/MOUSART/releases)
[![Release](https://img.shields.io/badge/version-3.0.0-brightgreen)](https://github.com/kryntx/MOUSART/releases/tag/v3.0.0)
[![Toolchain](https://img.shields.io/badge/toolchain-PyQt6%20%7C%20Python-green)](https://www.riverbankcomputing.com/software/pyqt/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)

**MOUSART** es un depurador de puerto serie completo construido con Python/PyQt6, diseñado para desarrollo embebido, depuración de hardware y comunicación serie. La versión 3.0 es una reescritura completa en Python que añade respuesta automática, soporte del protocolo Modbus, comandos rápidos, grabación y exportación de datos, control de pines, soporte multi-codificación y docenas de funciones profesionales.

---

## Resumen de funciones

### 1. Gestión de conexiones
- Actualización automática de puertos disponibles (intervalo 2s)
- Puerto serie virtual, USB-a-serie, Bluetooth
- Velocidad: 300–921600 preajustes + personalizado (1-9999999)
- Bits de datos: 5, 6, 7, 8 / Bits de parada: 1, 1.5, 2
- Paridad: None, Even, Odd, Mark, Space
- Control de flujo: Ninguno / Hardware (RTS/CTS) / Software (XON/XOFF)
- Control manual DTR/RTS / Monitoreo CTS/DSR/DCD/RI

### 2. Recepción de datos
- Modo texto (UTF-8 / GBK / GB18030 / Latin-1 / ASCII)
- Modo hexadecimal (HEX)
- Marca de tiempo (precisión de milisegundos)
- Indicador de dirección (`<<` RX / `>>` TX / `!!` ERR)
- Pausar visualización (recepción en segundo plano)
- Filtro por palabra clave (texto / regex)
- Límite de registro: 2000 entradas

### 3. Envío de datos
- Modo envío Texto / HEX
- Control de salto de línea (CR / LF independiente)
- Envío temporizado (1ms–3600000ms, con límite de contador)
- Envío de archivo
- Constructor de trama Modbus RTU (CRC automático)
- Barra de comandos rápidos (agregar/editar/eliminar, persistente)
- Secuencia/cola de envío (soporte de bucle)

### 4. Respuesta automática
- Respuesta automática al recibir palabra clave específica
- Retraso de respuesta configurable (ms)
- Activación/desactivación con un clic

### 5. Codificación y conversión
- Conversión Texto ↔ Hex
- Multi-codificación: UTF-8, GBK, GB18030, Latin-1, ASCII
- Sumas de verificación: Sum8 / XOR8 / CRC16-Modbus / CRC32
- Constructor y analizador de trama Modbus RTU
- Conversión binario / decimal / hexadecimal

### 6. Grabación y exportación
- Guardar registro en TXT / CSV
- Grabación automática (archivo de 10MB)
- Contador de bytes RX/TX en tiempo real

### 7. Puerto serie virtual (solo Linux)
- Creación de puerto virtual con `socat`
- Conexión externa vía `/tmp/mousart_vport`

### 8. Interfaz y configuración
- Tema oscuro / claro
- Escalado de fuente 0.8x–1.5x
- Gestión de perfiles (múltiples configuraciones)

---

---

## Inicio rápido

### Binarios precompilados

Descargar de [GitHub Releases](https://github.com/kryntx/MOUSART/releases):

| Plataforma | Archivo | Tamaño |
|------------|---------|--------|
| **Linux x86_64 (deb)** | `mouserial_3.0.0-1_amd64.deb` | ~82KB |
| **Windows x86_64** | `MOUSART-v3.0.0-windows-x86_64.exe` | ~23MB |

#### Instalación Debian/Ubuntu (Recomendado)
```bash
# Descargar e instalar el paquet deb (las dependencias se manejan automáticamente)
wget https://github.com/kryntx/MOUSART/releases/download/v3.0.0/mouserial_3.0.0-1_amd64.deb
sudo apt install ./mouserial_3.0.0-1_amd64.deb
```

### Compilar desde código fuente

```bash
# Ubuntu/Debian dependencias
sudo apt install python3-pyqt6 python3-serial socat

git clone https://github.com/kryntx/MOUSART.git
cd MOUSART

# Instalar dependencias Python
pip3 install PyQt6 pyserial

# Ejecutar
python3 -m mousart
```

#### Construir EXE para Windows

```bash
pip3 install pyinstaller
pyinstaller pyinstaller.spec --noconfirm
# Salida: dist/MOUSART.exe
```

#### Construir paquete Debian

```bash
sudo apt install dh-python python3-setuptools debhelper
dpkg-buildpackage -us -uc -b
```

---

## Uso

### Modo puerto serie virtual
1. Seleccionar modo **"Virtual"** en el panel izquierdo
2. Hacer clic en **"Start"**
3. Se muestra la ruta del puerto `/tmp/mousart_vport`
4. Conectar cualquier herramienta serie a esta ruta

### Modo depuración serie hardware
1. Seleccionar modo **"Debug"**
2. Elegir puerto y configurar parámetros
3. Hacer clic en **"Open"** para conectar
4. Escribir en el área de envío y hacer clic **"Enviar"** o `Ctrl+Enter`

### Comandos rápidos
1. Hacer clic en **"+"** en la barra de comandos rápidos
2. Ingresar nombre y datos
3. Clic izquierdo para enviar, clic derecho para editar

### Respuesta automática
1. Sección **"Auto Reply"** en el panel izquierdo
2. Activar el toggle, establecer palabra clave y datos de respuesta

### Constructor Modbus
1. Hacer clic en **"Modbus"** en la barra de herramientas
2. Establecer dirección esclavo, código de función, dirección inicial, cantidad
3. Hacer clic en **"Construir"** para generar trama con CRC

---

## Parámetros serie

| Parámetro | Valores |
|-----------|---------|
| **Velocidad** | 300–921600 + personalizado (1-9999999) |
| **Bits de datos** | 5, 6, 7, 8 |
| **Bits de parada** | 1, 1.5, 2 |
| **Paridad** | None, Odd, Even, Mark, Space |
| **Control de flujo** | None, Hardware, Software |
| **Codificación recepción** | UTF-8, GBK, GB18030, Latin-1, ASCII |

---

## Registro de cambios

### v3.0.0 (2026-05-29)
**Reescritura completa - Versión Python/PyQt6**

- Reescritura completa en Python, migración de C++/Qt5/QML a Python/PyQt6
- Estructura de código más sencilla, más fácil de mantener y ampliar
- Todas las funciones de v2.0.0 completamente conservadas
- Soporte multiplataforma optimizado (Windows EXE + Linux deb)
- Nuevo diseño de icono de aplicación

### v2.0.0 (2026-05-29)
Control de pines, respuesta automática, comandos rápidos, multi-codificación, Modbus RTU, exportación de registro, estadísticas RX/TX, filtrado de datos, gestión de perfiles, herramientas de suma de verificación, secuencia de envío

### v1.0.0 (2026-05-27)
Versión inicial

---

## FAQ

**Q: ¿No se puede abrir el puerto?** Problema de permisos. Use `sudo python3 -m mousart` o añada el usuario al grupo `dialout`.

**Q: ¿El puerto virtual no funciona?** Instale `socat`: `sudo apt install socat`

---

## Licencia

**Licencia MIT** - ver [LICENSE](LICENSE).

**MOUSART** - ¡Haciendo la depuración serie más simple y eficiente!
