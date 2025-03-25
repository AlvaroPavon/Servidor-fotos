import qrcode
import http.server
import socketserver
import os

# Configuración del servidor
PORT = 8000
DIRECTORY = r"C:\Users\ÁlvaroPavón\OneDrive - PLANTASUR TRADING SL\Escritorio\PruebaConexion"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

# Generar el código QR
def generar_qr():
    url = f"http://localhost:{PORT}"
    qr = qrcode.make(url)
    qr.save("codigo_qr.png")
    print(f"Código QR generado: {url}")

# Iniciar el servidor
def iniciar_servidor():
    os.chdir(DIRECTORY)
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Servidor iniciado en el puerto {PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    generar_qr()
    iniciar_servidor()