import flet as ft
from src.resources.properties import Properties as Props


def convert_percentage_to_width_height(width: int, height: int):
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
    Properties tab in Workspace frame
    """

    def __init__(self, title: str, page: ft.Page, tab_references: dict[str, ft.Tab]):
        super().__init__()
        self.text = title
        self.icon = ft.Icon(ft.Icons.SETTINGS_INPUT_COMPONENT, size=Props.TAB_ICON_SIZE,visible=Props.TAB_ICON_ENABLED)
        self.page = page

        self.explorer_tab = tab_references[Props.EXPLORER_KEY]
        self.preview_tab = tab_references[Props.PREVIEW_KEY]
        self.scan_tab = tab_references[Props.SCAN_KEY]

        # Explorer settings
        self.explorer_settings: ft.ExpansionTile = ft.ExpansionTile(
            title=ft.Text(value=Props.EXPLORER_SETTINGS_TITLE),
            subtitle=ft.Text(value=Props.EXPLORER_SETTINGS_SUBTITLE),
            affinity=ft.TileAffinity.LEADING,
            initially_expanded=Props.INITIALLY_EXPANDED_PROPERTIES,
            controls_padding=Props.TAB_PADDING,
            controls=[
                ft.ListTile(title=ft.Text("Explorer width: ")),
                ft.Slider(min=20, max=60, divisions=4, label="{value}%", on_change=self.__explorer_width_slider_changed, value=Props.EXPLORER_SIZE*100)
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
                ft.ListTile(title=ft.Text("Buttons border radius: ")),
                ft.Slider(min=0, max=100, divisions=10, label="{value}%", on_change=self.__scan_border_radius_slider_changed, value=Props.BORDER_RADIUS),
                ft.ListTile(title=ft.Text("View test image size: ")),
                ft.Slider(min=40, max=100, divisions=6, label="{value}%", on_change=self.__image_viewer_size_slider_changed, value=convert_percentage_to_width_height(Props.IMAGE_VIEW_WIDTH, Props.IMAGE_VIEW_HEIGHT)),
                ft.ListTile(title=ft.Text("Save file path: ")),
                ft.TextField(label="Path", border=ft.InputBorder.UNDERLINE, hint_text=Props.DEFAULT_HINT)
            ]
        )

        self.content = ft.Column(
            [
                self.explorer_settings,
                self.scan_settings
            ],
            scroll=ft.ScrollMode.AUTO
        )

    def __explorer_width_slider_changed(self, e):
        new_width = e.control.value / 100
        self.explorer_tab.modify_width(new_width)

    def __scan_border_radius_slider_changed(self, e):
        new_radius = e.control.value
        self.scan_tab.modify_button_radius(new_radius)

    def __image_viewer_size_slider_changed(self, e):
        percentage = int(e.control.value)
        new_width, new_height = convert_percentage_to_resolution(percentage)
        self.scan_tab.modify_view_image_size(new_width, new_height)
