import flet as ft

from ..custom.header_control import HeaderControl
from ...properties import *


class ScabTab(ft.Tab):
    """
    Scan tab in Workspace frame
    """
    def __init__(self, title: str):
        super().__init__()
        self.text = title
        self.icon = ft.Icon(ft.Icons.CAMERA, size=TAB_ICON_SIZE, visible=TAB_ICON_ENABLED)
        self.image_source = "src/resources/assets/images/example_01.png"
        self.content=ft.Column(
            [
                HeaderControl("View"),
                self.image_viewer(),
                HeaderControl("Options")
            ]
        )


    def image_viewer(self):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Image(src=self.image_source, height=400),
                    ft.Row(
                        [
                            ft.Dropdown(
                                options=[ft.DropdownOption(text="Camera 1"), ft.DropdownOption(text="Camera 2"), ft.DropdownOption(text="Camera 3")],
                                border_radius=0,
                                label="Camera: "
                            ),
                            ft.ElevatedButton(
                                text="Test",
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(0))
                            )
                        ]
                    )
                ]
            ),
            alignment=ft.alignment.top_center,
            expand = 1
        )