import flet as ft

from src.resources.properties import Properties as Props


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
            label="Frequency",
            width = Props.CHECKBOX_WIDTH,
            border_radius = Props.BORDER_RADIUS
        )

        self.format_dropdown = ft.Dropdown(
            options=[
                ft.DropdownOption(text="RAW"),
                ft.DropdownOption(text="JPG")
            ],
            label = "Format",
            width = Props.CHECKBOX_WIDTH,
            border_radius = Props.BORDER_RADIUS
        )

        self.resolution_dropdown = ft.Dropdown(
            options=[
                ft.DropdownOption(text="24MP (4000x6000)"),
                ft.DropdownOption(text="FHD (1920x1080)")
            ],
            label="Resolution",
            width = Props.CHECKBOX_WIDTH,
            border_radius = Props.BORDER_RADIUS
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