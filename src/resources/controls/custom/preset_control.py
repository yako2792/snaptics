import os
import json
import time
import flet as ft

from src.resources.properties import Properties as Props
from src.resources.controls.custom.progress_bar import ProgressBar
from src.motor_controller import StepperMotorController as Motor
from src.camera_controller import GPhoto2 as gphoto2
from src.resources.controls.custom.progress_bar import ProgressBar
from src.resources.controls.custom.image_text_button import ImageTextButton


def is_scanning():
    return Props.IS_SCANNING

def no_camera_selected():
    return not any([Props.CURRENT_USE_CAMERA1, Props.CURRENT_USE_CAMERA2, Props.CURRENT_USE_CAMERA3])

def capture_options_missing():
    return not all([Props.CURRENT_FREQUENCY, Props.CURRENT_FORMAT, Props.CURRENT_RESOLUTION])

class PresetControl(ft.Container):
    """
    A container that provides functionality for managing presets, including
    applying, adding, updating, and deleting presets.

    This class allows the user to interact with preset data, view and modify
    preset settings, and perform actions such as applying or saving new presets
    via the UI controls (dropdowns, text fields, buttons).

    Attributes:
        page (ft.Page): The page object that contains this container.
        presets (dict): A dictionary of existing presets loaded from a JSON file.
        options (ft.Container): A container holding various options for preset configurations.
        camera_use (ft.Container): A container for camera usage settings (checkboxes).
        preset_dropdown (ft.Dropdown): A dropdown to select existing presets.
        preset_name_input (ft.TextField): An input field to enter a new preset name.
        apply_button (ft.ElevatedButton): A button to apply the selected preset.
        add_button (ft.ElevatedButton): A button to add a new preset.
        delete_button (ft.ElevatedButton): A button to delete an existing preset.
        update_button (ft.ElevatedButton): A button to update an existing preset.
    """
    def __init__(self, page: ft.Page, options: ft.Container, camera_use: ft.Container):

        super().__init__()
        self.page = page
        self.presets = self.__load_presets()
        self.motor = Motor(
            dir_pin=Props.DIR_PIN,
            step_pin=Props.STEP_PIN
        )

        # OPTIONS INSTANCES
        self.options = options
        self.camera_use = camera_use

        # INPUT FIELDS
        self.preset_dropdown = ft.Dropdown(
            label="Preset",
            options=[ft.dropdown.Option(name) for name in self.presets],
            width=Props.DROPDOWN_WIDTH,
            border_radius=Props.BORDER_RADIUS
        )
        
        self.preset_name_input = ft.TextField(
            label="Nombre",
            width=Props.DROPDOWN_WIDTH,
            border_radius=Props.BORDER_RADIUS
        )
        # BUTTONS - LEFT
        self.apply_button = ft.ElevatedButton(
            text="Aplicar",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
            height=Props.BUTTON_HEIGHT,
            width=Props.BUTTON_WIDTH,
            on_click=self.__apply_preset
        )

        self.start_button = ft.ElevatedButton(
            text="Comenzar",
            icon=ft.Icons.PLAY_ARROW,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
            height=Props.BUTTON_HEIGHT,
            width=Props.BUTTON_WIDTH,
            on_click=self.__start_button_clicked
        )

        # BUTTONS - RIGHT
        self.add_button = ft.ElevatedButton(
            text="Añadir",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
            height=Props.BUTTON_HEIGHT,
            width=Props.BUTTON_WIDTH,
            on_click=self.__add_preset
        )
        self.delete_button = ft.ElevatedButton(
            text="Borrar",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
            height=Props.BUTTON_HEIGHT,
            width=Props.BUTTON_WIDTH,
            on_click=self.__delete_preset
        )
        self.update_button = ft.ElevatedButton(
            text="Actualizar",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
            height=Props.BUTTON_HEIGHT,
            width=Props.BUTTON_WIDTH,
            on_click=self.__update_preset
        )

        # CONTENT
        self.content = ft.Container(
            ft.Row(
                [
                    ft.Column(
                        [
                            self.preset_dropdown,
                            ft.Row(
                                [
                                    self.apply_button,
                                    self.start_button
                                ]
                            )

                        ],
                        expand=1
                    ),
                    ft.Column(
                        [
                            self.preset_name_input,
                            ft.Row(
                                [
                                    self.add_button,
                                    self.update_button,
                                    self.delete_button
                                ]
                            )

                        ],
                        expand=1
                    )
                ]
            ),
            padding = Props.PAGE_PADDING
        )

        Props.PRESETS = self


    def __load_presets(self):
        """
        Read presets in json file.
        :return: dict with all presets
        """
        if not os.path.exists(Props.PRESETS_PATH):
            with open(Props.PRESETS_PATH, "w") as file:
                json.dump({}, file, indent=2)
            return {}
        with open(Props.PRESETS_PATH, "r") as file:
            return json.load(file)

    def __write_presets(self, presets):
        """
        Writes the provided presets to the JSON file.

        Args:
            presets (dict): A dictionary containing the presets to save.

        Side effects:
            - Saves the given presets dictionary to the file at the path defined in Props.PRESETS_PATH.
        """
        with open(Props.PRESETS_PATH, "w") as file:
            json.dump(presets, file, indent=2)

    def __reload_presets(self):
        """
        Reloads the presets from the JSON file and updates the preset dropdown.

        Side effects:
            - Refreshes the list of presets from the file.
            - Updates the preset dropdown options with the new preset names.
        """
        self.presets = self.__load_presets()
        self.preset_dropdown.options = [ft.dropdown.Option(name) for name in self.presets]

    def __delete_preset(self, e):
        """
        Deletes an existing preset based on the name provided in the input field.

        Args:
            e (ControlEvent): The event triggered when the user clicks "Delete".

        Side effects:
            - Removes the preset from the JSON file if it exists.
            - Displays an alert for success or if the preset was not found.
            - Reloads the preset list and updates the dropdown.
        """
        __preset_name = self.preset_name_input.value
        if not self.__validate_preset_name(__preset_name): return

        # GET CURRENT PRESETS
        presets = self.__load_presets()

        # CHECK IF PRESET EXISTS
        if __preset_name not in presets:
            self.show_alert(f"No existe un preset con el nombre: {__preset_name}")
            return

        # DELETE PRESET
        del presets[__preset_name]

        # WRITE IN JSON FILE
        self.__write_presets(presets)
        self.show_alert(f"Se borró el preset correctamente: {__preset_name}")

        self.__reload_presets()
        self.preset_dropdown.update()

    def __add_preset(self, e):
        """
        Adds a new preset using the current values from UI controls.

        Args:
            e (ControlEvent): The event triggered when the user clicks "Add".

        Side effects:
            - Reads current dropdown and checkbox values.
            - Saves a new preset to the JSON file.
            - Shows an alert if the preset already exists.
            - Refreshes the preset dropdown after adding.
        """
        __preset_name = self.preset_name_input.value
        if not self.__validate_preset_name(__preset_name): return

        # READ PRESETS
        presets = self.__load_presets()

        # READ CURRENT VALUES IN OPTIONS
        __freq = self.options.freq_dropdown.value
        __format = self.options.format_dropdown.value
        __resolution = self.options.resolution_dropdown.value
        __use_camera1 = self.camera_use.camera1_checkbox.content.value
        __use_camera2 = self.camera_use.camera2_checkbox.content.value
        __use_camera3 = self.camera_use.camera3_checkbox.content.value

        # BUILD SETTINGS
        preset_settings = {
            "frequency": __freq,
            "format": __format,
            "resolution": __resolution,
            "use_camera1": __use_camera1,
            "use_camera2": __use_camera2,
            "use_camera3": __use_camera3
        }

        # CHECK IF PRESET EXISTS
        if __preset_name in presets:
            self.show_alert(f"El preset ya existe: {__preset_name}")
            return

        presets[__preset_name] = preset_settings

        # ADD PRESET TO JSON
        self.__write_presets(presets)
        self.show_alert(f"Preset añadido: {__preset_name}")

        self.__reload_presets()
        self.preset_dropdown.update()

    def __update_preset(self, e):
        """
        Updates an existing preset with the current UI control values.

        Args:
            e (ControlEvent): The event triggered when the user clicks "Update".

        Side effects:
            - Reads current values from dropdowns and checkboxes.
            - Replaces the existing preset in the JSON file.
            - Displays a success or error snackbar.
            - Reloads and refreshes the preset dropdown.
        """
        __preset_name = self.preset_name_input.value
        if not self.__validate_preset_name(__preset_name): return

        # READ PRESETS
        presets = self.__load_presets()

        # READ CURRENT VALUES IN OPTIONS
        __freq = self.options.freq_dropdown.value
        __format = self.options.format_dropdown.value
        __resolution = self.options.resolution_dropdown.value
        __use_camera1 = self.camera_use.camera1_checkbox.content.value
        __use_camera2 = self.camera_use.camera2_checkbox.content.value
        __use_camera3 = self.camera_use.camera3_checkbox.content.value

        # BUILD SETTINGS
        preset_settings = {
            "frequency": __freq,
            "format": __format,
            "resolution": __resolution,
            "use_camera1": __use_camera1,
            "use_camera2": __use_camera2,
            "use_camera3": __use_camera3
        }

        # CHECK IF PRESET EXISTS
        if __preset_name not in presets:
            self.show_alert(f"El preset no existe: {__preset_name}")
            return

        # UPDATING PRESET
        presets[__preset_name] = preset_settings

        # ADD PRESET TO JSON
        self.__write_presets(presets)
        self.show_alert(f"Se actualizó el preset correctamente: {__preset_name}")

        self.__reload_presets()
        self.preset_dropdown.update()

    def __apply_preset(self, e):
        """
        Applies the selected preset by updating UI controls and global properties.

        Args:
            e (ControlEvent): The event triggered by the user selecting a preset.

        Side effects:
            - Updates dropdowns and checkboxes based on the preset.
            - Sets corresponding values in the Props class.
            - Displays a confirmation snackbar.
        """
        if self.preset_dropdown.value == None: 
            self.show_alert("Primero selecciona un preset.")
            return

        __preset_name = self.preset_dropdown.value
        # READ PRESETS
        presets = self.__load_presets()
        preset = presets.get(__preset_name)

        # DEFINE FUTURE VALUES IN OPTIONS
        __freq = preset["frequency"]
        __format = preset["format"]
        __resolution = preset["resolution"]
        __use_camera1 = preset["use_camera1"]
        __use_camera2 = preset["use_camera2"]
        __use_camera3 = preset["use_camera3"]

        # MODIFY CURRENT VALUES
        self.options.freq_dropdown.value = __freq
        self.options.format_dropdown.value = __format
        self.options.resolution_dropdown.value = __resolution
        self.camera_use.camera1_checkbox.content.value = __use_camera1
        self.camera_use.camera2_checkbox.content.value = __use_camera2
        self.camera_use.camera3_checkbox.content.value = __use_camera3

        # APPLY CHANGES IN PROPERTIES CLASS
        Props.CURRENT_FREQUENCY = __freq
        Props.CURRENT_FORMAT = __format
        Props.CURRENT_RESOLUTION = __resolution
        Props.CURRENT_USE_CAMERA1 = __use_camera1
        Props.CURRENT_USE_CAMERA2 = __use_camera2
        Props.CURRENT_USE_CAMERA3 = __use_camera3

        self.show_alert(f"Se aplicó el preset correctamente: {__preset_name}")

        # UPDATE PAGE
        self.options.update()
        self.camera_use.update()

    def show_alert(self, message: str):
        """
        Displays a temporary snackbar alert with the given message.

        Args:
            message (str): The message to display in the snackbar.
        """
        snackbar = ft.SnackBar(
            content=ft.Text(value=message),
            duration=2000
        )
        snackbar.open = True
        self.page.open(snackbar)
        self.page.update()

    def __validate_preset_name(self, name: str) -> bool:
        """
        Validates that a preset name is not empty or just whitespace.
        Shows an alert if invalid.

        Args:
            name (str): The preset name to validate.

        Returns:
            bool: True if valid, False if invalid.
        """
        if not name or not name.strip():
            self.show_alert("El nombre del preset está vacío.")
            return False
        return True

    def update_all_radius(self):
        """
        Update border radius of all objects in custom control
        :return:
        """
        self.preset_dropdown.border_radius = Props.BORDER_RADIUS
        self.preset_name_input.border_radius = Props.BORDER_RADIUS
        self.apply_button.style = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS))
        self.add_button.style = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS))
        self.delete_button.style = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS))
        self.update_button.style = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS))

    def __start_button_clicked(self, e):
        # VALIDATIONS
        # Check if there is a scan runnign
        if is_scanning():
            self.show_alert("Espera, se está realizando un escaneo.")
            return

        if not Props.CAMERAS_DICT or all(k is None for k in Props.CAMERAS_DICT.keys()):
            self.show_alert("No hay cámaras conectadas. Por favor, conecta una cámara primero.")
            return

        # Check at least one camera is selected
        if no_camera_selected():
            self.show_alert("Debe seleccionarse al menos una cámara.")
            return
        # Check all capture options are selected
        if capture_options_missing():
            self.show_alert("Hay opciones de captura que faltan.")
            return
        
        # START CAPTURE
        self.show_alert("Captura iniciada.")
        Props.IS_SCANNING = True

        progress_bar = ProgressBar(page=Props.PAGE, title="Escaneo")
        progress_bar.show()

        self.clean_directory()

        match Props.CURRENT_FREQUENCY:
            case "5 [DEG/SHOT]":
                n = 72
                for i in range(0,n):
                    self.motor.move_degs(5)
                    self.trigger_capture(iteration_number = i)

                    progress_bar.update_value(new_value=(1/n)*(i+1))
                    progress_bar.update_legend(new_legend=f"Serie actual: {i + 1}, restante {n - i - 1}.")

            case "45 [DEG/SHOT]":
                n = 8
                for i in range(0,n):
                    self.motor.move_degs(45)
                    self.trigger_capture(iteration_number = i)

                    progress_bar.update_value(new_value=(1/n)*(i+1))
                    progress_bar.update_legend(new_legend=f"Serie actual: {i + 1}, restante {n - i -1}.")

            case "90 [DEG/SHOT]":
                n = 4
                for i in range(0,n):
                    self.motor.move_degs(90)
                    self.trigger_capture(iteration_number = i)

                    progress_bar.update_value(new_value=(1/n)*(i+1))
                    progress_bar.update_legend(new_legend=f"Serie actual: {i + 1}, restante {n - i - 1}.")

            case "360 [DEG/SHOT]":
                self.motor.move_degs(360)
                time.sleep(3)

            case _:
                self.motor.move_degs(360)
                time.sleep(3)


        Props.IS_SCANNING = False
        progress_bar.update_value(new_value=(1))
        progress_bar.update_legend(new_legend=f"Listo!")

        self.show_images_under_cameras()

    def clean_directory(self):
        if Props.CURRENT_USE_CAMERA1:
            for f in os.listdir(Props.CAMERA1_DOWNLOAD_PATH):
                path = os.path.join(Props.CAMERA1_DOWNLOAD_PATH, f)
                os.remove(path) 
        
        if Props.CURRENT_USE_CAMERA2:
            for f in os.listdir(Props.CAMERA2_DOWNLOAD_PATH):
                path = os.path.join(Props.CAMERA2_DOWNLOAD_PATH, f)
                os.remove(path)

        if Props.CURRENT_USE_CAMERA3:
            for f in os.listdir(Props.CAMERA3_DOWNLOAD_PATH):
                path = os.path.join(Props.CAMERA3_DOWNLOAD_PATH, f)
                os.remove(path)
    
    def trigger_capture(self, iteration_number: int) -> None:

        if Props.CURRENT_USE_CAMERA1:
            gphoto2.capture_image(
                camera_port = Props.CAMERAS_DICT[Props.CAMERAS_LIST[0]],
                download_path = Props.CAMERA1_DOWNLOAD_PATH,
                file_name = "A000" + str(iteration_number) + Props.CURRENT_FILE_EXTENSION
            )
        
            time.sleep(0.25)

        if Props.CURRENT_USE_CAMERA2:
            gphoto2.capture_image(
                camera_port = Props.CAMERAS_DICT[Props.CAMERAS_LIST[1]],
                download_path = Props.CAMERA2_DOWNLOAD_PATH,
                file_name = "B000" + str(iteration_number) + Props.CURRENT_FILE_EXTENSION
            )

            time.sleep(0.25)

        if Props.CURRENT_USE_CAMERA3:
            gphoto2.capture_image(
                camera_port = Props.CAMERAS_DICT[Props.CAMERAS_LIST[2]],
                download_path = Props.CAMERA3_DOWNLOAD_PATH,
                file_name = "C000" + str(iteration_number) + Props.CURRENT_FILE_EXTENSION
            )

            time.sleep(0.25)

    
    def show_images_under_cameras(self):
        """
        Show original images under cameras.
        """

        if Props.CURRENT_USE_CAMERA1:
            for f in os.listdir(Props.CAMERA1_DOWNLOAD_PATH):
                image_path = os.path.join(Props.CAMERA1_DOWNLOAD_PATH, f)
                Props.IMAGES_LIST_CAMERA1.append(ImageTextButton(image_path))    

        if Props.CURRENT_USE_CAMERA2:
            for f in os.listdir(Props.CAMERA2_DOWNLOAD_PATH):
                image_path = os.path.join(Props.CAMERA2_DOWNLOAD_PATH, f)
                Props.IMAGES_LIST_CAMERA2.append(ImageTextButton(image_path))  
            
        if Props.CURRENT_USE_CAMERA3:
            for f in os.listdir(Props.CAMERA3_DOWNLOAD_PATH):
                image_path = os.path.join(Props.CAMERA3_DOWNLOAD_PATH, f)
                Props.IMAGES_LIST_CAMERA3.append(ImageTextButton(image_path))  

        Props.EXPLORER_CAMERAS.update_cameras()

    def clear(self):
        self.preset_dropdown.options = []
        self.preset_dropdown.value = None
        self.preset_dropdown.update()
