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
from src.resources.controls.filters.filter import Filter


class RoutinesTab(ft.Tab):
    """
    Routines tab in Workspace frame
    """

    def __init__(self, page: ft.Page, title: str):
        super().__init__()
        self.page = page
        self.text = title
        self.motor = Motor(dir_pin=10, step_pin=8)
        self.icon = ft.Icon(ft.Icons.CONSTRUCTION, size=Props.TAB_ICON_SIZE, visible=Props.TAB_ICON_ENABLED)

        # region Tab: Controls
        self.stage_type_dropdown = ft.Dropdown(
            options=[
                ft.DropdownOption(text="Scan"),
                ft.DropdownOption(text="Filter"),
                ft.DropdownOption(text="Save")
            ],
            value=None,
            label="Type",
            width = Props.CHECKBOX_WIDTH,
            border_radius = Props.BORDER_RADIUS,
        )

        self.add_stage_button = ft.ElevatedButton(
            text="Add",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
            height=Props.BUTTON_HEIGHT,
            width=Props.BUTTON_WIDTH,
            on_click=self.__add_stage_button_clicked
        )

        self.start_routine_button = ft.Container(
            height=Props.BUTTON_HEIGHT,
            expand=True,
            content=ft.ElevatedButton(
                text="Start",
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
            label="Name",
            width = Props.CHECKBOX_WIDTH,
            border_radius = Props.BORDER_RADIUS
        )

        self.apply_routine_button = ft.ElevatedButton(
            text="Apply",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
            height=Props.BUTTON_HEIGHT,
            width=Props.BUTTON_WIDTH,
            on_click=self.__apply_routine_button_clicked
        )

        self.routine_name_input = ft.TextField(
            label="Name",
            width=Props.DROPDOWN_WIDTH,
            border_radius=Props.BORDER_RADIUS,
            on_change=self.__routine_name_input_changed 
        )

        self.add_new_routine_button = ft.ElevatedButton(
            text="Add",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
            height=Props.BUTTON_HEIGHT,
            width=Props.BUTTON_WIDTH,
            on_click=self.__add_new_routine_button_clicked
        )

        self.update_routine_button = ft.ElevatedButton(
            text="Update",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
            height=Props.BUTTON_HEIGHT,
            width=Props.BUTTON_WIDTH,
            on_click=self.__update_routine_button_clicked
        )

        self.delete_routine_button = ft.ElevatedButton(
            text="Delete",
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
                    HeaderControl("Stages"),
                    ft.Row(
                        [
                            self.stage_type_dropdown,
                            self.add_stage_button
                        ]
                    ),
                    
                    # Stages: List
                    self.stages_list_container,
                    
                    # Stages: Routine saver
                    HeaderControl("Routine"),
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

    # region Controllers
    def __add_stage_button_clicked(self, e):
        # Validations
        stage_value = self.stage_type_dropdown.value
        Props.STAGES_NUMBER += 1

        if (stage_value == None):
            self.show_alert("Select a stage type to continue.")
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
        
        self.stages_list_container.content.controls = []
        routine_name = self.routine_loader_dropdown.value
        

        try:
            stages = Routines.get_stages_in_routine(routine_name=routine_name)
        except:
            self.show_alert("Issue loading routine, or routine does not exists: " + routine_name)
            return
        
        Props.STAGES_NUMBER = 0
        Props.CURRENT_ROUTINE["stages"] = []
        Props.CURRENT_ROUTINE["name"] = routine_name

        for i in range(len(stages), 0, -1):
            Props.STAGES_NUMBER += 1

            stage_config = Routines.get_stage_config(routine_name=routine_name,stage_number=Props.STAGES_NUMBER)

            current_stage_card = None
            stage_type = Routines.get_stage_type(routine_name=routine_name, stage_number=Props.STAGES_NUMBER)

            match stage_type:
                case "Scan":
                    # Create the card
                    current_stage_card = StageScan(
                        stage_number = Props.STAGES_NUMBER,
                        card_list = self.stages_list_container
                    )
                    
                    # Modify current values and apply
                    current_stage_card.preset_dropdown.value = stage_config["preset_name"]
                    # print(f"Assigned {stage_config['preset_name']} to Scan card")
                    

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
                    current_stage_card.filter_dropdown.value = stage_config["filter_name"]
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

                    current_stage_card.save_dropdown.value = stage_config["save_path"]
                    # print(f"Assigned {stage_config['save_path']} to Scan card")

                    Props.CURRENT_ROUTINE["stages"].append(
                        {
                            "type": stage_type,
                            "config": stage_config
                        }
                    )  

                case _:
                    self.show_alert("Unrecognized stage type: " + stage_type)
                    return
                
            self.stages_list_container.content.controls.append(
                current_stage_card
            )
        
        print(Props.CURRENT_ROUTINE)
        self.stages_list_container.content.update()
        self.show_alert("Applied routine: " + routine_name)

    def __add_new_routine_button_clicked(self, e):

        Props.CURRENT_ROUTINE["name"] = self.routine_name_input.value

        routine_name = Props.CURRENT_ROUTINE["name"]
        stages = Props.CURRENT_ROUTINE["stages"]

        Routines.add_routine(routine_name=routine_name, stages=stages)

        self.routine_loader_dropdown.options = self.__get_available_routines()
        self.routine_loader_dropdown.update()
        self.show_alert("Added routine: " + routine_name)

    def __update_routine_button_clicked(self, e):

        routine_name = Props.CURRENT_ROUTINE["name"]
        stages = Props.CURRENT_ROUTINE["stages"]

        Routines.update_routine(routine_name=routine_name, stages=stages)
        self.show_alert("Updated routine: " + routine_name)
    
    def __delete_routine_button_clicked(self, e):
        
        routine_name = self.routine_name_input.value

        try:
            Routines.remove_routine(routine_name=routine_name)
            self.routine_loader_dropdown.options = self.__get_available_routines()
            self.routine_loader_dropdown.update()
        except:
            self.show_alert("Issue deleting routine: " + routine_name)

        self.show_alert("Deleted routine: " + routine_name)

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
            self.show_alert("Please add at least one stage.")
            return

        # Check the amout of stages
        for stage in Props.CURRENT_ROUTINE["stages"]:
            match stage["type"]:
                case "Scan":
                    Props.IS_SCANNING = True

                    self.__start_scan(stage=stage)

                    Props.IS_SCANNING = False
                
                case "Filter":
                    Props.IS_FILTERING = True

                    self.__start_filter(stage=stage)
                    Props.APPEND_FILTER = True

                    Props.IS_FILTERING = False

                case "Save":
                    Props.IS_SAVING = True

                    self.__start_save(stage=stage)

                    Props.IS_SAVING = True

                case _:
                    pass
        
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

        self.clean_directory()

        # START CAPTURE
        match Props.CURRENT_FREQUENCY:
            case "5 [DEG/SHOT]":
                for i in range(0,72):
                    self.motor.move_degs(5)
                    time.sleep(3)
                    self.trigger_capture(iteration_number = i)

            case "45 [DEG/SHOT]":
                for i in range(0,8):
                    self.motor.move_degs(45)
                    time.sleep(3)
                    self.trigger_capture(iteration_number = i)

            case "90 [DEG/SHOT]":
                for i in range(0,4):
                    self.motor.move_degs(90)
                    time.sleep(3)
                    self.trigger_capture(iteration_number = i)

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

        for image in images_to_filter:

            file_name = os.path.basename(image)
            file_path = Props.FILTERED_IMAGES_DIRECTORY + file_name

            match filter_to_apply:
                case "Remove background":
                    Filter.remove_background(
                        image_path=image,
                        output_path=file_path
                    )

                case "Resize image":
                    Filter.resize_image(
                        image_path=image,
                        output_path=file_path
                    )
                
                case "Fisheye correction":
                    Filter.resize_image(
                        image_path=image,
                        output_path=file_path
                    )

                case "CA Correction":
                    Filter.ca_correction(
                        image_path=image,
                        output_path=file_path
                    )
                
                case _:
                    pass

    def __start_save(self, stage):
        pass
    
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

    def trigger_capture(self, iteration_number: int) -> None:
        if Props.CURRENT_USE_CAMERA1:
            gphoto2.capture_image(
                camera_port = Props.CAMERAS_DICT[Props.CAMERAS_LIST[0]],
                download_path = Props.CAMERA1_DOWNLOAD_PATH,
                file_name = "A000" + str(iteration_number) + Props.CURRENT_FILE_EXTENSION
            )

        if Props.CURRENT_USE_CAMERA2:
            gphoto2.capture_image(
                camera_port = Props.CAMERAS_DICT[Props.CAMERAS_LIST[1]],
                download_path = Props.CAMERA2_DOWNLOAD_PATH,
                file_name = "B000" + str(iteration_number) + Props.CURRENT_FILE_EXTENSION
            )

        if Props.CURRENT_USE_CAMERA3:
            gphoto2.capture_image(
                camera_port = Props.CAMERAS_DICT[Props.CAMERAS_LIST[2]],
                download_path = Props.CAMERA3_DOWNLOAD_PATH,
                file_name = "C000" + str(iteration_number) + Props.CURRENT_FILE_EXTENSION
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
    # endregion
