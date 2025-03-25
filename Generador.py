import qrcode
import http.server
import socketserver
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import stat

# Configuración del servidor
PORT = 8000
DIRECTORY = r"C:\Users\ÁlvaroPavón\OneDrive - PLANTASUR TRADING SL\Escritorio\PruebaConexion"
IP_LOCAL = "192.168.1.94"  # Reemplaza con tu dirección IP local

# Función para cambiar los permisos del directorio
def cambiar_permisos(directorio):
    try:
        os.chmod(directorio, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        print(f"Permisos de {directorio} cambiados exitosamente.")
    except Exception as e:
        print(f"Error al cambiar permisos: {e}")

# Manejador para las solicitudes HTTP
class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

# Función para generar la galería (incluye modal, selección múltiple, descarga, etc.)
def generar_galeria():
    extensiones_imagenes = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp', 'jfif')
    imagenes = [f for f in os.listdir(DIRECTORY) if f.lower().endswith(extensiones_imagenes)]
    
    # Se usan los recursos de OneForAll-WebUI ubicados en la carpeta "ui"
    html_content = f'''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="utf-8">
        <!-- Meta tag para dispositivos móviles -->
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Galería de Fotos</title>
        <!-- Enlace al CSS de OneForAll-WebUI desde la carpeta 'ui' -->
        <link rel="stylesheet" href="ui/css/oneforall.min.css">
        <style>
            :root {{
                --primary-color: #0078D4;  /* Azul One UI */
                --secondary-color: #ffffff;
                --bg-color-light: #f8f9fa;
                --bg-color-dark: #121212;
                --text-color-light: #000000;
                --text-color-dark: #ffffff;
                --border-radius: 8px;
                --card-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }}
            body {{
                font-family: 'SamsungOne', Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: var(--bg-color-light);
                color: var(--text-color-light);
                display: flex;
                flex-direction: column;
                align-items: center;
                box-sizing: border-box;
            }}
            h1 {{
                font-size: 24px;
                text-align: center;
                margin: 20px 0;
                color: var(--primary-color);
            }}
            .gallery {{
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 15px;
                max-width: 1000px;
                margin: 20px auto;
            }}
            .image-container {{
                position: relative;
                flex: 1 1 150px;
                box-shadow: var(--card-shadow);
                border-radius: var(--border-radius);
                overflow: hidden;
                cursor: pointer;
            }}
            .image-container img {{
                width: 100%;
                height: auto;
                display: block;
                transition: transform 0.3s ease;
            }}
            .image-container:hover img {{
                transform: scale(1.05);
            }}
            .gallery img.selected {{
                border: 3px solid var(--primary-color);
            }}
            .checkmark {{
                position: absolute;
                top: 5px;
                right: 5px;
                width: 25px;
                height: 25px;
                background-color: rgba(0, 0, 0, 0.5);
                color: white;
                border-radius: 50%;
                display: flex;
                justify-content: center;
                align-items: center;
                font-size: 18px;
                display: none;
            }}
            .gallery img.selected + .checkmark {{
                display: flex;
            }}
            .modal {{
                display: none;
                position: fixed;
                z-index: 1;
                left: 0;
                top: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0,0,0,0.8);
                padding: 10px;
            }}
            .modal-content {{
                margin: auto;
                display: block;
                width: 100%;
                max-width: 90%;
                height: auto;
                border-radius: 10px;
                animation: zoomIn 0.5s;
            }}
            .close {{
                position: absolute;
                top: 20px;
                right: 35px;
                color: var(--text-color-light);
                font-size: 30px;
                font-weight: bold;
                cursor: pointer;
            }}
            .download-btn {{
                display: block;
                margin: 20px auto;
                padding: 8px 16px;
                background-color: var(--primary-color);
                color: var(--secondary-color);
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                border-radius: var(--border-radius);
                cursor: pointer;
            }}
            /* Botones y contador en posición fija */
            .multi-select-btn, .counter {{
                position: fixed;
                padding: 10px 20px;
                background-color: var(--primary-color);
                color: var(--secondary-color);
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                border-radius: var(--border-radius);
                cursor: pointer;
                z-index: 2;
            }}
            .counter {{
                top: 10px;
                right: 10px;
            }}
            .multi-select-btn {{
                top: 10px;
                left: 10px;
            }}
            /* Reducir tamaño de botones en móviles */
            @media (max-width: 600px) {{
                .multi-select-btn, .counter, .download-btn {{
                    font-size: 12px;
                    padding: 4px 8px;
                }}
            }}
            @media (max-width: 400px) {{
                .multi-select-btn, .counter, .download-btn {{
                    font-size: 10px;
                    padding: 2px 4px;
                }}
            }}
            /* Eliminar fondo, bordes y padding en el contador y el botón de descarga */
            .counter {{
                background: none !important;
                padding: 0 !important;
                border: none !important;
            }}
            .counter .select-btn {{
                background: none !important;
                padding: 0 !important;
                border: none !important;
                cursor: pointer;
            }}
        </style>
        <script>
            let multiSelectActive = false;
            
            function setTheme() {{
                const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
                if (prefersDark) {{
                    document.documentElement.style.setProperty('--bg-color-light', '#121212');
                    document.documentElement.style.setProperty('--text-color-light', '#ffffff');
                }} else {{
                    document.documentElement.style.setProperty('--bg-color-light', '#ffffff');
                    document.documentElement.style.setProperty('--text-color-light', '#000000');
                }}
                document.querySelector('meta[name="theme-color"]').setAttribute('content', prefersDark ? '#121212' : '#ffffff');
            }}
            window.addEventListener('load', setTheme);
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', setTheme);

            function openModal(src) {{
                if (!multiSelectActive) {{
                    document.getElementById('myModal').style.display = "block";
                    document.getElementById('modalImage').src = src;
                    document.getElementById('modalImage').style.maxHeight = "80vh";
                    document.getElementById('downloadLink').href = src;
                }}
            }}

            function closeModal() {{
                document.getElementById('myModal').style.display = "none";
            }}

            function toggleSelect(img) {{
                img.classList.toggle('selected');
                updateCounter();
            }}

            function downloadSelected() {{
                const selectedImages = document.querySelectorAll('.gallery img.selected');
                selectedImages.forEach(img => {{
                    const link = document.createElement('a');
                    link.href = img.src;
                    link.download = img.alt;
                    link.click();
                }});
            }}

            function toggleMultiSelect() {{
                multiSelectActive = !multiSelectActive;
                document.querySelector('.multi-select-btn').textContent = multiSelectActive ?
                    'Desactivar Seleccion Multiple' : 'Activar Seleccion Multiple';
                document.querySelectorAll('.gallery img').forEach(img => {{
                    img.onclick = multiSelectActive ? () => toggleSelect(img) : () => openModal(img.src);
                }});
                document.querySelector('.counter').style.display = multiSelectActive ? 'flex' : 'none';
                if (!multiSelectActive) {{
                    document.querySelectorAll('.gallery img.selected').forEach(img => img.classList.remove('selected'));
                }}
                updateCounter();
            }}

            function updateCounter() {{
                const count = document.querySelectorAll('.gallery img.selected').length;
                // Actualizamos solo el número en el span interno del contador
                document.querySelector('.counter .counter-number').textContent = count;
                const selectBtn = document.querySelector('.counter .select-btn');
                if (multiSelectActive) {{
                    if (!selectBtn) {{
                        const btn = document.createElement('button');
                        btn.className = 'select-btn download-btn';
                        // Usamos un icono de descarga (emoji)
                        btn.textContent = '⬇️';
                        btn.onclick = downloadSelected;
                        document.querySelector('.counter').appendChild(btn);
                    }}
                }} else if (selectBtn) {{
                    selectBtn.remove();
                }}
            }}

            document.addEventListener('contextmenu', event => event.preventDefault());
        </script>
        <meta name="theme-color" content="#ffffff">
    </head>
    <body>
        <h1>Galería de Fotos</h1>
        <button class="multi-select-btn" onclick="toggleMultiSelect()">Activar Seleccion Multiple</button>
        <!-- El contador ahora muestra solo el número -->
        <div class="counter" style="display:none;"><span class="counter-number">0</span></div>
        <div class="gallery" id="gallery">
    '''
    # Agregar cada imagen a la galería
    for imagen in imagenes:
        html_content += f'''
                <div class="image-container">
                    <img src="{imagen}" alt="{imagen}" onclick="openModal('{imagen}')" ondblclick="toggleSelect(this)">
                    <div class="checkmark">✔</div>
                </div>
        '''
    html_content += '''
        </div>
        <div id="myModal" class="modal">
            <span class="close" onclick="closeModal()">&times;</span>
            <div class="modal-body">
                <img class="modal-content" id="modalImage">
                <a id="downloadLink" class="download-btn" href="#" download>Descargar Imagen</a>
            </div>
        </div>
        <!-- Enlace al JS de OneForAll-WebUI desde la carpeta 'ui' -->
        <script src="ui/js/oneforall.min.js"></script>
    </body>
    </html>
    '''
    try:
        with open(os.path.join(DIRECTORY, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html_content)
        print("Galería generada.")
    except Exception as e:
        print(f"Error al generar la galería: {e}")

# Función para generar el código QR
def generar_qr():
    url = f"http://{IP_LOCAL}:{PORT}"
    qr = qrcode.make(url)
    try:
        qr.save(os.path.join(DIRECTORY, "codigo_qr.png"))
        print(f"Código QR generado: {url}")
    except Exception as e:
        print(f"Error al guardar el código QR: {e}")

# Observador de cambios en el directorio
class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.startswith(DIRECTORY):
            generar_galeria()

# Función para iniciar el servidor HTTP y el observador
def iniciar_servidor():
    cambiar_permisos(DIRECTORY)
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, DIRECTORY, recursive=False)
    observer.start()

    try:
        os.chdir(DIRECTORY)
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"Servidor iniciado en {IP_LOCAL}:{PORT}")
            httpd.serve_forever()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    generar_galeria()
    generar_qr()
    iniciar_servidor()
