import os
import json
import flet as ft

from src.resources.properties import Properties as Props

class PresetControl(ft.Container):

    def __init__(self, page: ft.Page, options: ft.Container, camera_use: ft.Container):

        super().__init__()
        self.page = page
        self.presets = self.__load_presets()

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
            label="Name",
            width=Props.DROPDOWN_WIDTH,
            border_radius=Props.BORDER_RADIUS
        )
        # BUTTONS - LEFT
        self.apply_button = ft.ElevatedButton(
            text="Apply",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
            height=Props.BUTTON_HEIGHT,
            width=Props.BUTTON_WIDTH,
            on_click=self.__apply_preset
        )
        # BUTTONS - RIGHT
        self.add_button = ft.ElevatedButton(
            text="Add",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
            height=Props.BUTTON_HEIGHT,
            width=Props.BUTTON_WIDTH,
            on_click=self.__add_preset
        )
        self.delete_button = ft.ElevatedButton(
            text="Delete",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
            height=Props.BUTTON_HEIGHT,
            width=Props.BUTTON_WIDTH,
            on_click=self.__delete_preset
        )
        self.update_button = ft.ElevatedButton(
            text="Update",
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
                            self.apply_button

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
        with open(Props.PRESETS_PATH, "w") as file:
            json.dump(presets, file, indent=2)

    def __reload_presets(self):
        self.presets = self.__load_presets()
        self.preset_dropdown.options = [ft.dropdown.Option(name) for name in self.presets]

    def __delete_preset(self, e):
        __preset_name = self.preset_name_input.value

        # GET CURRENT PRESETS
        presets = self.__load_presets()

        # CHECK IF PRESET EXISTS
        if __preset_name not in presets:
            self.show_alert(f"No preset with name: {__preset_name}")
            return

        # DELETE PRESET
        del presets[__preset_name]

        # WRITE IN JSON FILE
        self.__write_presets(presets)
        self.show_alert(f"Deleted preset: {__preset_name}")

        self.__reload_presets()
        self.preset_dropdown.update()

    def __add_preset(self, e):
        __preset_name = self.preset_name_input.value

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
            self.show_alert(f"Preset already exists: {__preset_name}")
            return

        presets[__preset_name] = preset_settings

        # ADD PRESET TO JSON
        self.__write_presets(presets)
        self.show_alert(f"Added preset: {__preset_name}")

        self.__reload_presets()
        self.preset_dropdown.update()

    def __update_preset(self, e):
        __preset_name = self.preset_name_input.value

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
            self.show_alert(f"Preset does not exists: {__preset_name}")
            return

        # UPDATING PRESET
        presets[__preset_name] = preset_settings

        # ADD PRESET TO JSON
        self.__write_presets(presets)
        self.show_alert(f"Updated preset: {__preset_name}")

        self.__reload_presets()
        self.preset_dropdown.update()

    def __apply_preset(self, e):
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

        self.show_alert(f"Applied preset: {__preset_name}")

        # UPDATE PAGE
        self.options.update()
        self.camera_use.update()

    def show_alert(self, message: str):
        snackbar = ft.SnackBar(
            content=ft.Text(value=message),
            duration=2000
        )
        snackbar.open = True
        self.page.open(snackbar)
        self.page.update()

    def update_all_radius(self):
        """
        Update border radius of all objects in custom control
        :return:
        """
        self.preset_dropdown.border_radius = Props.BORDER_RADIUS
        self.apply_button.style = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS))