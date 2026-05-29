# MOUSART
## Herramienta de depuracion serial completa

<div align="center">

**[简体中文](README.md)** | **[English](README.en.md)** | **[繁體中文](README.zh-TW.md)** | **[日本語](README.ja.md)** | **[한국어](README.ko.md)** | **[Deutsch](README.de.md)** | **[Français](README.fr.md)** | **[Русский](README.ru.md)**

</div>

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows-blue)](https://github.com/kryntx/MOUSART/releases)
[![Release](https://img.shields.io/badge/version-3.0.0-brightgreen)](https://github.com/kryntx/MOUSART/releases/tag/v3.0.0)

**MOUSART** es una herramienta de depuracion serial completa disenada para desarrollo embebido, depuracion de hardware y escenarios de comunicacion serial. Soporta dos modos independientes: depuracion serial y puerto serial virtual, con decenas de funciones profesionales como respuesta automatica, soporte de protocolo Modbus, comandos rapidos, grabacion y exportacion de datos, control de pines y soporte de codificacion multiple.

---

## Capturas de pantalla

### Modo depuracion serial

<div align="center">
  <img src="img/d1.png" width="800" alt="Interfaz de depuracion serial MOUSART">
  <br>
  <em>Modo depuracion serial - Conexion al puerto serial de hardware para envio y recepcion de datos</em>
</div>

### Modo puerto serial virtual

<div align="center">
  <img src="img/v1.png" width="800" alt="Interfaz de puerto serial virtual MOUSART">
  <br>
  <em>Modo puerto serial virtual - Creacion de un par de puertos seriales virtuales para programas externos</em>
</div>

---

## Caracteristicas

### Modo depuracion serial
- Actualizacion automatica de la lista de puertos seriales disponibles (sondeo cada 2 segundos)
- Soporte para adaptadores USB-serial, Bluetooth serial, etc.
- Baudrate: 300 ~ 921600 valores predefinidos + valores personalizados (1-9999999)
- Bits de datos: 5, 6, 7, 8 / Bits de parada: 1, 1.5, 2
- Paridad: None, Even, Odd, Mark, Space
- Control de flujo: Ninguno / Hardware (RTS/CTS) / Software (XON/XOFF)
- Control manual DTR/RTS
- Monitoreo en tiempo real de niveles de pines CTS/DSR/DCD/RI
- Respuesta automatica (coincidencia de palabras clave + configuracion de retardo)

### Modo puerto serial virtual (solo Linux)
- Creacion con un clic de un par de puertos seriales virtuales basada en `socat`
- Los programas externos se conectan a traves de `/tmp/mousart_vport`
- Zonas de envio/recepcion independientes y estadisticas

### Envio y recepcion de datos
- Cambio de modo de envio Texto / HEX
- Soporte de codificacion multiple: UTF-8, GBK, GB18030, Latin-1, ASCII
- Control de salto de linea al enviar (interruptores independientes CR / LF)
- Envio temporizado (1ms ~ 3600000ms)
- Envio de archivo
- Constructor de tramas Modbus RTU (CRC automatico)
- Barra de comandos rapidos (clic izquierdo enviar, clic derecho editar)
- Atajo de teclado Ctrl+Enter para enviar

### Analisis de datos
- Calculo de sumas de verificacion: Sum8 / XOR8 / CRC16-Modbus / CRC32
- Conversion binario / decimal / hexadecimal
- Conversion Texto <-> Hex en tiempo real
- Filtrado por palabra clave / expresion regular

### Grabacion de datos
- Guardado con un clic de registros en TXT / CSV
- Grabacion automatica (division automatica a 10 MB/archivo)
- Contador de bytes RX/TX en tiempo real y visualizacion de tasa

### Interfaz
- Tema dual oscuro/claro
- Escalado de fuente 0.8x-1.5x
- Gestion de perfiles

---

## Guia de instalacion

### Linux (Debian/Ubuntu)

#### Metodo 1: Instalacion del paquete deb (recomendado)

```bash
# 1. Descargar el paquete deb
wget https://github.com/kryntx/MOUSART/releases/download/v3.0.0/mouserial_3.0.0-1_amd64.deb

# 2. Instalar (las dependencias se instalan automaticamente)
sudo apt install ./mouserial_3.0.0-1_amd64.deb

# 3. Ejecutar
mousart
```

#### Metodo 2: Ejecutar desde el codigo fuente

```bash
# 1. Instalar dependencias del sistema
sudo apt update
sudo apt install python3-pyqt5 python3-serial socat git

# 2. Clonar el proyecto
git clone https://github.com/kryntx/MOUSART.git
cd MOUSART

# 3. Ejecutar
python3 -m mousart
```

#### Metodo 3: Instalar dependencias con pip y ejecutar

```bash
# 1. Instalar dependencias del sistema
sudo apt install socat

# 2. Instalar dependencias de Python
pip3 install PyQt5 pyserial

# 3. Clonar y ejecutar
git clone https://github.com/kryntx/MOUSART.git
cd MOUSART
python3 -m mousart
```

### Windows

#### Metodo 1: Ejecutar desde el codigo fuente

```bash
# 1. Instalar Python 3.10+ (descargar desde python.org)

# 2. Instalar dependencias
pip install PyQt5 pyserial

# 3. Clonar el proyecto y ejecutar
git clone https://github.com/kryntx/MOUSART.git
cd MOUSART
python -m mousart
```

#### Metodo 2: Crear un EXE

```bash
# 1. Instalar dependencias
pip install PyQt5 pyserial pyinstaller

# 2. Construir
pyinstaller pyinstaller.spec --noconfirm

# 3. Ejecutar el dist/MOUSART.exe generado
```

---

## Guia de desinstalacion

### Desinstalacion del paquete deb de Linux

```bash
# Metodo 1: Desinstalar con apt
sudo apt remove mouserial

# Metodo 2: Desinstalacion completa (incluyendo archivos de configuracion)
sudo apt purge mouserial

# Limpiar configuracion de usuario (opcional)
rm -rf ~/.mousart
rm -rf ~/mousart_logs
```

### Desinstalacion de la instalacion desde codigo fuente de Linux

```bash
# Eliminar el directorio del proyecto
rm -rf /path/to/MOUSART

# Limpiar configuracion de usuario (opcional)
rm -rf ~/.mousart
rm -rf ~/mousart_logs
```

### Desinstalacion de Windows

```
# Eliminar el directorio del proyecto

# Limpiar configuracion de usuario (opcional)
# Eliminar el directorio %USERPROFILE%\.mousart
# Eliminar el directorio %USERPROFILE%\mousart_logs
```

---

## Guia de uso

### Modo depuracion serial
1. En el panel izquierdo, seleccione el modo **"Depuracion serial"**
2. Seleccione el puerto serial de la lista desplegable
3. Configure los parametros del puerto serial (baudrate, bits de datos, bits de parada, paridad, control de flujo)
4. Haga clic en **"Abrir"** para establecer la conexion
5. Ingrese datos en el area de envio a la derecha y haga clic en **"Enviar"** o presione `Ctrl+Enter`
6. El area de recepcion muestra los datos recibidos en tiempo real

### Modo puerto serial virtual (solo Linux)
1. En el panel izquierdo, seleccione el modo **"Puerto serial de simulacion"**
2. Haga clic en **"Iniciar"** para crear el par de puertos seriales virtuales
3. La interfaz muestra la ruta del puerto externo `/tmp/mousart_vport`
4. Conectese a esta ruta con cualquier herramienta serial
5. Ingrese datos en el area de envio y envie

### Comandos rapidos
1. Haga clic en **"+"** en la barra de comandos rapidos en la parte inferior para agregar un nuevo comando
2. Ingrese el nombre y los datos (soporta texto y HEX)
3. Clic izquierdo en el boton del comando para enviar inmediatamente
4. Clic derecho en el boton del comando para editar o eliminar

### Respuesta automatica (Modo depuracion serial)
1. Encuentre el area de **"Respuesta automatica"** en el panel izquierdo
2. Active el interruptor y configure la palabra clave de coincidencia y los datos de respuesta
3. Opcionalmente puede configurar el retardo de respuesta (milisegundos)

### Construccion de trama Modbus
1. Haga clic en el boton **"Modbus"** en la barra de herramientas de envio
2. Configure la direccion del esclavo, el codigo de funcion, la direccion de inicio y la cantidad
3. Haga clic en **"Construir"** para generar automaticamente una trama Modbus RTU con CRC

### Grabacion y exportacion de registros
1. Haga clic en el boton **"Grabar"** en la barra de herramientas del area de recepcion para iniciar la grabacion automatica
2. Todos los datos enviados y recibidos se guardan automaticamente en `~/mousart_logs/`
3. Haga clic en **"Guardar"** para exportar manualmente como TXT o CSV

### Control de pines (Modo depuracion serial)
1. Despues de abrir el puerto serial, la barra de control de pines se muestra en el panel izquierdo
2. Haga clic en los botones DTR/RTS para cambiar el nivel de los pines
3. Los indicadores de estado CTS/DSR/DCD/RI se muestran en tiempo real

---

## Preguntas frecuentes

**Q: No se puede abrir el puerto serial?**
A: Generalmente es un problema de permisos. Agregue el usuario al grupo `dialout`:
```bash
sudo usermod -aG dialout $USER
# Cierre sesion y vuelva a iniciarla para que surta efecto
```

**Q: El puerto serial virtual no funciona?**
A: Asegurese de que `socat` este instalado:
```bash
sudo apt install socat
```

**Q: Los caracteres chinos se muestran incorrectamente?**
A: Seleccione la codificacion de recepcion correcta en el panel izquierdo (por ejemplo, GBK).

**Q: Como envio un comando Modbus?**
A: Haga clic en el boton **"Modbus"**, complete los parametros y haga clic en **"Construir"**. Los datos de la trama se rellenaran automaticamente en el area de envio.

**Q: Donde se guardan los archivos de grabacion automatica?**
A: Por defecto en `~/mousart_logs/`, el formato del nombre de archivo es `mousart_rec_YYYYMMDD_HHmmss.log`.

---

## Licencia

Este proyecto utiliza la **licencia MIT** - consulte [LICENSE](LICENSE) para mas detalles.

**MOUSART** - Hacer la depuracion serial mas simple y eficiente!
