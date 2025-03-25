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

# Función para generar la galería con diseño orgánico y fluido
def generar_galeria():
    extensiones_imagenes = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp', 'jfif')
    imagenes = [f for f in os.listdir(DIRECTORY) if f.lower().endswith(extensiones_imagenes)]
    
    # Se elimina la referencia a la librería de GitHub e incorpora CSS personalizado
    html_content = f'''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="utf-8">
        <!-- Meta tag para dispositivos móviles -->
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Galería de Fotos</title>
        <style>
            /* Fondo degradado y suave */
            body {{
                margin: 0;
                padding: 0;
                font-family: 'Arial', sans-serif;
                background: linear-gradient(135deg, #a1c4fd, #c2e9fb);
                color: #333;
                display: flex;
                flex-direction: column;
                align-items: center;
                box-sizing: border-box;
            }}
            h1 {{
                margin: 20px 0;
                font-size: 2em;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
            }}
            /* Contenedor de la galería con formas orgánicas */
            .gallery {{
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 15px;
                max-width: 1000px;
                margin: 20px auto;
                padding: 10px;
            }}
            .image-container {{
                position: relative;
                flex: 1 1 150px;
                /* Bordes irregulares para un efecto orgánico */
                border-radius: 40% 60% 50% 70% / 60% 40% 70% 50%;
                overflow: hidden;
                cursor: pointer;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                transition: transform 0.3s ease;
            }}
            .image-container:hover {{
                transform: scale(1.05);
            }}
            .image-container img {{
                width: 100%;
                height: auto;
                display: block;
            }}
            .gallery img.selected {{
                outline: 5px solid #0078D4;
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
            /* Modal para ver imagen a pantalla completa */
            .modal {{
                display: none;
                position: fixed;
                z-index: 10;
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
            /* Botón de cerrar con mix-blend-mode para adaptarse al fondo */
            .close {{
                position: absolute;
                top: 20px;
                right: 35px;
                font-size: 30px;
                font-weight: bold;
                cursor: pointer;
                color: white;
                mix-blend-mode: difference;
            }}
            /* Contador y botones de control minimalistas */
            .multi-select-btn, .counter {{
                position: fixed;
                font-size: 16px;
                cursor: pointer;
                z-index: 2;
            }}
            /* Estilo del botón de selección múltiple con forma */
            .multi-select-btn {{
                top: 10px;
                left: 10px;
                background: rgba(255, 255, 255, 0.8);
                border: none;
                border-radius: 25px;
                color: #0078D4;
                padding: 8px 16px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                font-weight: bold;
                transition: background-color 0.3s ease;
            }}
            .multi-select-btn:hover {{
                background-color: rgba(255, 255, 255, 1);
            }}
            .counter {{
                top: 10px;
                right: 10px;
                background: none;
                border: none;
                display: flex;
                align-items: center;
                color: #0078D4;
            }}
            .counter .counter-number {{
                font-size: 16px;
                margin-right: 5px;
            }}
            .counter .select-btn {{
                background: none;
                border: none;
                cursor: pointer;
                font-size: 16px;
                color: #0078D4;
            }}
            /* Modal: Centrar la imagen y el botón de descarga */
            .modal-body {{
                text-align: center;
            }}
            .modal-body .download-btn {{
                margin-top: 20px;
                display: inline-block;
                background-color: #0078D4;
                color: #fff;
                padding: 10px 20px;
                border-radius: 25px;
                text-decoration: none;
                font-size: 18px;
                transition: background-color 0.3s ease;
            }}
            .modal-body .download-btn:hover {{
                background-color: #005ea6;
            }}
            /* Animación para modal */
            @keyframes zoomIn {{
                from {{ transform: scale(0.5); }}
                to {{ transform: scale(1); }}
            }}
            /* Ajustes responsivos */
            @media (max-width: 600px) {{
                h1 {{ font-size: 1.5em; }}
                .multi-select-btn, .counter {{
                    font-size: 14px;
                }}
                .modal-body .download-btn {{
                    font-size: 16px;
                    padding: 8px 16px;
                }}
            }}
            @media (max-width: 400px) {{
                h1 {{ font-size: 1.2em; }}
                .multi-select-btn, .counter {{
                    font-size: 12px;
                }}
                .modal-body .download-btn {{
                    font-size: 14px;
                    padding: 6px 12px;
                }}
            }}
            @keyframes zoomIn {{
                from {{ transform: scale(0.5); }}
                to {{ transform: scale(1); }}
            }}
        </style>
        <script>
            let multiSelectActive = false;
            
            function setTheme() {{
                // (Opcional: lógica para cambiar tema)
            }}
            window.addEventListener('load', setTheme);

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
                    'Desactivar Selección Múltiple' : 'Activar Selección Múltiple';
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
                        btn.className = 'select-btn';
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
        <button class="multi-select-btn" onclick="toggleMultiSelect()">Activar Selección Múltiple</button>
        <!-- El contador muestra únicamente el número -->
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
