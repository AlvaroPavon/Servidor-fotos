import subprocess
import sys
import threading
import tkinter as tk
from tkinter import messagebox
import qrcode
import http.server
import socketserver
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import stat

# Función para instalar e importar paquetes
def install_and_import(package, import_name=None):
    try:
        if import_name:
            __import__(import_name)
        else:
            __import__(package.split("[")[0])
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Instalar dependencias necesarias
install_and_import("qrcode[pil]", "qrcode")
install_and_import("watchdog")

# Configuración del servidor
PORT = 8000
# Directorio donde se encuentran index.html, styles.css, scripts.js, imágenes, etc.
DIRECTORY = r"C:\Users\ÁlvaroPavón\OneDrive - PLANTASUR TRADING SL\Escritorio\PruebaConexion"
IP_LOCAL = "192.168.1.94"  # Reemplaza con tu dirección IP local

def cambiar_permisos(directorio):
    try:
        os.chmod(directorio, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        print(f"Permisos de {directorio} cambiados exitosamente.")
    except Exception as e:
        print(f"Error al cambiar permisos: {e}")

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

def generar_qr():
    url = f"http://{IP_LOCAL}:{PORT}"
    qr = qrcode.make(url)
    try:
        qr.save(os.path.join(DIRECTORY, "codigo_qr.png"))
        print(f"Código QR generado: {url}")
    except Exception as e:
        print(f"Error al guardar el código QR: {e}")

class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print("Cambio detectado en el directorio.")
        # Aquí se podría agregar lógica para actualizar la galería

# Clase para correr el servidor en un hilo separado
class ServerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.httpd = None
        self.observer = None

    def run(self):
        cambiar_permisos(DIRECTORY)
        # Iniciar el observador para detectar cambios
        self.observer = Observer()
        self.observer.schedule(FileChangeHandler(), DIRECTORY, recursive=True)
        self.observer.start()
        os.chdir(DIRECTORY)
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            self.httpd = httpd
            print(f"Servidor iniciado en {IP_LOCAL}:{PORT}")
            try:
                httpd.serve_forever()
            except Exception as e:
                print("Servidor detenido:", e)

    def stop(self):
        if self.httpd:
            self.httpd.shutdown()
        if self.observer:
            self.observer.stop()
            self.observer.join()

# Variables globales para el hilo del servidor
server_thread = None

# Funciones para iniciar y detener el servidor mediante la interfaz
def start_server():
    global server_thread
    if server_thread is None or not server_thread.is_alive():
        generar_qr()  # Genera el código QR antes de iniciar el servidor
        server_thread = ServerThread()
        server_thread.start()
        status_label.config(text="Servidor iniciado.")
    else:
        messagebox.showinfo("Información", "El servidor ya está en ejecución.")

def stop_server():
    global server_thread
    if server_thread and server_thread.is_alive():
        server_thread.stop()
        status_label.config(text="Servidor detenido.")
    else:
        messagebox.showinfo("Información", "El servidor no está en ejecución.")

# Crear la interfaz gráfica con Tkinter
root = tk.Tk()
root.title("Control de Servidor de Galería")
root.geometry("300x150")

start_button = tk.Button(root, text="Iniciar Servidor", command=start_server, width=20)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Detener Servidor", command=stop_server, width=20)
stop_button.pack(pady=10)

status_label = tk.Label(root, text="Servidor detenido.")
status_label.pack(pady=10)

root.mainloop()
