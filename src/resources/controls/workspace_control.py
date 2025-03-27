import flet as ft
from .header_control import HeaderControl
from ..properties import *

class WorkspaceControl(ft.Container):
    """
    The main workspace area of the application.

    This container serves as the primary working space where
    users interact with content. It includes a header and can
    be expanded to fit available space.
    """

    def __init__(self, page: ft.Page):
        """
        Initializes the workspace control.

        Args:
            page (ft.Page): The main page instance of the application.
        """
        super().__init__()
        self.title = "Workspace"
        self.bgcolor = CONTAINER_BGCOLOR
        self.alignment = ft.alignment.top_left
        self.expand = 1
        self.padding = 3

        self.content = ft.Column(
            [
                HeaderControl(self.title)
            ]
        )
