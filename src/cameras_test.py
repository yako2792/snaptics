import subprocess
import os
import datetime 
import time

class gphoto2:
    def __init__(self):
        self.cameras = self.get_models_and_ports()
        self.default_camera = self.cameras[next(iter(self.cameras))]
        self.download_path = os.getcwd() + "/src/resources/assets/images/"

        self.file_extension = ".jpg"

        self.imageformat_dict = self.get_available_formats_for_camera(self.default_camera)
        self.iso_dict = self.get_available_isos_for_camera(self.default_camera)


    def get_models_and_ports(self):
        """
        Method to get all available cameras.
        """
        result = subprocess.run(['gphoto2', '--auto-detect'], capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')[2:]
        
        cameras = {}

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
    
    def get_available_isos_for_camera(self, camera_port):
        """
        Method to get all available isos.
        """
        result = subprocess.run(
            ['gphoto2', '--port', camera_port, '--get-config', 'iso'],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise RuntimeError(f"Error obtaining ISO: {result.stderr.strip()}")
        
        lines = result.stdout.strip().split('\n')[4:]
        isos = {}

        for line in lines:
            line = line.strip()
            if line.startswith("Choice:"):
                parts = line.split(' ', 2)
                if len(parts) == 3:
                    index = int(parts[1])
                    valor = parts[2].strip()
                    isos[valor] = index

        return isos

    def get_available_formats_for_camera(self, camera_port):
        """
        Method to get all available imageformats.
        """
        result = subprocess.run(
            ['gphoto2', '--port', camera_port, '--get-config', 'imageformat'],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise RuntimeError(f"Error obtaining IMAGEFORMAT: {result.stderr.strip()}")
        
        lines = result.stdout.strip().split('\n')[4:]
        imageformats = {}

        for line in lines:
            line = line.strip()
            if line.startswith("Choice:"):
                parts = line.split(' ', 2)
                if len(parts) == 3:
                    index = int(parts[1])
                    valor = parts[2].strip()
                    imageformats[valor] = index

        return imageformats

    def trigger_capture(self, camera = None):
        """
        Method to capture images and download them to `self.download_path``.
        """

        __file_name = f"test_{datetime.datetime.now().strftime('%H-%M-%S')}{self.file_extension}"

        if camera == None:
            __camera = self.default_camera

        result = subprocess.run(['gphoto2', '--capture-image-and-download', f'--filename={self.download_path}{__file_name}'], capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')[:]

        for line in lines:
            print(line)

    def change_image_format(self, format):
        """
        Method to change image capture format between
        """
        match format:
            case "RAW":
                self.file_extension = ".CR2"
            case _:
                self.file_extension = ".jpg"
        
        result = subprocess.run(['gphoto2', '--set-config', f'imageformat={self.imageformat_dict[format]}'], capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')[:]

        for line in lines:
            print(line)

    def change_iso(self, iso):
        """
        Method to change iso value.
        """
        match format:
            case "RAW":
                self.file_extension = ".CR2"
            case _:
                self.file_extension = ".jpg"
        
        result = subprocess.run(['gphoto2', '--set-config', f'iso={self.imageformat_dict[format]}'], capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')[:]

        for line in lines:
            print(line)


    def auto_detect(self):
        """
        Method to reproduce --auto-detect command.
        """
        result = subprocess.run(['gphoto2', '--auto-detect'], capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')[:]

        for line in lines:
            print(line)
    
    def list_cameras(self):
        """
        Method to print available cameras for usage.
        """
        print(self.cameras)

cameras = gphoto2()
#cameras.list_cameras()
#cameras.auto_detect()
#cameras.change_image_format("Small Normal JPEG")
print(cameras.iso_dict)
print(cameras.imageformat_dict)
cameras.change_image_format("Small Normal JPEG")