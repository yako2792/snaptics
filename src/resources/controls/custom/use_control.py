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

        self.camera1_checkbox = ft.Container(
            content=ft.Checkbox(
                label="Camera 1",
                value=False
            ),
            height=Props.CHECKBOX_HEIGHT,
            width=Props.CHECKBOX_WIDTH
        )
        self.camera2_checkbox = ft.Container(
            content=ft.Checkbox(
                label="Camera 2",
                value=False
            ),
            height=Props.CHECKBOX_HEIGHT,
            width=Props.CHECKBOX_WIDTH
        )
        self.camera3_checkbox = ft.Container(
            content=ft.Checkbox(
                label="Camera 3",
                value=False
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
                    ),
                    ft.Column(
                        [
                            ft.ElevatedButton(
                                text="Start",
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
                                height=Props.BUTTON_HEIGHT,
                                width=Props.BUTTON_WIDTH
                            ),
                            ft.ElevatedButton(
                                text="Reset",
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
                                height=Props.BUTTON_HEIGHT,
                                width=Props.BUTTON_WIDTH
                            ),
                            ft.ElevatedButton(
                                text="Stop",
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
                                height=Props.BUTTON_HEIGHT,
                                width=Props.BUTTON_WIDTH
                            )
                        ]
                    )
                ]
            ),
            padding=Props.PAGE_PADDING
        )