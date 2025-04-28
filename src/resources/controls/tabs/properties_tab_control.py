from email.header import Header

import flet as ft

from src.resources.properties import Properties as Props


class PropertiesTab(ft.Tab):
    """
    Properties tab in Workspace frame
    """

    def __init__(self, title: str):
        super().__init__()
        self.text = title
        self.icon = ft.Icon(ft.Icons.SETTINGS_INPUT_COMPONENT, size=Props.TAB_ICON_SIZE,visible=Props.TAB_ICON_ENABLED)

        # Explorer settings
        self.explorer_settings: ft.ExpansionTile = ft.ExpansionTile(
            title=ft.Text(value=Props.EXPLORER_SETTINGS_TITLE),
            subtitle=ft.Text(value=Props.EXPLORER_SETTINGS_SUBTITLE),
            affinity=ft.TileAffinity.LEADING,
            initially_expanded=False,
            controls_padding=Props.TAB_PADDING,
            controls=[
                ft.ListTile(title=ft.Text("Explorer width: ")),
                ft.Slider(min=0, max=100, divisions=10, label="{value}%")
            ]
        )

        # Scan settings
        self.scan_settings: ft.ExpansionTile = ft.ExpansionTile(
            title=ft.Text(value=Props.SCAN_SETTINGS_TITLE),
            subtitle=ft.Text(value=Props.SCAN_SETTINGS_SUBTITLE),
            affinity=ft.TileAffinity.LEADING,
            initially_expanded=False,
            controls_padding=Props.TAB_PADDING,
            controls=[
                ft.ListTile(title=ft.Text("Buttons border radius: ")),
                ft.Slider(min=0, max=100, divisions=10, label="{value}%"),
                ft.ListTile(title=ft.Text("View test image size: ")),
                ft.Slider(min=0, max=100, divisions=10, label="{value}%"),
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