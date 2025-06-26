import os
import time
import json
import flet as ft
from src.resources.utils.routines_controller import Routines
from src.resources.controls.custom.header_control import HeaderControl
from src.resources.properties import Properties as Props
from src.resources.controls.custom.stages.stage_scan import StageScan
from src.resources.controls.custom.stages.stage_filter import StageFilter
from src.resources.controls.custom.stages.stage_save import StageSave
from src.camera_controller import GPhoto2 as gphoto2
from src.motor_controller import StepperMotorController as Motor
from src.resources.controls.filters.filters import Filter
from src.resources.controls.custom.progress_bar import ProgressBar
from src.camera_controller import GPhoto2 as gp
from src.resources.controls.custom.loading_dialog import LoadingDialog
from src.resources.utils.save_controller import Save

class RoutinesTab(ft.Tab):
    """
    Routines tab in Workspace frame
    """

    def __init__(self, page: ft.Page, title: str):
        super().__init__()
        self.page = page
        self.progress_bar = ProgressBar(
            page=self.page,
            title = f"Rutina: {Props.CURRENT_ROUTINE['name']}"
        )
        self.text = title
        self.motor = Motor(
            dir_pin=Props.DIR_PIN,
            step_pin=Props.STEP_PIN
        )

        self.icon = ft.Icon(ft.Icons.CONSTRUCTION, size=Props.TAB_ICON_SIZE, visible=Props.TAB_ICON_ENABLED)

        # region Tab: Controls
        self.stage_type_dropdown = ft.Dropdown(
            options=[
                ft.DropdownOption(text="Scan"),
                ft.DropdownOption(text="Filter"),
                ft.DropdownOption(text="Save")
            ],
            value=None,
            label="Tipo",
            width = Props.CHECKBOX_WIDTH,
            border_radius = Props.BORDER_RADIUS,
        )

        self.add_stage_button = ft.ElevatedButton(
            text="Añadir",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
            height=Props.BUTTON_HEIGHT,
            width=Props.BUTTON_WIDTH,
            on_click=self.__add_stage_button_clicked
        )

        self.start_routine_button = ft.Container(
            height=Props.BUTTON_HEIGHT,
            expand=True,
            content=ft.ElevatedButton(
                text="Comenzar",
                icon=ft.Icons.PLAY_ARROW,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
                height=Props.BUTTON_HEIGHT,
                width=Props.BUTTON_WIDTH,
                on_click=self.__start_routine_button_clicked
            )
        )

        self.stages_list_container = ft.Container(
            expand = 1,
            content = ft.Column(
                controls = [],
                scroll = ft.ScrollMode.AUTO
            )
        )

        self.routine_loader_dropdown = ft.Dropdown(
            options=self.__get_available_routines(),
            value=None,
            label="Nombre",
            width = Props.CHECKBOX_WIDTH,
            border_radius = Props.BORDER_RADIUS
        )

        self.apply_routine_button = ft.ElevatedButton(
            text="Aplicar",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
            height=Props.BUTTON_HEIGHT,
            width=Props.BUTTON_WIDTH,
            on_click=self.__apply_routine_button_clicked
        )

        self.routine_name_input = ft.TextField(
            label="Nombre",
            width=Props.DROPDOWN_WIDTH,
            border_radius=Props.BORDER_RADIUS,
            on_change=self.__routine_name_input_changed 
        )

        self.add_new_routine_button = ft.ElevatedButton(
            text="Añadir",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
            height=Props.BUTTON_HEIGHT,
            width=Props.BUTTON_WIDTH,
            on_click=self.__add_new_routine_button_clicked
        )

        self.update_routine_button = ft.ElevatedButton(
            text="Actualizar",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
            height=Props.BUTTON_HEIGHT,
            width=Props.BUTTON_WIDTH,
            on_click=self.__update_routine_button_clicked
        )

        self.delete_routine_button = ft.ElevatedButton(
            text="Borrar",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
            height=Props.BUTTON_HEIGHT,
            width=Props.BUTTON_WIDTH,
            on_click=self.__delete_routine_button_clicked
        )
        # endregion

        # region Tabs: Content
        self.content = ft.Container(
            padding = Props.TAB_PADDING,
            content = ft.Column(
                [
                    # Stages: Selector
                    HeaderControl("Etapas"),
                    ft.Row(
                        [
                            self.stage_type_dropdown,
                            self.add_stage_button
                        ]
                    ),
                    
                    # Stages: List
                    self.stages_list_container,
                    
                    # Stages: Routine saver
                    HeaderControl("Rutina"),
                    ft.Row(
                        [   
                            # Routine saver: Left
                            ft.Column(
                                [
                                    self.routine_loader_dropdown,
                                    ft.Row(
                                        [
                                            self.apply_routine_button,
                                            self.start_routine_button
                                        ]
                                    )
                                ]
                            ),

                            # Routine saver: Right
                            ft.Column(
                                [
                                    self.routine_name_input,
                                    ft.Row(
                                        [
                                            self.add_new_routine_button,
                                            self.update_routine_button,
                                            self.delete_routine_button
                                        ]
                                    )
                                ]
                            )
                        ]
                    )

                ]
            )
        )
        # endregion

        Props.ROUTINES = self

    # region Controllers
    def __add_stage_button_clicked(self, e):
        # Validations
        stage_value = self.stage_type_dropdown.value
        Props.STAGES_NUMBER += 1

        if (stage_value == None):
            self.show_alert("Selecciona una etapa para continuar.")
            return
        
        # Add stage
        match stage_value:
            case "Scan":
                self.stages_list_container.content.controls.append(
                    StageScan(
                        stage_number = Props.STAGES_NUMBER,
                        card_list = self.stages_list_container
                    )
                )
                self.stages_list_container.content.update()

            case "Filter":
                self.stages_list_container.content.controls.append(
                    StageFilter(
                        stage_number = Props.STAGES_NUMBER,
                        card_list = self.stages_list_container
                    )
                )
                self.stages_list_container.content.update()

            case "Save":
                self.stages_list_container.content.controls.append(
                    StageSave(
                        stage_number = Props.STAGES_NUMBER,
                        card_list = self.stages_list_container
                    )
                )
                self.stages_list_container.content.update()

            case _:
                self.show_alert("Unrecognized stage type: " + stage_value)
                return
        
        # Modify current routine json
        Props.CURRENT_ROUTINE["stages"] += [
            {
                "type": stage_value,
                "config": {}
            }
        ]

    def __apply_routine_button_clicked(self, e):
        """ Applies the selected routine to the current stages list.
        Validates if the routine exists and if it has stages.
        If the routine is valid, it loads the stages and applies the configurations.
        """
        # Reset current stages list
        Props.STAGES_NUMBER = 0
        Props.CURRENT_ROUTINE["stages"] = []
        Props.CURRENT_ROUTINE["name"] = None
        
        self.stages_list_container.content.controls = []
        routine_name = self.routine_loader_dropdown.value
        
        if routine_name in ("", None, " "):
            self.show_alert("Por favor, selecciona una rutina para aplicar.")
            return
        if routine_name not in Routines.get_available_routines():
            self.show_alert("La rutina no existe: " + routine_name)
            return
        # Load routine

        stages = Routines.get_stages_in_routine(routine_name=routine_name)

        if stages == []:
            self.show_alert("La rutina no tiene etapas: " + routine_name)
            return
        # Reset current routine
        Props.CURRENT_ROUTINE["name"] = routine_name

        loading_dialog = LoadingDialog(page=Props.PAGE, title="Espera")
        loading_dialog.show()
        loading_dialog.update_legend(f"Aplicando rutina: {routine_name}")

        for i in range(len(stages), 0, -1):
            Props.STAGES_NUMBER += 1

            stage_config = Routines.get_stage_config(routine_name=routine_name,stage_number=Props.STAGES_NUMBER)

            current_stage_card = None
            stage_type = Routines.get_stage_type(routine_name=routine_name, stage_number=Props.STAGES_NUMBER)
            
            loading_dialog.update_legend(f"Añadiendo etapa {Props.STAGES_NUMBER}: {stage_type}")

            match stage_type:
                case "Scan":
                    # Create the card
                    current_stage_card = StageScan(
                        stage_number = Props.STAGES_NUMBER,
                        card_list = self.stages_list_container
                    )
                    
                    # Modify current values and apply
                    loading_dialog.update_legend(f"Cargando presets...")
                    current_stage_card.preset_dropdown.value = stage_config.get("preset_name")
                    presets  = self.__load_presets()

                    # Add capture values 
                    loading_dialog.update_legend(f"Aplicando preset a las cámaras.")
                    preset = presets.get(stage_config.get("preset_name"))
                    if preset is None:
                        self.show_alert(f"Preset '{stage_config.get('preset_name')}' no encontrado. Por favor, verifica la configuración de tu rutina.")
                    else:
                        Props.CURRENT_FREQUENCY = preset["frequency"]
                        Props.CURRENT_FORMAT = preset["format"]
                        Props.CURRENT_RESOLUTION = preset["resolution"]
                        Props.CURRENT_USE_CAMERA1 = preset["use_camera1"]
                        Props.CURRENT_USE_CAMERA2 = preset["use_camera2"]
                        Props.CURRENT_USE_CAMERA3 = preset["use_camera3"]

                    for camera in Props.CAMERAS_LIST:
                        if camera == None:
                            continue
                        
                        loading_dialog.update_legend(f"Aplicando configuración a la cámara: {camera}")
                        gp.set_config(
                            camera_port=Props.CAMERAS_DICT[camera],
                            camera_config=Props.FORMAT_CAMERA_CONFIG,
                            config_value=Props.FORMATS_DICT[Props.CURRENT_FORMAT]
                        )
                        loading_dialog.update_legend(f"Aplicando configuración de formato: {Props.FORMAT_CAMERA_CONFIG}")

                        gp.set_config(
                            camera_port=Props.CAMERAS_DICT[camera],
                            camera_config=Props.RESOLUTION_CAMERA_CONFIG,
                            config_value=Props.RESOLUTIONS_DICT[Props.CURRENT_RESOLUTION]
                        )
                        loading_dialog.update_legend(f"Aplicando configuración de resolución: {Props.RESOLUTION_CAMERA_CONFIG}")

                    
                    loading_dialog.update_legend(f"Configuración aplicada correctamente!")

                    # Modify values on backend
                    Props.CURRENT_ROUTINE["stages"].append(
                        {
                            "type": stage_type,
                            "config": stage_config
                        }
                    )

                case "Filter":
                    current_stage_card = StageFilter(
                        stage_number = Props.STAGES_NUMBER,
                        card_list = self.stages_list_container
                    )

                    # Modify current values and apply
                    current_stage_card.filter_dropdown.value = stage_config.get('filter_name')
                    # print(f"Assigned {stage_config['filter_name']} to Scan card")

                    Props.CURRENT_ROUTINE["stages"].append(
                        {
                            "type": stage_type,
                            "config": stage_config
                        }
                    )  

                case "Save":
                    current_stage_card = StageSave(
                        stage_number = Props.STAGES_NUMBER,
                        card_list = self.stages_list_container
                    )

                    current_stage_card.server_dropdown.value = stage_config.get("server_name")
                    current_stage_card.path_dropdown.value = stage_config.get("path")
                    current_stage_card.credentials_dropdown.value = stage_config.get("credentials", {}).get("user", "")
                    # print(f"Assigned {stage_config['save_path']} to Scan card")

                    Props.CURRENT_ROUTINE["stages"].append(
                        {
                            "type": stage_type,
                            "config": stage_config
                        }
                    )  

                case _:
                    # Unrecognized stage type
                    loading_dialog.update_legend(f"Tipo de etapa no reconocido: {stage_type}")
                    self.show_alert("Tipo de etapa no reconocido: " + stage_type)
                    continue
            
            loading_dialog.update_legend(f"Listo!")
            loading_dialog.hide()

            self.stages_list_container.content.controls.append(
                current_stage_card
            )
        
        print(Props.CURRENT_ROUTINE)
        self.stages_list_container.content.update()
        self.show_alert("Rutina aplicada: " + routine_name)

    def __add_new_routine_button_clicked(self, e):

        Props.CURRENT_ROUTINE["name"] = self.routine_name_input.value

        routine_name = Props.CURRENT_ROUTINE["name"]
        stages = Props.CURRENT_ROUTINE["stages"]

        # Validations
        if stages == []:
            self.show_alert("Por favor, añade al menos una etapa a la rutina.")
            return
        if routine_name in ("", None, " "):
            self.show_alert("Por favor, ingresa un nombre de rutina para añadir.")
            return
        if routine_name in Routines.get_available_routines():
            self.show_alert("La rutina ya existe: " + routine_name)
            return

        Routines.add_routine(routine_name=routine_name, stages=stages)

        self.routine_loader_dropdown.options = self.__get_available_routines()
        self.routine_loader_dropdown.update()
        self.show_alert("Rutina añadida: " + routine_name)

    def __update_routine_button_clicked(self, e):

        routine_name = Props.CURRENT_ROUTINE["name"]
        stages = Props.CURRENT_ROUTINE["stages"]

        if routine_name in ("", None, " "):
            self.show_alert("Por favor, introduce una rutina para actualizar.")
            return
        if routine_name not in Routines.get_available_routines():
            self.show_alert("La rutina no existe: " + routine_name)
            return
        # Update routine

        Routines.update_routine(routine_name=routine_name, stages=stages)
        self.show_alert("Rutina actualizada: " + routine_name)
    
    def __delete_routine_button_clicked(self, e):
        
        routine_name = self.routine_name_input.value
        if routine_name in ("", None, " "):
            self.show_alert("Por favor, introduce una rutina para borrar.")
            return
        
        if routine_name not in Routines.get_available_routines():
            self.show_alert("La rutina no existe: " + routine_name)
            return
        
        # Delete routine
        try:
            Routines.remove_routine(routine_name=routine_name)
            self.routine_loader_dropdown.options = self.__get_available_routines()
            self.routine_loader_dropdown.update()
        except:
            self.show_alert("Hubo un problema al borrar la rutina o ya había sido borrada: " + routine_name)

        self.show_alert("Rutina borrada: " + routine_name)

    def __get_available_routines(self) -> list[ft.DropdownOption]:
        routines_list = []

        available_routines = Routines.get_available_routines()

        for routine in available_routines:
            routines_list.append(
                ft.DropdownOption(
                    text=str(routine)
                )
            )

        return routines_list
    
    def __routine_name_input_changed(self, e):
        Props.CURRENT_ROUTINE["name"] = self.routine_name_input.value
    
    def __start_routine_button_clicked(self, e):
        if Props.CURRENT_ROUTINE["stages"] == []:
            self.show_alert("Por favor, añade al menos una etapa.")
            return
        
        self.progress_bar.percentage.value = "0%"
        self.progress_bar.show()

        # Check the amout of stages
        total_stages = len(Props.CURRENT_ROUTINE["stages"])
        current_stage_num = 1

        for stage in Props.CURRENT_ROUTINE["stages"]:
            match stage["type"]:
                case "Scan":
                    Props.IS_SCANNING = True

                    self.progress_bar.update_legend("Scan: Cargando...")
                    self.__start_scan(stage=stage)
                    self.progress_bar.update_legend("Scan: Listo...")
                    self.progress_bar.update_value(new_value=(1/total_stages)*(current_stage_num))

                    current_stage_num += 1

                    Props.IS_SCANNING = False
                
                case "Filter":
                    Props.IS_FILTERING = True

                    self.progress_bar.update_legend("Filter: Cargando...")
                    self.__start_filter(stage=stage)
                    Props.APPEND_FILTER = True
                    self.progress_bar.update_legend("Filter: Listo...")
                    self.progress_bar.update_value(new_value=(1/total_stages)*(current_stage_num))

                    current_stage_num += 1

                    Props.IS_FILTERING = False

                case "Save":
                    Props.IS_SAVING = True

                    self.progress_bar.update_legend("Save: Cargando...")
                    self.__start_save(stage=stage)
                    self.progress_bar.update_legend("Save: Listo...")
                    self.progress_bar.update_value(new_value=(1/total_stages)*(current_stage_num))

                    
                    # Clean filtered directory if not appending
                    Props.APPEND_FILTER = False
                    self.clean_directory_filtered()

                    current_stage_num += 1

                    Props.IS_SAVING = False

                case _:
                    pass
        
        self.progress_bar.update_value(new_value=(1))
        self.progress_bar.update_legend(new_legend=f"Listo.")
        Props.APPEND_FILTER = False
    
    def __start_scan(self, stage):
        # Load preset
        preset_name = stage["config"]["preset_name"]
        presets = self.__load_presets()
        preset = presets.get(preset_name)

        # APPLY VALUES
        # DEFINE FUTURE VALUES IN OPTIONS
        __freq = preset["frequency"]
        __format = preset["format"]
        __resolution = preset["resolution"]
        __use_camera1 = preset["use_camera1"]
        __use_camera2 = preset["use_camera2"]
        __use_camera3 = preset["use_camera3"]

        # MODIFY CURRENT VALUES
        Props.OPTIONS_CONTROL.freq_dropdown.value = __freq
        Props.OPTIONS_CONTROL.format_dropdown.value = __format
        Props.OPTIONS_CONTROL.resolution_dropdown.value = __resolution
        Props.USE_CONTROL.camera1_checkbox.content.value = __use_camera1
        Props.USE_CONTROL.camera2_checkbox.content.value = __use_camera2
        Props.USE_CONTROL.camera3_checkbox.content.value = __use_camera3

        # APPLY CHANGES IN PROPERTIES CLASS
        Props.CURRENT_FREQUENCY = __freq
        Props.CURRENT_FORMAT = __format
        Props.CURRENT_RESOLUTION = __resolution
        Props.CURRENT_USE_CAMERA1 = __use_camera1
        Props.CURRENT_USE_CAMERA2 = __use_camera2
        Props.CURRENT_USE_CAMERA3 = __use_camera3

        self.clean_directory()

        # START CAPTURE
        match Props.CURRENT_FREQUENCY:
            case "5 [DEG/SHOT]":
                n = 72
                for i in range(0,n):
                    
                    # Prefix
                    match i:
                        case 8:
                            Props.LETTER_PREFIX = "A"
                        case 17:
                            Props.LETTER_PREFIX = "B"
                        case 71:
                            Props.LETTER_PREFIX = "C"
                        case 35:
                            Props.LETTER_PREFIX = "D"
                        case 53:
                            Props.LETTER_PREFIX = "E"
                        case _:
                            Props.LETTER_PREFIX = ""


                    self.motor.move_degs(5)
                    self.trigger_capture(iteration_number = i)
                    self.progress_bar.update_legend(new_legend=f"Scan: Serie actual: {i + 1}, restante {n - i - 1}")

            case "45 [DEG/SHOT]":
                n = 8
                for i in range(0,n):

                    # Prefix
                    match i:
                        case 0:
                            Props.LETTER_PREFIX = "A"
                        case 1:
                            Props.LETTER_PREFIX = "B"
                        case 7:
                            Props.LETTER_PREFIX = "C"
                        case 3:
                            Props.LETTER_PREFIX = "D"
                        case 5:
                            Props.LETTER_PREFIX = "E"
                        case _:
                            Props.LETTER_PREFIX = ""

                    self.motor.move_degs(45)
                    self.trigger_capture(iteration_number = i)
                    self.progress_bar.update_legend(new_legend=f"Scan: Serie actual: {i + 1}, restante {n - i - 1}")

            case "90 [DEG/SHOT]":
                n = 4
                for i in range(0,n):

                    # Prefix
                    match i:
                        case 0:
                            Props.LETTER_PREFIX = "B"
                        case 3:
                            Props.LETTER_PREFIX = "C"
                        case 1:
                            Props.LETTER_PREFIX = "D"
                        case 2:
                            Props.LETTER_PREFIX = "E"
                        case _:
                            Props.LETTER_PREFIX = ""
                    
                    self.motor.move_degs(90)
                    self.trigger_capture(iteration_number = i)
                    self.progress_bar.update_legend(new_legend=f"Scan: Serie actual: {i + 1}, restante {n - i - 1}")

            case "360 [DEG/SHOT]":
                self.motor.move_degs(360)
                time.sleep(3)

            case _:
                self.motor.move_degs(360)
                time.sleep(3)

    def __start_filter(self, stage):

        filter_to_apply = stage["config"]["filter_name"]
        images_to_filter = []

        if Props.APPEND_FILTER:
            for f in os.listdir(Props.FILTERED_IMAGES_DIRECTORY):
                image_path = os.path.join(Props.FILTERED_IMAGES_DIRECTORY, f)
                images_to_filter.append(image_path)
        else: 
            if Props.CURRENT_USE_CAMERA1:
                for f in os.listdir(Props.CAMERA1_DOWNLOAD_PATH):
                    image_path = os.path.join(Props.CAMERA1_DOWNLOAD_PATH, f)
                    images_to_filter.append(image_path)

            if Props.CURRENT_USE_CAMERA2:
                for f in os.listdir(Props.CAMERA2_DOWNLOAD_PATH):
                    image_path = os.path.join(Props.CAMERA2_DOWNLOAD_PATH, f)
                    images_to_filter.append(image_path)
            
            if Props.CURRENT_USE_CAMERA3:
                for f in os.listdir(Props.CAMERA3_DOWNLOAD_PATH):
                    image_path = os.path.join(Props.CAMERA3_DOWNLOAD_PATH, f)
                    images_to_filter.append(image_path)

        total_images = len(images_to_filter)
        filtered_images = 0
        self.progress_bar.update_legend(new_legend=f"Filter: Se encontraron {total_images} imágenes para filtrar.")

        for image in images_to_filter:
            print(image)
            file_name = os.path.basename(image)
            print(file_name)
            file_path = Props.FILTERED_IMAGES_DIRECTORY + file_name
            filtered_images += 1
            self.progress_bar.update_legend(new_legend=f"Filter: Aplicando filtro a imagen {file_name}, imágenes restantes {total_images - filtered_images}.")

            match filter_to_apply:
                case "Remove background":
                    print("Aplicando filtro a " + image)
                    
                    Filter.remove_background(
                        image_path=image,
                        output_path=file_path
                    )

                case "Resize image":
                    print("Aplicando filtro a " + image)
                    Filter.resize_image(
                        image_path=image,
                        output_path=file_path
                    )
                
                case "Fisheye correction":
                    print("Aplicando filtro a " + image)
                    Filter.resize_image(
                        image_path=image,
                        output_path=file_path
                    )

                case "CA Correction":
                    print("Aplicando filtro a " + image)
                    Filter.ca_correction(
                        image_path=image,
                        output_path=file_path
                    )
                
                case "Crop Center":

                    (width, height) = Props.CROP_RESLUTIONS.get(
                        stage["config"].get("resolution"))

                    print("Aplicando filtro a " + image)
                    Filter.crop_center_object(
                        image_path=image,
                        output_path=file_path,
                        width=width,
                        height=height,
                    )
                
                case _:
                    pass

    def __start_save(self, stage):

        self.progress_bar.update_legend(new_legend=f"Save: Preparando para guardar archivos en el servidor remoto {Props.USE_SERVER}.")

        # GET IMAGES TO TRANSFER
        images_to_transfer = []
        print(f"Images to transfer before: {images_to_transfer}")

        if Props.APPEND_FILTER:
            for f in os.listdir(Props.FILTERED_IMAGES_DIRECTORY):
                if not f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif')):
                    continue  # Skip non-image files
                image_path = os.path.join(Props.FILTERED_IMAGES_DIRECTORY, f)
                images_to_transfer.append(image_path)
        else: 
            if Props.CURRENT_USE_CAMERA1:
                for f in os.listdir(Props.CAMERA1_DOWNLOAD_PATH):
                    if not f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif')):
                        continue  # Skip non-image files
                    image_path = os.path.join(Props.CAMERA1_DOWNLOAD_PATH, f)
                    images_to_transfer.append(image_path)

            if Props.CURRENT_USE_CAMERA2:
                for f in os.listdir(Props.CAMERA2_DOWNLOAD_PATH):
                    if not f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif')):
                        continue  # Skip non-image files
                    image_path = os.path.join(Props.CAMERA2_DOWNLOAD_PATH, f)
                    images_to_transfer.append(image_path)
            
            if Props.CURRENT_USE_CAMERA3:
                for f in os.listdir(Props.CAMERA3_DOWNLOAD_PATH):
                    if not f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif')):
                        continue  # Skip non-image files
                    image_path = os.path.join(Props.CAMERA3_DOWNLOAD_PATH, f)
                    images_to_transfer.append(image_path)

        print(f"Images to transfer after: {images_to_transfer}")

        Props.USE_PATH = stage["config"]["path"]

        # TRANSFER IMAGES
        total_images = len(images_to_transfer)
        print(f"Total images: {total_images}")
        for image_file_path in images_to_transfer:
            file_name = os.path.basename(image_file_path)
            total_images-=1

            if file_name == ".gitkeep":
                continue

            print(f"Sending image: {file_name}")
            self.progress_bar.update_legend(new_legend=f"Save: Guardando imagen {file_name}, restantes {total_images}.")

            if not Props.USE_PATH.endswith('/'):
                Props.USE_PATH += '/'
                
            print(f"Remote file path: {Props.USE_PATH + '/' + Props.PRODUCT_ID + '/' + file_name}")

            Save.post_file_in_remote(
                local_file_path=image_file_path,
                remote_file_path=Props.USE_PATH + '/' + Props.PRODUCT_ID + '/' + file_name
            )

        self.progress_bar.update_legend(new_legend=f"Save: Proceso de guardado de imagen completado.")
    
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
        
        pass
    
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
    
    def clean_directory_filtered(self):
        for f in os.listdir(Props.FILTERED_IMAGES_DIRECTORY):
            path = os.path.join(Props.FILTERED_IMAGES_DIRECTORY, f)
            os.remove(path) 

    def trigger_capture(self, iteration_number: int) -> None:
        if Props.CURRENT_USE_CAMERA1:
            local_prefix = "" if Props.LETTER_PREFIX in ("A","F") else Props.LETTER_PREFIX
            gphoto2.capture_image(
                camera_port = Props.CAMERAS_DICT[Props.CAMERAS_LIST[0]],
                download_path = Props.CAMERA1_DOWNLOAD_PATH,
                file_name = Props.PRODUCT_ID + str(iteration_number) + local_prefix + Props.CURRENT_FILE_EXTENSION
            )

        if Props.CURRENT_USE_CAMERA2:
            local_prefix = "A" if Props.LETTER_PREFIX == "A" else ""
            gphoto2.capture_image(
                camera_port = Props.CAMERAS_DICT[Props.CAMERAS_LIST[1]],
                download_path = Props.CAMERA2_DOWNLOAD_PATH,
                file_name = Props.PRODUCT_ID + str(iteration_number) + local_prefix + Props.CURRENT_FILE_EXTENSION
            )

        if Props.CURRENT_USE_CAMERA3:
            local_prefix = "F" if Props.LETTER_PREFIX == "C" else ""
            gphoto2.capture_image(
                camera_port = Props.CAMERAS_DICT[Props.CAMERAS_LIST[2]],
                download_path = Props.CAMERA3_DOWNLOAD_PATH,
                file_name = Props.PRODUCT_ID + str(iteration_number) + local_prefix + Props.CURRENT_FILE_EXTENSION
            )

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
    
    def clear(self):
        """
        Clears the current routine and resets the stages list.
        """
        Props.STAGES_NUMBER = 0
        Props.CURRENT_ROUTINE["stages"] = []
        Props.CURRENT_ROUTINE["name"] = None
        self.stages_list_container.content.controls = []
        self.stages_list_container.content.update()
        self.routine_loader_dropdown.options = self.__get_available_routines()
        self.routine_loader_dropdown.update()
        self.routine_loader_dropdown.value = None

    # endregion
