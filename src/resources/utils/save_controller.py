from os.path import dirname
from src.resources.properties import Properties as Props
from src.resources.utils.credentials_controller import Credentials
from smb.SMBConnection import SMBConnection

class Save:
    @staticmethod
    def connect(user: str, password: str, display_name: str, server_ip: str):
        conn = SMBConnection(
            user, password,
            display_name, server_ip,
            use_ntlm_v2=True,
            is_direct_tcp=True
        )
        if conn.connect(server_ip, 445):
            print(f"Conexión exitosa al servidor SMB {server_ip}.")
            return conn
        else:
            raise Exception("No se pudo conectar al servidor SMB.")

    @staticmethod
    def mkdir_p_remote(conn, resource, ruta_remota):
        """
        Crea un directorio remoto (y sus subdirectorios) en un recurso SMB.
        Si ya existen, muestra un mensaje amigable.
        """
        partes = ruta_remota.strip('/').split('/')
        ruta_actual = ''
        for parte in partes:
            ruta_actual += f'/{parte}'
            try:
                conn.createDirectory(resource, ruta_actual)
                print(f"Carpeta creada: {ruta_actual}")
            except Exception as e:
                mensaje = str(e)
                if "0xC0000035" in mensaje or "STATUS_OBJECT_NAME_COLLISION" in mensaje:
                    print(f"Carpeta ya existe: {ruta_actual}")
                else:
                    print(f"Error al crear {ruta_actual}: {mensaje}")

    @staticmethod
    def post_file_in_remote(local_file_path: str, remote_file_path: str):

        conn = Save.connect(
            user=Props.USE_USER,
            password=Credentials.decrypt_password(Props.USE_PASSWORD),
            display_name="SnapticsConn",
            server_ip=Props.USE_IP
        )

        # Split on resource and file path
        split_result = remote_file_path.lstrip('/').split('/', 1)

        # Asignar partes
        resource = split_result[0]
        print(f"Resource detectado: {resource}")

        file_path = '/' + split_result[1] if len(split_result) > 1 else '/'
        print(f"File path detectado: {file_path}")

        Save.mkdir_p_remote(conn=conn, resource=resource, ruta_remota=dirname(file_path))

        with open(local_file_path, 'rb') as f:
            conn.storeFile(resource, file_path, f)
        print(f"Archivo subido: {local_file_path} → //{Props.USE_IP}{remote_file_path}")

        conn.close()
        print("Conexion cerrada correctamente.")  