import qrcode
import http.server
import socketserver
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import stat

# Configuracion del servidor
PORT = 8000
DIRECTORY = r"C:\Users\ÁlvaroPavón\OneDrive - PLANTASUR TRADING SL\Escritorio\PruebaConexion"
IP_LOCAL = "192.168.1.94"  # Reemplaza esto con tu direccion IP local

# Funcion para cambiar los permisos del directorio
def cambiar_permisos(directorio):
    try:
        # Cambiar los permisos para que todos los usuarios tengan acceso de lectura y escritura
        os.chmod(directorio, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        print(f"Permisos de {directorio} cambiados exitosamente.")
    except Exception as e:
        print(f"Error al cambiar permisos: {e}")

# Definir el manejador para las solicitudes HTTP
class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

# Funcion para generar la galeria
def generar_galeria():
    extensiones_imagenes = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp', 'jfif')
    imagenes = [f for f in os.listdir(DIRECTORY) if f.lower().endswith(extensiones_imagenes)]
    
    # Iniciar el contenido HTML
    html_content = '''
    <html>
    <head>
        <title>Galeria de Fotos</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/samsunginternet/OneUI-Web/oui-css/oui.css">
        <style>
            :root {
                --primary-color: #0078D4;  /* Azul One UI */
                --secondary-color: #ffffff;
                --bg-color-light: #f8f9fa;
                --bg-color-dark: #121212;
                --text-color-light: #000000;
                --text-color-dark: #ffffff;
                --border-radius: 8px;
                --card-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }
            body {
                font-family: 'SamsungOne', Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: var(--bg-color-light);
                color: var(--text-color-light);
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                box-sizing: border-box;
            }
            h1 {
                font-size: 24px;
                text-align: center;
                margin-bottom: 20px;
                color: var(--primary-color);
            }
            .gallery {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                padding: 20px;
                gap: 15px;
                margin-bottom: 20px;
            }
            .gallery img {
                width: 100%;
                max-width: 180px;
                height: auto;
                object-fit: cover;
                border-radius: var(--border-radius);
                transition: transform 0.3s ease;
                cursor: pointer;
                position: relative;
                box-shadow: var(--card-shadow);
                border: 3px solid transparent;
            }
            .gallery img.selected {
                border: 3px solid var(--primary-color);
            }
            .gallery img:hover {
                transform: scale(1.05);
            }
            .checkmark {
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
            }
            .gallery img.selected .checkmark {
                display: flex;
            }
            .modal {
                display: none;
                position: fixed;
                z-index: 1;
                left: 0;
                top: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0,0,0,0.8);
                padding: 10px;
            }
            .modal-content {
                margin: auto;
                display: block;
                width: 100%;
                max-width: 90%;
                height: auto;
                border-radius: 10px;
                animation: zoomIn 0.5s;
            }
            .close {
                position: absolute;
                top: 20px;
                right: 35px;
                color: var(--text-color-light);
                font-size: 30px;
                font-weight: bold;
                cursor: pointer;
            }
            .download-btn {
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
            }
            .multi-select-btn, .counter {
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
            }
            .counter {
                top: 10px;
                right: 10px;
            }
            .multi-select-btn {
                top: 10px;
                left: 10px;
            }
            @media (max-width: 600px) {
                .gallery img {
                    max-width: 150px;
                }
                .modal-content {
                    width: 100%;
                }
                .download-btn, .multi-select-btn, .counter {
                    font-size: 14px;
                    padding: 6px 12px;
                }
                .close {
                    font-size: 25px;
                }
            }
            @media (max-width: 400px) {
                .gallery img {
                    max-width: 120px;
                }
                .modal-content {
                    width: 100%;
                }
                .download-btn, .multi-select-btn, .counter {
                    font-size: 12px;
                    padding: 4px 8px;
                }
                .close {
                    font-size: 20px;
                }
            }
            @keyframes zoomIn {
                from { transform: scale(0.5); }
                to { transform: scale(1); }
            }
        </style>
        <script>
            let multiSelectActive = false;

            function setTheme() {
                const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
                if (prefersDark) {
                    document.documentElement.style.setProperty('--bg-color-light', '#121212');
                    document.documentElement.style.setProperty('--text-color-light', '#ffffff');
                } else {
                    document.documentElement.style.setProperty('--bg-color-light', '#ffffff');
                    document.documentElement.style.setProperty('--text-color-light', '#000000');
                }
                document.querySelector('meta[name="theme-color"]').setAttribute('content', prefersDark ? '#121212' : '#ffffff');
            }
            window.addEventListener('load', setTheme);
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', setTheme);

            function openModal(src) {
                if (!multiSelectActive) {
                    document.getElementById('myModal').style.display = "block";
                    document.getElementById('modalImage').src = src;
                    document.getElementById('modalImage').style.maxHeight = "80vh";
                    document.getElementById('downloadLink').href = src;
                }
            }

            function closeModal() {
                document.getElementById('myModal').style.display = "none";
            }

            function toggleSelect(img) {
                img.classList.toggle('selected');
                updateCounter();
            }

            function downloadSelected() {
                const selectedImages = document.querySelectorAll('.gallery img.selected');
                selectedImages.forEach(img => {
                    const link = document.createElement('a');
                    link.href = img.src;
                    link.download = img.alt;
                    link.click();
                });
            }

            function toggleMultiSelect() {
                multiSelectActive = !multiSelectActive;
                document.querySelector('.multi-select-btn').textContent = multiSelectActive ? 'Desactivar Seleccion Multiple' : 'Activar Seleccion Multiple';
                document.querySelectorAll('.gallery img').forEach(img => {
                    img.onclick = multiSelectActive ? () => toggleSelect(img) : () => openModal(img.src);
                });
                document.querySelector('.counter').style.display = multiSelectActive ? 'flex' : 'none';
                if (!multiSelectActive) {
                    document.querySelectorAll('.gallery img.selected').forEach(img => img.classList.remove('selected'));
                }
                updateCounter();
            }

            function updateCounter() {
                const count = document.querySelectorAll('.gallery img.selected').length;
                document.querySelector('.counter').textContent = `Seleccionadas: ${count}`;
                const selectBtn = document.querySelector('.counter .select-btn');
                if (multiSelectActive) {
                    if (!selectBtn) {
                        const btn = document.createElement('button');
                        btn.className = 'select-btn download-btn';  // Usando el mismo estilo de botón
                        btn.textContent = 'Descargar Seleccionadas';
                        btn.onclick = downloadSelected;
                        document.querySelector('.counter').appendChild(btn);
                    }
                } else if (selectBtn) {
                    selectBtn.remove();
                }
            }

            document.addEventListener('contextmenu', event => event.preventDefault());
        </script>
        <meta name="theme-color" content="#ffffff">
    </head>
    <body>
        <h1>Galeria de Fotos</h1>
        <button class="multi-select-btn" onclick="toggleMultiSelect()">Activar Seleccion Multiple</button>
        <div class="counter" style="display:none;">Seleccionadas: 0</div>
        <div class="gallery" id="gallery">
    '''
    
    # Generar imagenes de la carpeta
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
    
    # Guardar el archivo HTML con codificacion UTF-8
    with open(os.path.join(DIRECTORY, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html_content)

# Funcion para generar el codigo QR
def generar_qr():
    url = f"http://{IP_LOCAL}:{PORT}"
    qr = qrcode.make(url)
    qr.save("codigo_qr.png")
    print(f"Codigo QR generado: {url}")

# Funcion para observar cambios en la carpeta y generar la galeria automaticamente
class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.startswith(DIRECTORY):
            generar_galeria()

# Funcion para iniciar el servidor
def iniciar_servidor():
    # Cambiar los permisos del directorio antes de continuar
    cambiar_permisos(DIRECTORY)
    
    # Configurar observador de cambios
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
