import flet as ft
from ...properties import *


class PreviewTab(ft.Tab):
    """
    Preview tab in Workspace frame
    """
    def __init__(self, title):
        super().__init__()
        self.text = title
        self.icon = ft.Icon(ft.Icons.PREVIEW, size=TAB_ICON_SIZE, visible=TAB_ICON_ENABLED)
        self.content=ft.Text(value="Example 1")