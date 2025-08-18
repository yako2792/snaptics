from smb.SMBConnection import SMBConnection

# Configuración
USUARIO = 'pign2'
CONTRASENA = 'P1gn4.@pymS4'
CLIENTE = 'cliente-python'
SERVIDOR = '192.168.0.221'  # IP del NAS
RECURSO = 'Resources'      # Nombre del recurso compartido
PUERTO = 445
TCP_DIRECTO = True

# Rutas
PRODUCT_ID = 'NEW_TEST'
BASE = '/FotosSpeed'

def conectar():
    conn = SMBConnection(
        USUARIO, CONTRASENA,
        CLIENTE, SERVIDOR,
        use_ntlm_v2=True,
        is_direct_tcp=TCP_DIRECTO
    )
    if conn.connect(SERVIDOR, PUERTO):
        print(f"Conexión exitosa al servidor SMB {SERVIDOR}.")
        return conn
    else:
        raise Exception("No se pudo conectar al servidor SMB.")
    

def subir_archivo(conn, ruta_local, ruta_remota):
    with open(ruta_local, 'rb') as f:
        conn.storeFile(RECURSO, ruta_remota, f)
    print(f"Archivo subido: {ruta_local} → {ruta_remota}")

def crear_directorio_remoto(conn, ruta_remota):
    """
    Crea un directorio remoto (y sus subdirectorios) en un recurso SMB.
    Si ya existen, muestra un mensaje amigable.
    """
    partes = ruta_remota.strip('/').split('/')
    ruta_actual = ''
    for parte in partes:
        ruta_actual += f'/{parte}'
        try:
            conn.createDirectory(RECURSO, ruta_actual)
            print(f"Carpeta creada: {ruta_actual}")
        except Exception as e:
            mensaje = str(e)
            if "0xC0000035" in mensaje or "STATUS_OBJECT_NAME_COLLISION" in mensaje:
                print(f"Carpeta ya existe: {ruta_actual}")
            else:
                print(f"Error al crear {ruta_actual}: {mensaje}")

def borrar_archivo(conn, ruta_remota):
    conn.deleteFiles(RECURSO, ruta_remota)
    print(f"Archivo eliminado: {ruta_remota}")

def borrar_directorio(conn, carpeta_remota):
    """
    Borra todos los archivos y subdirectorios dentro de una carpeta remota SMB,
    y luego elimina la carpeta en sí.
    """
    try:
        archivos = conn.listPath(RECURSO, carpeta_remota)
        for f in archivos:
            if f.filename in ['.', '..']:
                continue
            ruta = f"{carpeta_remota}/{f.filename}"
            if f.isDirectory:
                borrar_directorio(conn, ruta)
            else:
                conn.deleteFiles(RECURSO, ruta)
                print(f"Archivo eliminado: {ruta}")

        # Una vez vacía, eliminar la carpeta
        conn.deleteDirectory(RECURSO, carpeta_remota)
        print(f"Carpeta eliminada: {carpeta_remota}")

    except Exception as e:
        print(f"(!) Error al borrar {carpeta_remota}: {e}")

def listar_contenido_remoto(conn, ruta_remota):
    """
    Lista archivos y carpetas dentro de una ruta remota SMB.
    Si la carpeta no existe, muestra un mensaje claro.
    """
    try:
        archivos = conn.listPath(RECURSO, ruta_remota)
        print(f"Contenido de {ruta_remota}:")
        for f in archivos:
            if f.filename in ['.', '..']:
                continue
            tipo = "(D)" if f.isDirectory else "(F)"
            print(f"\t->{tipo} {f.filename}")
    except Exception as e:
        mensaje = str(e)
        if "0xC0000034" in mensaje or "STATUS_OBJECT_NAME_NOT_FOUND" in mensaje or "Path not found" in mensaje:
            print(f"(x) La carpeta no existe: {ruta_remota}")
        else:
            print(f"(!) Error al listar {ruta_remota}: {mensaje}")

 # Ejemplo de uso
if __name__ == "__main__":
    conn = conectar()
    shares = conn.listShares()
    names = [share.name for share in shares]
    print("Recursos SMB disponibles:")
    for name in names:
        print(f"→ {name}")

    print("\n\nContenido en directorio remoto antes.")
    listar_contenido_remoto(conn, f"{BASE}/{PRODUCT_ID}")

    # # CREATE
    # # Subir una carpeta completa
    # crear_directorio_remoto(conn, f"{BASE}/{PRODUCT_ID}")

    # # Subir un archivo
    # subir_archivo(conn, "archivo.txt", f"{BASE}/{PRODUCT_ID}/test.txt")

    # print("\n\nContenido en directorio remoto despues.")
    # listar_contenido_remoto(conn, f"{BASE}/{PRODUCT_ID}")

    # # DELETE
    # # Borrar un archivo
    # # borrar_archivo(conn, f"{BASE}/{PRODUCT_ID}/test.txt")
    borrar_archivo(conn, f"{BASE}/{PRODUCT_ID}/NEW_TEST0B.png")
    borrar_archivo(conn, f"{BASE}/{PRODUCT_ID}/NEW_TEST1D.png")
    borrar_archivo(conn, f"{BASE}/{PRODUCT_ID}/NEW_TEST2E.png")
    borrar_archivo(conn, f"{BASE}/{PRODUCT_ID}/NEW_TEST3C.png")
    borrar_archivo(conn, f"{BASE}/{PRODUCT_ID}/Thumbs.db")

    # # Borrar una carpeta completa
    borrar_directorio(conn, f"{BASE}/{PRODUCT_ID}")

    print("\n\nContenido en directorio remoto final.")
    listar_contenido_remoto(conn, f"{BASE}/{PRODUCT_ID}")

    conn.close()
    print("Conexion cerrada correctamente.")
