from tkinter.ttk import Label

import flet as ft
from src.resources.properties import Properties as Props


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

        # CONTROLS
        self.camera_dropdown = ft.Dropdown(
            options=[
                ft.DropdownOption(text="Camera 1"),
                ft.DropdownOption(text="Camera 2"),
                ft.DropdownOption(text="Camera 3")
            ],
            label="Camera",
            width=Props.DROPDOWN_WIDTH,
            border_radius=Props.BORDER_RADIUS
        )

        self.test_button = ft.ElevatedButton(
            text="Test",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
            height=Props.BUTTON_HEIGHT
        )

        self.view_image = ft.Container(
            alignment=ft.alignment.center,
            width= Props.IMAGE_VIEW_WIDTH,
            height= Props.IMAGE_VIEW_HEIGHT,
            bgcolor=Props.PAGE_BGCOLOR,
            content=ft.Text(value=Props.NO_IMAGE)
        )

        self.content = ft.Container(
            alignment=ft.alignment.center,
            expand=1,
            content=ft.Column(
                [
                    self.view_image,
                    ft.Row(
                        [
                            self.camera_dropdown,
                            self.test_button
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

    def update_all_radius(self):
        """
        Update all border radius in custom controls
        :return:
        """
        self.test_button.style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS))
        self.camera_dropdown.border_radius=Props.BORDER_RADIUS

    def update_view_image_size(self):
        """
        Update view image size
        :return:
        """
        self.view_image.width = Props.IMAGE_VIEW_WIDTH
        self.view_image.height = Props.IMAGE_VIEW_HEIGHT