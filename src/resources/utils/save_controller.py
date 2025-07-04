import paramiko
from src.resources.properties import Properties as Props
from src.resources.utils.credentials_controller import Credentials

class Save:

    @staticmethod
    def mkdir_p_remote(sftp, remote_directory):
        """
        Recursively create remote directories on remote server, works with Windows or Linux paths.
        """
        # Detect separator: si hay backslash, asumimos Windows, sino slash Linux/Unix
        sep = '\\' if '\\' in remote_directory else '/'
        print(f"[mkdir_p_remote] Separador detectado: '{sep}'")
        
        # Normalize to no trailing separator
        if remote_directory.endswith(sep):
            remote_directory = remote_directory[:-1]
            print(f"[mkdir_p_remote] Separador final eliminado: {remote_directory}")

        # Crear lista de directorios desde la raíz
        dirs = []
        while remote_directory and remote_directory != sep:
            dirs.append(remote_directory)
            remote_directory = remote_directory.rsplit(sep, 1)[0]
        dirs = dirs[::-1]
        print(f"[mkdir_p_remote] Directorios a verificar/crear: {dirs}")

        for directory in dirs:
            try:
                sftp.stat(directory)
                print(f"[mkdir_p_remote] Ya existe: {directory}")
            except FileNotFoundError:
                try:
                    sftp.mkdir(directory)
                    print(f"[mkdir_p_remote] Directorio creado: {directory}")
                except Exception as e:
                    print(f"[mkdir_p_remote] Error al crear {directory}: {e}")

    @staticmethod
    def post_file_in_remote(local_file_path: str, remote_file_path: str):
        """
        Post the given resource on the given remote directory.
        Ensures remote directories exist before uploading.
        """
        print(f"[post_file_in_remote] Conectando a {Props.USE_IP}:{Props.USE_PORT} con usuario {Props.USE_USER}")
        transport = paramiko.Transport((Props.USE_IP, int(Props.USE_PORT)))
        transport.connect(
            username=Props.USE_USER,
            password=Credentials.decrypt_password(Props.USE_PASSWORD)
        )
        sftp = paramiko.SFTPClient.from_transport(transport)

        sep = '\\' if '\\' in remote_file_path else '/'
        print(f"[post_file_in_remote] Separador detectado en la ruta remota: '{sep}'")

        if sep == '\\':
            remote_dir = remote_file_path.rsplit('\\', 1)[0]
        else:
            remote_dir = remote_file_path.rsplit('/', 1)[0]


        # remote_dir = remote_file_path.rsplit('\\', 1)[0] if '\\' in remote_file_path else remote_file_path.rsplit('/', 1)[0]

        print(f"[post_file_in_remote] Directorio remoto: {remote_dir}")
        Save.mkdir_p_remote(sftp, remote_dir)

        print(f"[post_file_in_remote] Subiendo {local_file_path} a {remote_file_path}")
        sftp.put(localpath=local_file_path, remotepath=remote_file_path)
        print("[post_file_in_remote] Subida completada")

        sftp.close()
        transport.close()
        print("[post_file_in_remote] Conexión cerrada")


