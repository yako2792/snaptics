import os
import flet as ft
from datetime import datetime
from src.camera_controller import GPhoto2 as gp
from src.resources.properties import Properties as Props

def test_camera_is_not_selected():
    return not all([Props.CURRENT_TEST_CAMERA])

def is_testing():
    return Props.IS_TESTING

class ImageViewer(ft.Container):
    """
    A component for displaying an image preview with camera controls.

    This container includes an image display and controls for selecting
    a camera source and performing actions like triggering a quick scan.
    """

    def __init__(self, page: ft.Page):
        """
        Initializes the image viewer.

        Args:
            source (str): The image source path or URL to be displayed.
        """
        super().__init__()
        self.page = page

        # CONTROLS
        self.camera_dropdown = ft.Dropdown(
            options=self.__get_cameras_options(),
            label="Camera",
            width=Props.DROPDOWN_WIDTH,
            border_radius=Props.BORDER_RADIUS,
            on_change=self.__camera_dropdown_changed
        )

        self.test_button = ft.ElevatedButton(
            text="Test",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
            height=Props.BUTTON_HEIGHT, 
            width=Props.BUTTON_WIDTH,
            on_click=self.__test_button_clicked
        )

        self.view_image = ft.Container(
            alignment=ft.alignment.center,
            width= Props.IMAGE_VIEW_WIDTH,
            height= Props.IMAGE_VIEW_HEIGHT,
            bgcolor=Props.PAGE_BGCOLOR,
            content=ft.Image(
                src="/images/example_01.png",
                width=1920,
                height=1280,
                fit=ft.ImageFit.COVER
            )
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

    def __get_cameras_options(self) -> list[ft.DropdownOption]:
        cameras_list: list[ft.DropdownOption] = []

        for camera_name in Props.CAMERAS_DICT.keys():
            cameras_list.append(
                ft.DropdownOption(text=str(camera_name))
            )

        return cameras_list

    def __camera_dropdown_changed(self, e):
        """
        Update camera selection for testing.
        :return:
        """
        Props.CURRENT_TEST_CAMERA = self.camera_dropdown.value

    def __test_button_clicked(self, e):
        """
        Action for test button
        :return:
        """
        
        __file_name: str = f"test_{datetime.now().strftime('%H-%M-%S')}.jpg"

        # Check if test file exists
        for f in os.listdir(Props.TEST_CAPTURES_DIRECTORY):
            path = os.path.join(Props.TEST_CAPTURES_DIRECTORY, f)
            os.remove(path)


        # VALIDATE
        # Check if is testing
        if is_testing():
            self.show_alert("Please wait, a test is already running.")
            return

        # Check if a camera is selected
        if test_camera_is_not_selected():
            self.show_alert("Please, select a camera to test")
            return
        
        required_props = {
            "ISO": Props.CURRENT_ISO,
            "SHUTTERSPEED": Props.CURRENT_SHUTTERSPEED,
            "FORMAT": Props.CURRENT_FORMAT
        }

        for name, value in required_props.items():
            if not value:
                self.show_alert("Please select a " + name + " value.")
                return

        
        # START TESTING
        self.show_alert("Testing camera " + self.camera_dropdown.value)
        Props.IS_TESTING = True

        __camera: str = Props.CAMERAS_DICT[Props.CURRENT_TEST_CAMERA]
        
        gp.capture_image(
            camera_port=__camera,
            download_path=Props.TEST_CAPTURES_DIRECTORY,
            file_name=__file_name
            )

        self.view_image.content.src = "/images/view_test/" + __file_name
        self.view_image.content.update()

        Props.IS_TESTING = False
        self.show_alert("Finished testing camera " + Props.CURRENT_TEST_CAMERA)
    
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