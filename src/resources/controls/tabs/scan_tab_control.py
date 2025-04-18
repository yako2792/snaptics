from pathlib import Path

import flet as ft

from src.resources.controls.custom.header_control import HeaderControl
from src.resources.controls.custom.image_viewer_control import ImageViewer
from src.resources.properties import *


class ScabTab(ft.Tab):
    """
    Scan tab in Workspace frame

    This tab provides an interface for interacting with connected cameras,
    including viewing live or static previews and performing scan actions.
    """
    def __init__(self, title: str):
        super().__init__()
        self.text = title
        self.icon = ft.Icon(ft.Icons.CAMERA, size=TAB_ICON_SIZE, visible=TAB_ICON_ENABLED)
        self.image_source = "some/path/image.jpg"
        self.content=ft.Container(
            padding=TAB_PADDING,
            content=ft.Column(
                [
                    HeaderControl("View"),
                    ImageViewer(self.image_source),
                    HeaderControl("Options")
                ],
                scroll=ft.ScrollMode.AUTO
            )
        )