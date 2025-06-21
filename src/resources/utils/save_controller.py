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
        
        # Normalize to no trailing separator
        if remote_directory.endswith(sep):
            remote_directory = remote_directory[:-1]

        # Crear lista de directorios desde la raíz
        dirs = []
        while remote_directory and remote_directory != sep:
            dirs.append(remote_directory)
            remote_directory = remote_directory.rsplit(sep, 1)[0]
        dirs = dirs[::-1]

        for directory in dirs:
            try:
                sftp.stat(directory)
            except FileNotFoundError:
                sftp.mkdir(directory)

    @staticmethod
    def post_file_in_remote(local_file_path: str, remote_file_path: str):
        """
        Post the given resource on the given remote directory.
        Ensures remote directories exist before uploading.
        """

        transport = paramiko.Transport((Props.USE_IP, int(Props.USE_PORT)))
        transport.connect(
            username=Props.USE_USER,
            password=Credentials.decrypt_password(Props.USE_PASSWORD)
        )

        sftp = paramiko.SFTPClient.from_transport(transport)

        remote_dir = remote_file_path.rsplit('\\', 1)[0] if '\\' in remote_file_path else remote_file_path.rsplit('/', 1)[0]

        Save.mkdir_p_remote(sftp, remote_dir)

        sftp.put(localpath=local_file_path, remotepath=remote_file_path)

        sftp.close()
        transport.close()


