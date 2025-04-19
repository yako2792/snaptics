import flet as ft
from src.resources.controls.custom.header_control import HeaderControl
from src.resources.properties import *

class ExplorerControl(ft.Container):
    """
    Sidebar panel for file or element exploration.

    This container acts as the explorer panel where users can
    navigate and manage files or elements. It includes a header
    and is positioned on the left side of the layout.
    """

    def __init__(self, page: ft.Page):
        """
        Initializes the explorer control.

        Args:
            page (ft.Page): The main page instance of the application.
        """
        super().__init__()
        self.title = "Explorer"
        self.bgcolor = CONTAINER_BGCOLOR
        self.alignment = ft.alignment.top_left
        self.width = page.width*EXPLORER_SIZE
        self.padding = FRAME_PADDING

        self.content = ft.Column(
            [
                HeaderControl(self.title)
            ]
        )

