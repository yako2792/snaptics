import flet as ft
from src.resources.properties import *


class PropertiesTab(ft.Tab):
    """
    Properties tab in Workspace frame
    """
    def __init__(self, title: str):
        super().__init__()
        self.text = title
        self.icon = ft.Icon(ft.Icons.SETTINGS_INPUT_COMPONENT, size=TAB_ICON_SIZE,visible=TAB_ICON_ENABLED)
        self.content = ft.Text(value="Example 4")