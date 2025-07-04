#!/bin/bash

# Variables configuradas según tu ruta y usuario
WINDOWS_IP="192.168.3.65"
WINDOWS_SHARE="MartinPSD1"
WINDOWS_USER="pign2"          # Usuario de windows
WINDOWS_PASS="P1gn4.@pymS4"   # contrasenia de windows

LOCAL_FILE="/home/pi/archivo_a_copiar.txt"     # AQUI EL ARCHIVO A TRANSFERIR
MOUNT_POINT="/mnt/windows_share"

# Crear punto de montaje si no existe
mkdir -p "$MOUNT_POINT"

# Montar la carpeta compartida SMB (versión 3.0)
sudo mount -t cifs "//${WINDOWS_IP}/${WINDOWS_SHARE}" "$MOUNT_POINT" -o username=$WINDOWS_USER,password=$WINDOWS_PASS,vers=3.0

if [ $? -ne 0 ]; then
    echo "Error montando la carpeta SMB. Revisa credenciales y conexión."
    exit 1
fi

# Copiar archivo al subdirectorio dentro del share
cp "$LOCAL_FILE" "$MOUNT_POINT/ActualizaciondeFotos/00_PSD TODOS/"

if [ $? -eq 0 ]; then
    echo "Archivo copiado exitosamente."
else
    echo "Error al copiar el archivo."
fi

# Desmontar la carpeta SMB
sudo umount "$MOUNT_POINT"
