import paramiko
from src.resources.properties import Properties as Props
from src.resources.utils.credentials_controller import Credentials

class Save:

    @staticmethod
    def post_file_in_remote(local_file_path: str, remote_file_path: str):
        """
        Post the given resource on the given remote directory.
        """

        if not Props.USE_PATH.endswith('/'):
            Props.USE_PATH += '/'

        transport = paramiko.Transport((Props.USE_SERVER, int(Props.USE_PORT)))
        transport.connect(
            username=Props.USE_USER, 
            password=Credentials.decrypt_password(
                Props.USE_PASSWORD
            )
        )

        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put(localpath=local_file_path, remotepath=remote_file_path)

        sftp.close()
        transport.close()

