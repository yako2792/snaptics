import os
import time
import flet as ft
from src.resources.properties import Properties as Props


class UseControl(ft.Container):
    """
    A container control that provides camera toggles and scan control buttons.

    This component includes three camera checkboxes and three action buttons
    (Start, Reset, Stop). It's intended to let the user select which cameras
    to use and to initiate control actions for scanning.

    Attributes:
        camera1_checkbox (ft.Container): Checkbox for enabling/disabling Camera 1.
        camera2_checkbox (ft.Container): Checkbox for enabling/disabling Camera 2.
        camera3_checkbox (ft.Container): Checkbox for enabling/disabling Camera 3.
    """
    def __init__(self):
        """
        Initializes the use control with camera checkboxes and action buttons.

        The layout includes:
            - A vertical column with checkboxes for Camera 1, 2, and 3.
            - A second column with Start, Reset, and Stop buttons.
        """
        super().__init__()

        # Other elements
        self.camera1_checkbox = ft.Container(
            content=ft.Checkbox(
                label=Props.CAMERAS_LIST[0] or "No disponible",
                value=False,
                on_change=self.__camera1_checkbox_changed
            ),
            height=Props.CHECKBOX_HEIGHT,
            width=Props.CHECKBOX_WIDTH
        )
        self.camera2_checkbox = ft.Container(
            content=ft.Checkbox(
                label=Props.CAMERAS_LIST[1] or "No disponible",
                value=False,
                on_change=self.__camera2_checkbox_changed
            ),
            height=Props.CHECKBOX_HEIGHT,
            width=Props.CHECKBOX_WIDTH
        )
        self.camera3_checkbox = ft.Container(
            content=ft.Checkbox(
                label=Props.CAMERAS_LIST[2] or "No disponible",
                value=False,
                on_change=self.__camera3_checkbox_changed
            ),
            height=Props.CHECKBOX_HEIGHT,
            width=Props.CHECKBOX_WIDTH
        )

        self.content = ft.Container(
            ft.Row(
                [
                    ft.Column(
                        [
                            self.camera1_checkbox,
                            self.camera2_checkbox,
                            self.camera3_checkbox
                        ]
                    )
                ]
            ),
            padding=Props.PAGE_PADDING
        )

    def __camera1_checkbox_changed(self,e):
        """
        Updates the global CURRENT_USE_CAMERA1 property
        based on the state of the Camera 1 checkbox.

        Args:
            e (ControlEvent): Checkbox change event.
        """
        Props.CURRENT_USE_CAMERA1 = self.camera1_checkbox.content.value

    def __camera2_checkbox_changed(self,e):
        """
        Updates the global CURRENT_USE_CAMERA2 property
        based on the state of the Camera 2 checkbox.

        Args:
            e (ControlEvent): Checkbox change event.
        """
        Props.CURRENT_USE_CAMERA2 = self.camera2_checkbox.content.value

    def __camera3_checkbox_changed(self,e):
        """
        Updates the global CURRENT_USE_CAMERA3 property
        based on the state of the Camera 3 checkbox.

        Args:
            e (ControlEvent): Checkbox change event.
        """
        Props.CURRENT_USE_CAMERA3 = self.camera3_checkbox.content.value
