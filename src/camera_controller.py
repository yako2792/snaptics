import os
import subprocess

class GPhoto2:

    @staticmethod
    def kill_initial_process() -> bool:
        """
        Terminates the initial gphoto2 process (gvfsd-gphoto2) if it's running.

        This method attempts to kill the 'gvfsd-gphoto2' process using the 'killall' command. 
        If the process is successfully terminated, it returns `True`; otherwise, it returns `False`.

        Returns:
            bool: `True` if the process was successfully killed, `False` if an error occurred or the process was not found.
        """
        try:
            subprocess.run(['killall', 'gvfsd-gphoto2'])
            return True
        except:
            return False
        
    @staticmethod
    def __run_command(command: str, capture_output: bool = False, capture_text: bool = False) -> list[str]:
        """
        Runs a gphoto2 shell command and returns the output as a list of lines.

        Args:
            command (str): The full gphoto2 command as a single string.

        Returns:
            list[str]: The stdout output split by line.

        Raises:
            RuntimeError: If the gphoto2 command fails.
        """
        command: list[str] = command.split(' ')

        result = subprocess.run(
            ['gphoto2'] + command,
            capture_output=capture_output,
            text=capture_text
        )

        if capture_output:
            if result.returncode != 0:
                raise RuntimeError(f"Error running command: {command}: {result.stderr.strip()}")
            
            return result.stdout.strip().split('\n')
        else:
            return
    
    @staticmethod
    def get_config(camera_port: str, camera_config: str) -> dict[str, str]:
        """
        Gets camera configuration options as a dictionary.

        Args:
            camera_port (str): The port of the camera.
            config_name (str): The configuration to query (e.g., "iso").

        Returns:
            dict[str, str]: A mapping from option values to their corresponding index, 
                            e.g., {"Auto": "0", "100": "1", ...}.
            
        Raises:
            RuntimeError: If the gphoto2 command fails.
        """

        lines = GPhoto2.__run_command("--port " + camera_port + " --get-config " + camera_config, capture_output=True, capture_text=True)

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
    
    @staticmethod
    def get_cameras() -> dict[str, str]:
        """
        Retrieves all available cameras and their corresponding ports using the gphoto2 command.

        This method runs the `gphoto2 --auto-detect` command to detect cameras connected to the system,
        and returns a dictionary of models and their corresponding ports. If multiple cameras with the same
        model are found, they will be numbered to differentiate them.

        Returns:
            dict[str, str]: A dictionary where the keys are camera model names and the values are the corresponding ports.

        Example:
            {
                "Canon EOS 80D": "usb:001,023",
                "Canon EOS 80D(1)": "usb:001,024"
            }

        Raises:
            RuntimeError: If the gphoto2 command fails to execute or returns an error.
        """
        try:
            # Run the command using the private __run_command method
            lines = GPhoto2.__run_command("--auto-detect", capture_output=True, capture_text=True)
            cameras: dict[str, str] = {}

            # Skip the first two lines, as they are headers
            for line in lines[2:]:
                if line.strip():
                    # Split by double spaces to separate model and port
                    parts = line.strip().rsplit('  ', 1)

                    if len(parts) == 2:
                        model, port = parts
                        model = model.strip()
                        port = port.strip()

                        # Handle duplicate model names by appending a number to them
                        if model in cameras:
                            count = 1
                            new_model = f"{model}({count})"

                            while new_model in cameras:
                                count += 1
                                new_model = f"{model}({count})"
                            model = new_model

                        # Add the model and port to the dictionary
                        cameras[model] = port

            return cameras

        except RuntimeError as e:
            # If an error occurs during the command execution, raise an exception
            raise RuntimeError(f"Failed to retrieve cameras: {str(e)}")

    @staticmethod
    def set_config(camera_port: str, camera_config: str, config_value: str) -> bool:
        """
        Sets a configuration value for the specified camera and returns the status of the operation.

        Args:
            camera_port (str): The port identifier of the camera (e.g., "usb:001,024").
            camera_config (str): The configuration name to set (e.g., "iso", "shutterspeed").
            config_value (str): The value to assign to the configuration.

        Returns:
            bool: True if the configuration was set successfully, False otherwise.
        """
        try:
            GPhoto2.__run_command("--port " + camera_port + " --set-config " + camera_config + "=" + config_value)
            return True
        except:
            return False
    
    @staticmethod
    def capture_image(camera_port: str, download_path: str, file_name: str) -> bool:
        """
        Captures an image from the camera and downloads it to the specified path.

        This method uses the `gphoto2` command-line utility to capture an image from a camera 
        connected to the specified port and save it to the given file path.

        Args:
            camera_port (str): The camera port identifier, e.g., "usb:001,024".
            download_path (str): The directory path where the captured image will be saved.
            file_name (str): The name of the file to save the captured image as.

        Returns:
            bool: `True` if the image was successfully captured and downloaded, `False` otherwise.

        Raises:
            RuntimeError: If the `gphoto2` command fails or there is an error in execution.
        """
        file_path: str = os.path.join(download_path, file_name)

        try:
            GPhoto2.__run_command("--port " + camera_port + " --capture-image-and-download --filename=" + file_path)
            return True
        except:
            return False