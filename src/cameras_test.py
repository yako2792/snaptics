import subprocess
import os
import datetime
import time


def get_config(camera: str, config: str) -> dict[str, str]:
    """
    Retrieves the available options for a given configuration (e.g., ISO, shutter speed, image format)
    for a specified camera.

    Args:
        camera (str): The camera port to communicate with.
        config (str): The configuration name (e.g., "iso", "shutterspeed", "imageformat").

    Returns:
        dict[str, str]: A dictionary with the available configuration choices and their corresponding index.

    Raises:
        RuntimeError: If the gphoto2 command fails to execute or return a result.
    """

    result = subprocess.run(
        ['gphoto2', '--port', camera, '--get-config', config],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(f"Error obtaining {config}: {result.stderr.strip()}")

    lines = result.stdout.strip().split('\n')[4:]

    configs = {}

    for line in lines:
        line = line.strip()
        if line.startswith("Choice:"):
            parts = line.split(' ', 2)
            if len(parts) == 3:
                index = int(parts[1])
                value = parts[2].strip()
                configs[value] = str(index)

    return configs

def set_config(camera: str, config: str, set_value: str) -> None:
    """
    Sets a configuration value for a given camera.

    Args:
        camera (str): The camera port to communicate with.
        config (str): The configuration name (e.g., "iso", "shutterspeed", "imageformat").
        set_value (str): The value to set for the specified configuration.

    Returns:
        None
    """

    result = subprocess.run(
        ['gphoto2', '--port', camera, '--set-config', f'{config}={set_value}'],
        capture_output=True,
        text=True
    )
    lines = result.stdout.strip().split('\n')[:]
    for line in lines:
        print(line)

class GPhoto2:
    """
        A class that interacts with a camera (Canon T7) using the gphoto2 command-line utility.

        This class allows for managing camera configurations such as ISO, shutter speed, and image format.
        It also allows capturing images and automatically downloading them.

        Attributes:
        -----------
        cameras (dict[str, str]): A dictionary of available cameras and their corresponding ports.
        default_camera (str): The default camera to use.
        download_path (str): The path where captured images will be saved.
        file_extension (str): The file extension for saved images (".jpg" by default).
        imageformat_dict (dict[str, str]): A dictionary of available image formats.
        iso_dict (dict[str, str]): A dictionary of available ISO values.
        shutterspeed_dict (dict[str, str]): A dictionary of available shutter speeds.

        Methods:
        --------
        _get_camera(camera_port: Optional[str]) -> str:
            Returns the camera port, or the default camera if no port is specified.

        get_models_and_ports() -> dict[str, str]:
            Retrieves all available cameras and their corresponding ports.

        get_available_shutterspeeds_for_camera(camera_port: Optional[str] = None) -> dict[str, str]:
            Retrieves all available shutter speeds for the specified camera.

        get_available_isos_for_camera(camera_port: Optional[str] = None) -> dict[str, str]:
            Retrieves all available ISO values for the specified camera.

        get_available_formats_for_camera(camera_port: Optional[str] = None) -> dict[str, str]:
            Retrieves all available image formats for the specified camera.

        trigger_capture(camera_port: Optional[str] = None) -> None:
            Captures an image and saves it to the specified download path.

        change_image_format(format: str, camera_port: Optional[str] = None) -> None:
            Changes the image format (e.g., RAW or JPEG).

        change_iso(iso: str = "AUTO", camera_port: Optional[str] = None) -> None:
            Changes the ISO value for the camera.

        change_shutterspeed(speed: str = "AUTO", camera_port: Optional[str] = None) -> None:
            Changes the shutter speed for the camera.

        auto_detect() -> None:
            Runs the `--auto-detect` command to list all connected cameras.

        list_cameras() -> None:
            Prints a list of available cameras.
        """
    def __init__(self):
        """
        Initializes the camera control interface, detects connected cameras, and loads available configurations.

        Sets the default camera and retrieves configurations such as available image formats, ISO values, and shutter speeds.
        """
        self.killed_initial_gphoto: bool = self.kill_initial_gphoto()
        self.cameras: dict[str, str] = self.get_models_and_ports()
        self.default_camera: str = self.cameras[next(iter(self.cameras))]
        self.download_path: str = os.getcwd() + "/src/resources/assets/images/"

        self.file_extension: str = ".jpg"

        self.imageformat_dict: dict[str, str] = self.get_available_formats_for_camera(self.default_camera)
        self.iso_dict: dict[str, str] = self.get_available_isos_for_camera(self.default_camera)
        self.shutterspeed_dict: dict[str, str] = self.get_available_shutterspeeds_for_camera(self.default_camera)

    def _get_camera(self, camera_port: str) -> str:
        """
        Returns the camera port, or the default camera if no port is specified.

        Args:
            camera_port (str): The camera port.

        Returns:
            str: The camera port.
        """
        return self.default_camera if camera_port is None else camera_port

    def kill_initial_gphoto(self) -> bool:
        try:
            subprocess.run(['killall', 'gvfsd-gphoto2'])
            return True
        except:
            return False

    def get_models_and_ports(self) -> dict[str, str]:
        """
        Retrieves all available cameras and their corresponding ports.

        Returns:
            dict[str, str]: A dictionary of available camera models and their ports.
        """
        try:
            result = subprocess.run(['gphoto2', '--auto-detect'], capture_output=True, text=True)
            lines = result.stdout.strip().split('\n')[2:]

            cameras: dict[str, str] = {}

            for line in lines:

                if line.strip():
                    parts = line.strip().rsplit('  ', 1)

                    if len(parts) == 2:
                        model, port = parts
                        model = model.strip()
                        port = port.strip()

                        if model in cameras:
                            count = 1
                            new_model = f"{model}({count})"

                            while new_model in cameras:
                                count += 1
                                new_model = f"{model}({count})"
                            model = new_model
                        cameras[model] = port

            return cameras
        
        except:
            return {}

    def get_available_shutterspeeds_for_camera(self, camera_port:str = None) -> dict[str, str]:
        """
        Retrieves all available shutter speeds for the specified camera.

        Args:
            camera_port (str): The camera port (optional).

        Returns:
            dict[str, str]: A dictionary of available shutter speeds.
        """

        __camera: str = self._get_camera(camera_port)

        return get_config(__camera, "shutterspeed")

    def get_available_isos_for_camera(self, camera_port:str = None) -> dict[str, str]:
        """
        Retrieves all available ISO values for the specified camera.

        Args:
            camera_port (str): The camera port (optional).

        Returns:
            dict[str, str]: A dictionary of available ISO values.
        """

        __camera: str = self._get_camera(camera_port)

        return get_config(__camera, "iso")

    def get_available_formats_for_camera(self, camera_port: str = None) -> dict[str, str]:
        """
        Retrieves all available image formats for the specified camera.

        Args:
            camera_port (str): The camera port (optional).

        Returns:
            dict[str, str]: A dictionary of available image formats.
        """

        __camera: str = self._get_camera(camera_port)

        return get_config(__camera, "imageformat")

    def trigger_capture(self, camera_port:str = None) -> None:
        """
        Captures an image and saves it to the specified download path.

        Args:
            camera_port (str): The camera port (optional).

        Returns:
            None
        """

        __camera: str = self._get_camera(camera_port)
        __file_name: str = f"{__camera}_{datetime.datetime.now().strftime('%H-%M-%S')}{self.file_extension}"

        result = subprocess.run(['gphoto2', '--port', __camera, '--capture-image-and-download', f'--filename={self.download_path}{__file_name}'], capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')[:]

        for line in lines:
            print(line)

    def change_image_format(self, format:str, camera_port:str = None) -> None:
        """
        Changes the image format for the camera (e.g., RAW or JPEG).

        Args:
            format (str): The desired image format (e.g., "RAW" or "JPEG").
            camera_port (str): The camera port (optional).

        Returns:
            None
        """

        __camera:str = self._get_camera(camera_port)

        match format:
            case "RAW":
                self.file_extension = ".CR2"
            case _:
                self.file_extension = ".jpg"

        set_config(__camera, "imageformat", self.imageformat_dict[format])

    def change_iso(self, iso:str = "AUTO", camera_port:str = None) -> None:
        """
        Changes the ISO value for the camera.

        Args:
            iso (str): The desired ISO value (default is "AUTO").
            camera_port (str): The camera port (optional).

        Returns:
            None
        """

        __camera:str = self._get_camera(camera_port)

        set_config(__camera, "iso", self.iso_dict[iso])

    def change_shutterspeed(self, speed:str = "AUTO", camera_port:str = None) -> None:
        """
        Changes the shutter speed for the camera.

        Args:
            speed (str): The desired shutter speed (default is "AUTO").
            camera_port (str): The camera port (optional).

        Returns:
            None
        """

        __camera: str = self._get_camera(camera_port)

        set_config(__camera, "shutterspeed", self.shutterspeed_dict[speed])

    def auto_detect(self) -> None:
        """
        Runs the `--auto-detect` command to list all connected cameras.

        Returns:
            None
        """
        result = subprocess.run(['gphoto2', '--auto-detect'], capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')[:]

        for line in lines:
            print(line)

    def list_cameras(self) -> None:
        """
        Prints a list of available cameras and their ports.

        Returns:
            None
        """
        print(self.cameras)

# EXAMPLE OF USAGE
# ----------------------
# cameras = GPhoto2()
# cameras.list_cameras()
# cameras.auto_detect()
# cameras.change_image_format("Small Normal JPEG")
# print(cameras.iso_dict)
# print(cameras.imageformat_dict)
# cameras.change_image_format("Small Normal JPEG")