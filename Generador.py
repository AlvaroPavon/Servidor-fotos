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
    html_content = '<html><head><title>Galería de Fotos</title></head>'
    html_content += '<style>img { width: 200px; height: 200px; object-fit: cover; margin: 10px; }</style>'
    html_content += '</head><body>'
    html_content += '<h1>Galería de Fotos</h1>'
    for imagen in imagenes:
        html_content += f'<div><a href="{imagen}" download><img src="{imagen}" alt="{imagen}"></a></div>'
    html_content += '</body></html>'
    
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