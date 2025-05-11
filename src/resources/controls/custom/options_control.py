import flet as ft

from src.resources.properties import Properties as Props
from src.camera_controller import GPhoto2 as gp


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
                ft.DropdownOption(text="90 [DEG/SHOT]")
            ],
            value=None,
            label="Frequency",
            width = Props.CHECKBOX_WIDTH,
            border_radius = Props.BORDER_RADIUS,
            on_change=self.__freq_dropdown_changed
        )

        self.format_dropdown = ft.Dropdown(
            options=self.__get_format_options(),
            value=None,
            label = "Format",
            width = Props.CHECKBOX_WIDTH,
            border_radius = Props.BORDER_RADIUS,
            on_change=self.__format_dropdown_changed
        )

        self.resolution_dropdown = ft.Dropdown(
            options=[
                ft.DropdownOption(text="24MP (4000x6000)"),
                ft.DropdownOption(text="FHD (1920x1080)")
            ],
            value=None,
            label="Resolution",
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

    def __freq_dropdown_changed(self,e):
        """
        Updates the current frequency setting when the user selects a new option.

        Args:
            e (ControlEvent): The event triggered when a frequency selection is made.

        Side effects:
            - Updates the `Props.CURRENT_FREQUENCY` with the selected value.
        """
        Props.CURRENT_FREQUENCY = self.freq_dropdown.value

    def __format_dropdown_changed(self,e):
        """
        Updates the current image format setting when the user selects a new option.

        Args:
            e (ControlEvent): The event triggered when a format selection is made.

        Side effects:
            - Updates the `Props.CURRENT_FORMAT` with the selected value.
        """
        Props.CURRENT_FORMAT = self.format_dropdown.value

    def __resolution_dropdown_changed(self,e):
        """
        Updates the current resolution setting when the user selects a new option.

        Args:
            e (ControlEvent): The event triggered when a resolution selection is made.

        Side effects:
            - Updates the `Props.CURRENT_RESOLUTION` with the selected value.
        """
        Props.CURRENT_RESOLUTION = self.resolution_dropdown.value

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

        __formats: dict[str, str] = gp.get_config(camera_port=Props.DEFAULT_CAMERA_PORT, camera_config=Props.FORMAT_CAMERA_CONFIG)

        for format in __formats.keys():
            formats_list.append(
                ft.DropdownOption(text=format)
            )

        return formats_list