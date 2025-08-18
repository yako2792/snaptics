import flet as ft
import time
from src.resources.properties import Properties as Props
from src.camera_controller import GPhoto2 as gp
from src.resources.controls.custom.loading_dialog import LoadingDialog


class OptionsControl(ft.Container):
    """
    A container control for displaying configurable scan options.

    This component contains dropdowns for selecting scan frequency,
    image format, and resolution. It is designed to be placed in the
    interface where users configure scan parameters before initiating
    a capture or scan operation.

    Attributes:
        freq_dropdown (ft.Dropdown): Dropdown for selecting frequency in degrees per shot.
        format_dropdown (ft.Dropdown): Dropdown for selecting image format (e.g., RAW, JPG).
        resolution_dropdown (ft.Dropdown): Dropdown for selecting output resolution.
    """

    def __init__(self):
        """
        Initializes the options control with default dropdown selections.

        The control includes:
            - Frequency selection dropdown
            - Format selection dropdown
            - Resolution selection dropdown

        All controls are arranged vertically with standard padding.
        """
        super().__init__()

        self.freq_dropdown = ft.Dropdown(
            options=[
                ft.DropdownOption(text="5 [DEG/SHOT]"),
                ft.DropdownOption(text="45 [DEG/SHOT]"),
                ft.DropdownOption(text="90 [DEG/SHOT]"),
                ft.DropdownOption(text="360 [DEG/SHOT]")
            ],
            value=None,
            label="Frecuencia",
            width = Props.CHECKBOX_WIDTH,
            border_radius = Props.BORDER_RADIUS,
            on_change=self.__freq_dropdown_changed
        )

        self.format_dropdown = ft.Dropdown(
            options=self.__get_format_options(),
            value=None,
            label = "Formato",
            width = Props.CHECKBOX_WIDTH,
            border_radius = Props.BORDER_RADIUS,
            on_change=self.__format_dropdown_changed
        )

        self.resolution_dropdown = ft.Dropdown(
            options=self.__get_resolution_options(),
            value=None,
            label="Resolución",
            width = Props.CHECKBOX_WIDTH,
            border_radius = Props.BORDER_RADIUS,
            on_change=self.__resolution_dropdown_changed
        )

        self.content = ft.Container(
            ft.Column(
                [
                    self.freq_dropdown,
                    self.format_dropdown,
                    self.resolution_dropdown
                ]
            ),
            padding = Props.PAGE_PADDING
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

    def __freq_dropdown_changed(self,e):
        """
        Updates the current frequency setting when the user selects a new option.

        Args:
            e (ControlEvent): The event triggered when a frequency selection is made.

        Side effects:
            - Updates the `Props.CURRENT_FREQUENCY` with the selected value.
        """
        Props.CURRENT_FREQUENCY = self.freq_dropdown.value

        loading_dialog = LoadingDialog(page=Props.PAGE, title="Espera")
        loading_dialog.show()
        loading_dialog.update_legend(f"Aplicando frecuencia: {Props.CURRENT_FREQUENCY}")
        time.sleep(1)
        loading_dialog.update_legend(f"Frecuencia aplicada correctamente!")
        loading_dialog.update_legend(f"Listo!")
        loading_dialog.hide()


    def __format_dropdown_changed(self,e):
        """
        Updates the current image format setting when the user selects a new option.

        Args:
            e (ControlEvent): The event triggered when a format selection is made.

        Side effects:
            - Updates the `Props.CURRENT_FORMAT` with the selected value.
        """
        Props.CURRENT_FORMAT = self.format_dropdown.value

        loading_dialog = LoadingDialog(page=Props.PAGE, title="Espera")
        loading_dialog.show()
        loading_dialog.update_legend(f"Aplicando formato: {Props.CURRENT_FORMAT}")
        print(f"Aplicando formato: {Props.CURRENT_FORMAT}")

        for camera in Props.CAMERAS_LIST:
            if camera == None:
                continue
            
            loading_dialog.update_legend(f"Aplicando formato a la cámara: {camera}")
            print(f"Aplicando formato a la cámara: {camera}")

            gp.set_config(
                camera_port=Props.CAMERAS_DICT[camera],
                camera_config=Props.FORMAT_CAMERA_CONFIG,
                config_value=Props.FORMATS_DICT[Props.CURRENT_FORMAT]
                )
            
            loading_dialog.update_legend(f"Formato aplicado correctamente!")
            print(f"Formato aplicado correctamente!")
        
        loading_dialog.update_legend(f"Listo!")
        loading_dialog.hide()
            

    def __resolution_dropdown_changed(self,e):
        """
        Updates the current resolution setting when the user selects a new option.

        Args:
            e (ControlEvent): The event triggered when a resolution selection is made.

        Side effects:
            - Updates the `Props.CURRENT_RESOLUTION` with the selected value.
        """
        Props.CURRENT_RESOLUTION = self.resolution_dropdown.value

        loading_dialog = LoadingDialog(page=Props.PAGE, title="Espera")
        loading_dialog.show()
        loading_dialog.update_legend(f"Aplicando resolución: {Props.CURRENT_RESOLUTION}")
        print(f"Aplicando resolución: {Props.CURRENT_RESOLUTION}")

        if "RAW" in Props.CURRENT_FORMAT:
            Props.CURRENT_FILE_EXTENSION = Props.RAW_EXTENSION
        else:
            Props.CURRENT_FILE_EXTENSION = Props.JPEG_EXTENSION

        for camera in Props.CAMERAS_LIST:
            if camera == None:
                continue 

            loading_dialog.update_legend(f"Aplicando resolución a la cámara: {camera}")
            print(f"Aplicando resolución a la cámara: {camera}")

            gp.set_config(
                camera_port=Props.CAMERAS_DICT[camera],
                camera_config=Props.RESOLUTION_CAMERA_CONFIG,
                config_value=Props.RESOLUTIONS_DICT[Props.CURRENT_RESOLUTION]
                )
            
            loading_dialog.update_legend(f"Resolución aplicada correctamente!")
            print("Resolucion aplicada correctamente.")
        
        loading_dialog.update_legend(f"Listo!")
        loading_dialog.hide()

    def update_all_radius(self):
        """
        Updates the border radius of all dropdowns in the control.

        Side effects:
            - Sets the border radius of `freq_dropdown`, `format_dropdown`, and `resolution_dropdown` to the value in `Props.BORDER_RADIUS`.
        """
        self.freq_dropdown.border_radius = Props.BORDER_RADIUS
        self.format_dropdown.border_radius = Props.BORDER_RADIUS
        self.resolution_dropdown.border_radius = Props.BORDER_RADIUS

    def __get_format_options(self):

        formats_list: list[ft.DropdownOption] = []

        for format in Props.FORMATS_DICT.keys():
            if format and "raw" not in format.lower():
                formats_list.append(
                    ft.DropdownOption(text=str(format))
                )

        return formats_list
    
    def __get_resolution_options(self):

        resolution_list: list[ft.DropdownOption] = []

        for resolution in Props.RESOLUTIONS_DICT.keys():
            resolution_list.append(
                ft.DropdownOption(text=str(resolution))
            )
        return resolution_list