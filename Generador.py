import qrcode
import http.server
import socketserver
import os

# Configuración del servidor
PORT = 8000
DIRECTORY = r"C:\Users\ÁlvaroPavón\OneDrive - PLANTASUR TRADING SL\Escritorio\PruebaConexion"
IP_LOCAL = "192.168.1.94"  # Reemplaza esto con tu dirección IP local

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

def generar_galeria():
    extensiones_imagenes = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp','jfif')
    imagenes = [f for f in os.listdir(DIRECTORY) if f.lower().endswith(extensiones_imagenes)]
    html_content = '''
    <html>
    <head>
        <title>Galería de Fotos</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: var(--bg-color); color: var(--text-color); }
            .gallery { display: flex; flex-wrap: wrap; justify-content: center; }
            .gallery img { width: 100%; max-width: 200px; height: auto; object-fit: cover; margin: 10px; cursor: pointer; border-radius: 10px; }
            .modal { display: none; position: fixed; z-index: 1; left: 0; top: 0; width: 100%; height: 100%; overflow: auto; background-color: rgba(0,0,0,0.8); }
            .modal-content { margin: auto; display: block; width: 80%; max-width: 700px; height: auto; border-radius: 10px; }
            .close { position: absolute; top: 20px; right: 35px; color: var(--text-color); font-size: 40px; font-weight: bold; cursor: pointer; }
            .download-btn { display: block; margin: 20px auto; padding: 10px 20px; background-color: #4CAF50; color: white; text-align: center; text-decoration: none; font-size: 20px; border-radius: 5px; width: auto; }
            .modal-body { text-align: center; }
            @media (max-width: 600px) {
                .gallery img { max-width: 100px; }
                .modal-content { width: 100%; }
                .download-btn { font-size: 16px; padding: 8px 16px; }
                .close { font-size: 30px; }
            }
        </style>
        <script>
            function setTheme() {
                const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
                if (prefersDark) {
                    document.documentElement.style.setProperty('--bg-color', '#121212');
                    document.documentElement.style.setProperty('--text-color', '#ffffff');
                } else {
                    document.documentElement.style.setProperty('--bg-color', '#ffffff');
                    document.documentElement.style.setProperty('--text-color', '#000000');
                }
            }
            window.addEventListener('load', setTheme);
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', setTheme);
            function openModal(src) {
                document.getElementById('myModal').style.display = "block";
                document.getElementById('modalImage').src = src;
                document.getElementById('modalImage').style.maxHeight = "80vh";
                document.getElementById('downloadLink').href = src;
            }
            function closeModal() {
                document.getElementById('myModal').style.display = "none";
            }
        </script>
    </head>
    <body>
        <h1 style="text-align:center;">Galería de Fotos</h1>
        <div class="gallery">
    '''
    for imagen in imagenes:
        html_content += f'<img src="{imagen}" alt="{imagen}" onclick="openModal(\'{imagen}\')">'
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
    
    with open(os.path.join(DIRECTORY, 'index.html'), 'w') as f:
        f.write(html_content)

# Generar el código QR
def generar_qr():
    url = f"http://{IP_LOCAL}:{PORT}"
    qr = qrcode.make(url)
    qr.save("codigo_qr.png")
    print(f"Código QR generado: {url}")

# Iniciar el servidor
def iniciar_servidor():
    os.chdir(DIRECTORY)
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Servidor iniciado en {IP_LOCAL}:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    generar_galeria()
    generar_qr()
    iniciar_servidor()