# Conexión QR Fotos

**Conexión QR Fotos** es una aplicación en Python que permite visualizar una galería de fotos con un diseño minimalista inspirado en Material You. La aplicación genera automáticamente un código QR en formato PNG para acceder a la galería desde dispositivos móviles y cuenta con una interfaz gráfica (Tkinter) para iniciar y detener el servidor, así como para seleccionar la carpeta de fotos.

## Características

- **Galería de Fotos:** Visualiza imágenes en una cuadrícula uniforme, donde cada imagen se ajusta sin dejar huecos utilizando `object-fit: cover`.
- **Código QR:** Genera un código QR con la URL del servidor (basada en la IP y el puerto configurados) y lo guarda en la misma carpeta donde se encuentra el ejecutable.
- **Servidor Web:** Implementa un servidor HTTP que sirve la galería y archivos estáticos.
- **Interfaz Gráfica:** Utiliza Tkinter para permitir:
  - Iniciar y detener el servidor.
  - Seleccionar la carpeta de fotos.
- **Observador de Cambios:** Utiliza `watchdog` para detectar cambios en la carpeta de fotos (funcionalidad que puede extenderse).
- **Empaquetable:** Se puede generar un ejecutable independiente con PyInstaller para facilitar su distribución en otros equipos.

## Requisitos

- Python 3.6 o superior
- Dependencias:
  - `qrcode[pil]`
  - `watchdog`

> **Nota:** El script `main.py` incluye un bloque para instalar automáticamente las dependencias si no están presentes.

## Instalación y Uso

### 1. Clona el Repositorio

Abre una terminal y ejecuta:

```bash
git clone https://github.com/tu_usuario/Conexion-QR-fotos.git
cd Conexion-QR-fotos
2. Ejecuta la aplicación
Ejecuta el script principal:

intento

Copiar
python main.py
Al hacerlo se abrirá una interfaz gráfica con las siguientes opciones:

Seleccionar la Carpeta de Fotos:
Utilice el botón "Seleccionar Carpeta de Fotos" para elegir el directorio desde donde se cargarán las imágenes.

Iniciar el Servidor:
Con el botón "Iniciar Servidor" se genera el código QR y se lanza el servidor en el puerto configurado (por defecto, 8000). La aplicación se sirve en la URL:
http://[IP_LOCAL]:8000(configurable en el código).

Detener el Servidor:
Con el botón "Detener Servidor" se para el servidor en ejecución.

3. Generación del Código QR
Al iniciar el servidor, se genera automáticamente un archivo codigo_qr.pngen la misma carpeta donde se encuentre el ejecutable (o main.pyen modo desarrollo), manteniendo la URL para acceder a la galería desde dispositivos móviles.

Empaquetado del Ejecutable con PyInstaller
Para crear un ejecutable autónomo que puedas instalar en otro ordenador, sigue estos pasos:

4. Instalar PyInstaller
Abre una terminal y ejecuta:

intento

Copiar
pip install pyinstaller
5. Estructura del Proyecto
Organiza el proyecto con la siguiente estructura:

intento

Copiar
Conexion-QR-fotos/
├── main.py
├── index.html         # (Opcional: si usas archivos estáticos para la web)
├── styles.css         # (Opcional)
├── scripts.js         # (Opcional)
├── photos/            # Carpeta para las imágenes (puede estar vacía inicialmente)
└── README.md
Nota: Si usas archivos estáticos (HTML, CSS, JS), deberás incluirlos al empaquetar.

6. Empaqueta la aplicación
Ejecuta el siguiente comando en la carpeta raíz del proyecto:

intento

Copiar
python -m PyInstaller --onefile --add-data "index.html;." --add-data "styles.css;." --add-data "scripts.js;." main.py
--onefile:Crea un único ejecutable.

--add-data "archivo;destino": Incluye los archivos estáticos en la raíz del ejecutable.

El ejecutable se generará en la carpeta dist/ .

7. Prueba el ejecutable
Copia el ejecutable generado (por ejemplo, main.exeen Windows) a otro ordenador oa un entorno limpio y ejecútalo para asegurarte de que la aplicación funcione correctamente y que todos los recursos se carguen.

Acceso a Recursos en el Ejecutable
El script main.pyutiliza la función resource_path()para acceder a los archivos estáticos empaquetados con PyInstaller. Esto garantiza que los archivos se encuentren correctamente en el ejecutable, ya sea en modo desarrollo o cuando se empaca.

Contribuciones
¡Se agradecen las contribuciones! Si tienes sugerencias, mejoras o encuentras algún error, por favor abre un problema o envía un pull request .

Licencia
Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo LICENSEpara más detalles.
