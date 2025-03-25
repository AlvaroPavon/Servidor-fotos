import subprocess
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import qrcode
import http.server
import socketserver
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import stat

def install_and_import(package, import_name=None):
    """
    Intenta importar el paquete; si falla, lo instala usando pip.
    """
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
# Valor por defecto de la carpeta de imágenes (se podrá cambiar desde la interfaz)
DIRECTORY = r"C:\Users\ÁlvaroPavón\OneDrive - PLANTASUR TRADING SL\Escritorio\PruebaConexion"
IP_LOCAL = "192.168.1.94"  # Reemplaza con tu dirección IP local

# Ruta del script (para guardar el código QR en la misma carpeta del script)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

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
        qr_path = os.path.join(SCRIPT_DIR, "codigo_qr.png")
        qr.save(qr_path)
        print(f"Código QR generado: {url}")
        print(f"Guardado en: {qr_path}")
    except Exception as e:
        print(f"Error al guardar el código QR: {e}")

class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print("Cambio detectado en el directorio.")
        # Aquí podrías agregar lógica para actualizar la galería si es necesario.

# Hilo para correr el servidor y el observador
class ServerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.httpd = None
        self.observer = None

    def run(self):
        cambiar_permisos(DIRECTORY)
        # Iniciar observador para detectar cambios en la carpeta seleccionada
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

server_thread = None  # Variable global para el hilo del servidor

def start_server():
    global server_thread
    if server_thread is None or not server_thread.is_alive():
        generar_qr()  # Genera el código QR en la carpeta del script
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

def select_directory():
    """Abre un diálogo para seleccionar la carpeta de fotos y actualiza la variable DIRECTORY."""
    global DIRECTORY
    new_dir = filedialog.askdirectory(initialdir=DIRECTORY, title="Selecciona la carpeta de fotos")
    if new_dir:
        DIRECTORY = new_dir
        path_label.config(text=f"Carpeta: {DIRECTORY}")
        print(f"Nueva carpeta seleccionada: {DIRECTORY}")

# Interfaz gráfica con Tkinter
root = tk.Tk()
root.title("Control de Servidor de Galería")
root.geometry("350x200")

start_button = tk.Button(root, text="Iniciar Servidor", command=start_server, width=25)
start_button.pack(pady=5)

stop_button = tk.Button(root, text="Detener Servidor", command=stop_server, width=25)
stop_button.pack(pady=5)

dir_button = tk.Button(root, text="Seleccionar Carpeta de Fotos", command=select_directory, width=25)
dir_button.pack(pady=5)

path_label = tk.Label(root, text=f"Carpeta: {DIRECTORY}", wraplength=300)
path_label.pack(pady=5)

status_label = tk.Label(root, text="Servidor detenido.")
status_label.pack(pady=5)

root.mainloop()
