import flet as ft

from src.resources.properties import Properties as Props


def is_scanning():
    return Props.IS_SCANNING

def no_camera_selected():
    return not any([Props.CURRENT_USE_CAMERA1, Props.CURRENT_USE_CAMERA2, Props.CURRENT_USE_CAMERA3])

def capture_options_missing():
    return not all([Props.CURRENT_FREQUENCY, Props.CURRENT_FORMAT, Props.CURRENT_RESOLUTION])

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
                label="Camera 1",
                value=False,
                on_change=self.__camera1_checkbox_changed
            ),
            height=Props.CHECKBOX_HEIGHT,
            width=Props.CHECKBOX_WIDTH
        )
        self.camera2_checkbox = ft.Container(
            content=ft.Checkbox(
                label="Camera 2",
                value=False,
                on_change=self.__camera2_checkbox_changed
            ),
            height=Props.CHECKBOX_HEIGHT,
            width=Props.CHECKBOX_WIDTH
        )
        self.camera3_checkbox = ft.Container(
            content=ft.Checkbox(
                label="Camera 3",
                value=False,
                on_change=self.__camera3_checkbox_changed
            ),
            height=Props.CHECKBOX_HEIGHT,
            width=Props.CHECKBOX_WIDTH
        )

        # BUTTONS
        self.start_button = ft.ElevatedButton(
            text="Start",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
            height=Props.BUTTON_HEIGHT,
            width=Props.BUTTON_WIDTH,
            on_click=self.__start_button_clicked
        )
        self.reset_button = ft.ElevatedButton(
            text="Reset",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
            height=Props.BUTTON_HEIGHT,
            width=Props.BUTTON_WIDTH
        )
        self.stop_button = ft.ElevatedButton(
            text="Stop",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
            height=Props.BUTTON_HEIGHT,
            width=Props.BUTTON_WIDTH
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
                            self.start_button,
                            self.reset_button,
                            self.stop_button
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

    def __start_button_clicked(self, e):
        # VALIDATIONS
        # Check if there is a scan runnign
        if is_scanning():
            self.show_alert("Wait, a scan is being performed.")
            return
        # Check at least one camera is selected
        if no_camera_selected():
            self.show_alert("At least one camera should be selected.")
            return
        # Check all capture options are selected
        if capture_options_missing():
            self.show_alert("Some capture options are missing.")
            return
        
        # START CAPTURE
        self.show_alert("Started capture.")
        Props.IS_SCANNING = True

        # Logic here...


    def show_alert(self, message: str):
        """
        Displays a temporary snackbar alert with the given message.

        Args:
            message (str): The message to display in the snackbar.
        """
        snackbar = ft.SnackBar(
            content=ft.Text(value=message),
            duration=2000
        )
        snackbar.open = True
        self.page.open(snackbar)
        self.page.update()

    def update_all_radius(self):
        """
        Update border radius of all objects in custom control
        :return:
        """
        self.start_button.style = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS))
        self.reset_button.style = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS))
        self.stop_button.style = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS))
