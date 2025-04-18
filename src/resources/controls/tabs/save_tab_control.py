import flet as ft
from src.resources.properties import *


class SaveTab(ft.Tab):
    """
    Save tab in Workspace frame
    """
    def __init__(self, title: str):
        super().__init__()
        self.text = title
        self.icon = ft.Icon(ft.Icons.SAVE, size=TAB_ICON_SIZE,visible=TAB_ICON_ENABLED)
        self.content=ft.Text(value="Example 3")