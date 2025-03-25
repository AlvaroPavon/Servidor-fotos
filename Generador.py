import qrcode
import http.server
import socketserver
import os

# Configuración del servidor
PORT = 8000
DIRECTORY = r"C:\Users\ÁlvaroPavón\OneDrive - PLANTASUR TRADING SL\Escritorio\PruebaConexion"
IP_LOCAL = "192.168.1.94"  

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

def generar_galeria():
    imagenes = [f for f in os.listdir(DIRECTORY) if f.endswith(('.png', '.jpg', '.jpeg', '.gif','jfif'))]
    html_content = '<html><head><title>Galería de Fotos</title></head><body>'
    html_content += '<h1>Galería de Fotos</h1>'
    for imagen in imagenes:
        html_content += f'<img src="{imagen}" style="width:200px;height:auto;margin:10px;">'
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