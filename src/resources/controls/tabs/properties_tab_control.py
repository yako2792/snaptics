import flet as ft
from src.resources.properties import Properties as Props
from src.camera_controller import GPhoto2 as gp


def convert_percentage_to_width_height(width: int, height: int):
    """
    Converts a resolution (width, height) into a corresponding percentage
    based on a predefined mapping.

    Args:
        width (int): Width in pixels.
        height (int): Height in pixels.

    Returns:
        int: Corresponding percentage. Returns 0 if the resolution is not in the map.
    """
    resolutions_to_percentage = {
        (320, 180): 40,
        (426, 240): 50,
        (480, 270): 60,
        (540, 300): 70,
        (640, 360): 80,
        (800, 450): 90,
        (960, 540): 100
    }

    return resolutions_to_percentage.get((width, height), 0)

def convert_percentage_to_resolution(percentage: int):
    """
    Converts a percentage value into a resolution (width, height) using
    a predefined mapping.

    Args:
        percentage (int): Size percentage (between 40 and 100).

    Returns:
        tuple[int, int]: Resolution as (width, height). Returns (0, 0) if percentage is not in the map.
    """
    percentage_to_resolutions = {
        40: (320, 180),
        50: (426, 240),
        60: (480, 270),
        70: (540, 300),
        80: (640, 360),
        90: (800, 450),
        100: (960, 540)
    }

    return percentage_to_resolutions.get(percentage, (0, 0))

class PropertiesTab(ft.Tab):
    """
    Properties tab for the workspace UI.

    This tab contains configurable settings for multiple sections of the application:
    Explorer, Scan, and Camera.

    Attributes:
        text (str): Tab title text.
        icon (ft.Icon): Icon displayed on the tab.
        explorer_tab (ft.Tab): Reference to the explorer tab.
        preview_tab (ft.Tab): Reference to the preview tab.
        scan_tab (ft.Tab): Reference to the scan tab.
        content (ft.Column): Main container with expandable tiles for each configuration section.
    """

    def __init__(self, title: str, page: ft.Page, tab_references: dict[str, ft.Tab]):
        super().__init__()
        self.text = title
        self.icon = ft.Icon(ft.Icons.SETTINGS_INPUT_COMPONENT, size=Props.TAB_ICON_SIZE,visible=Props.TAB_ICON_ENABLED)
        self.page = page

        self.explorer_tab = tab_references[Props.EXPLORER_KEY]
        self.preview_tab = tab_references[Props.PREVIEW_KEY]
        self.scan_tab = tab_references[Props.SCAN_KEY]

        self.iso_dropdown = ft.Dropdown(
            options=self.__get_available_isos(),
            label="ISO",
            width=Props.DROPDOWN_WIDTH, 
            on_change=self.__iso_dropdown_changed
        )

        self.shutterspeed_dropdown = ft.Dropdown(
            options=self.__get_available_shutterspeeds(),
            label="SHUTTERSPEED",
            width=Props.DROPDOWN_WIDTH, 
            on_change=self.__shutterspeed_dropdown_changed
        )

        # Explorer settings
        self.explorer_settings: ft.ExpansionTile = ft.ExpansionTile(
            title=ft.Text(value=Props.EXPLORER_SETTINGS_TITLE),
            subtitle=ft.Text(value=Props.EXPLORER_SETTINGS_SUBTITLE),
            affinity=ft.TileAffinity.LEADING,
            initially_expanded=Props.INITIALLY_EXPANDED_PROPERTIES,
            controls_padding=Props.TAB_PADDING,
            controls=[
                ft.ListTile(
                    title=ft.Text("Explorer width: "),
                    subtitle=ft.Slider(min=20, max=60, divisions=4, label="{value}%", on_change=self.__explorer_width_slider_changed, value=Props.EXPLORER_SIZE*100)
                )
            ]
        )

        # Scan settings
        self.scan_settings: ft.ExpansionTile = ft.ExpansionTile(
            title=ft.Text(value=Props.SCAN_SETTINGS_TITLE),
            subtitle=ft.Text(value=Props.SCAN_SETTINGS_SUBTITLE),
            affinity=ft.TileAffinity.LEADING,
            initially_expanded=Props.INITIALLY_EXPANDED_PROPERTIES,
            controls_padding=Props.TAB_PADDING,
            controls=[
                ft.ListTile(
                    title=ft.Text("Buttons border radius: "),
                    subtitle=ft.Slider(min=0, max=100, divisions=10, label="{value}%", on_change=self.__scan_border_radius_slider_changed, value=Props.BORDER_RADIUS)
                ),
                ft.ListTile(
                    title=ft.Text("View test image size: "),
                    subtitle=ft.Slider(min=40, max=100, divisions=6, label="{value}%", on_change=self.__image_viewer_size_slider_changed, value=convert_percentage_to_width_height(Props.IMAGE_VIEW_WIDTH, Props.IMAGE_VIEW_HEIGHT))
                ),
                ft.ListTile(
                    title=ft.Text("Save file path: "),
                    subtitle=ft.TextField(label="Path", border=ft.InputBorder.UNDERLINE, hint_text=Props.DEFAULT_HINT)
                ),

            ]
        )

        # Camera settings
        self.camera_settings: ft.ExpansionTile = ft.ExpansionTile(
            title=ft.Text(value=Props.CAMERA_SETTINGS_TITLE),
            subtitle=ft.Text(value=Props.CAMERA_SETTINGS_SUBTITLE),
            affinity=ft.TileAffinity.LEADING,
            initially_expanded=Props.INITIALLY_EXPANDED_PROPERTIES,
            controls_padding=Props.TAB_PADDING,
            controls=[
                ft.ListTile(
                    title=ft.Text("Camera ISO: "),
                    subtitle=self.iso_dropdown 
                ),
                ft.ListTile(
                    title=ft.Text("Camera SHUTTERSPEED: "),
                    subtitle=self.shutterspeed_dropdown
                ),

            ]
        )

        self.content = ft.Column(
            [
                self.explorer_settings,
                self.scan_settings,
                self.camera_settings
            ],
            scroll=ft.ScrollMode.AUTO
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

    def __get_available_isos(self):

        isos_list: list[ft.DropdownOption] = []

        for iso in Props.ISOS_DICT.keys():
            isos_list.append(
                ft.DropdownOption(text=iso)
            )

        return isos_list

    def __get_available_shutterspeeds(self):

        shutterspeeds_list: list[ft.DropdownOption] = []

        for shutterspeed in Props.SHUTTERSPEEDS_DICT.keys():
            shutterspeeds_list.append(
                ft.DropdownOption(text=shutterspeed)
            )

        return shutterspeeds_list

    def __explorer_width_slider_changed(self, e):
        """
        Callback for the Explorer width slider.

        Updates the width of the Explorer tab based on the selected slider value.
        """
        new_width = e.control.value / 100
        self.explorer_tab.modify_width(new_width)

    def __scan_border_radius_slider_changed(self, e):
        """
        Callback for the button border radius slider.

        Updates the corner radius of buttons in the Scan tab.
        """
        new_radius = e.control.value
        self.scan_tab.modify_button_radius(new_radius)

    def __image_viewer_size_slider_changed(self, e):
        """
        Callback for the image viewer size slider.

        Converts the percentage to a resolution and updates the test image viewer size.
        """
        percentage = int(e.control.value)
        new_width, new_height = convert_percentage_to_resolution(percentage)
        self.scan_tab.modify_view_image_size(new_width, new_height)

    def __iso_dropdown_changed(self, e):
        """
        Callback for the iso dropdown menu.
        """

        Props.CURRENT_ISO = self.iso_dropdown.value
        for camera in Props.CAMERAS_LIST:
            gp.set_config(
                camera_port=Props.CAMERAS_DICT[camera],
                camera_config=Props.ISO_CAMERA_CONFIG,
                config_value=Props.ISOS_DICT[Props.CURRENT_ISO]
                )
            self.show_alert("Iso set properly.")

    def __shutterspeed_dropdown_changed(self, e):
        """
        Callback for the shutterspeed dropdown menu.
        """

        Props.CURRENT_SHUTTERSPEED = self.shutterspeed_dropdown.value
        for camera in Props.CAMERAS_LIST:
            gp.set_config(
                camera_port=Props.CAMERAS_DICT[camera],
                camera_config=Props.SHUTTERSPEED_CAMERA_CONFIG,
                config_value=Props.SHUTTERSPEEDS_DICT[Props.CURRENT_SHUTTERSPEED]
                )
            print("set " + Props.CAMERAS_DICT[camera] + Props.SHUTTERSPEED_CAMERA_CONFIG + Props.SHUTTERSPEEDS_DICT[Props.CURRENT_SHUTTERSPEED])
            self.show_alert("Shutterspeed set properly.")