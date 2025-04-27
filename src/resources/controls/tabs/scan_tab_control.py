from pathlib import Path

import flet as ft

from src.resources.controls.custom.header_control import HeaderControl
from src.resources.controls.custom.image_viewer_control import ImageViewer
from src.resources.controls.custom.options_control import OptionsControl
from src.resources.controls.custom.use_control import UseControl
from src.resources.properties import Properties as Props


class ScabTab(ft.Tab):
    """
    Scan tab in Workspace frame

    This tab provides an interface for interacting with connected cameras,
    including viewing live or static previews and performing scan actions.
    """
    def __init__(self, title: str):
        super().__init__()
        self.text = title
        self.icon = ft.Icon(ft.Icons.CAMERA, size=Props.TAB_ICON_SIZE, visible=Props.TAB_ICON_ENABLED)
        self.image_source = "some/path/image.jpg"
        self.content=ft.Container(
            padding=Props.TAB_PADDING,
            content=ft.Column(
                [
                    # TOP
                    HeaderControl("View"),
                    ImageViewer(self.image_source),

                    # BOTTOM
                    ft.Row(
                        [
                            ft.Container(
                                ft.Column(
                                    [
                                        HeaderControl("Options"),
                                        OptionsControl()
                                    ],
                                    alignment=ft.alignment.top_left
                                ),
                                alignment=ft.alignment.top_left,
                                expand=1
                            ),
                            ft.Container(
                                ft.Column(
                                    [
                                        HeaderControl("Use"),
                                        UseControl()
                                    ],
                                    alignment=ft.alignment.top_left
                                ),
                                alignment=ft.alignment.top_left,
                                expand=1
                            )
                        ]
                    )
                ],
                scroll=ft.ScrollMode.AUTO
            )
        )