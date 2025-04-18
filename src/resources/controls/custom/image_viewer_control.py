from tkinter.ttk import Label

import flet as ft

from src.resources.properties import *


class ImageViewer(ft.Container):
    """
    A component for displaying an image preview with camera controls.

    This container includes an image display and controls for selecting
    a camera source and performing actions like triggering a quick scan.
    """

    def __init__(self, source: str):
        """
        Initializes the image viewer.

        Args:
            source (str): The image source path or URL to be displayed.
        """
        super().__init__()
        self.image_path = source

        self.content = ft.Container(
            alignment=ft.alignment.center,
            expand=1,
            content=ft.Column(
                [
                    ft.Container(
                        alignment=ft.alignment.center,
                        width=640,
                        height=360,
                        bgcolor=PAGE_BGCOLOR,
                        content=ft.Text(value=NO_IMAGE)
                    ),
                    ft.Row(
                        [
                            ft.Dropdown(
                                options=[
                                    ft.DropdownOption(text="Camera 1"),
                                    ft.DropdownOption(text="Camera 2"),
                                    ft.DropdownOption(text="Camera 3")
                                ],
                                label="Camera",
                                width=350
                            ),
                            ft.ElevatedButton(
                                text="Test",
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0)),
                                height=49
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
