import flet as ft
from src.resources.properties import Properties as Props

def test_camera_is_not_selected():
    return not all([Props.CURRENT_TEST_CAMERA])

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
            options=[
                ft.DropdownOption(text="Camera 1"),
                ft.DropdownOption(text="Camera 2"),
                ft.DropdownOption(text="Camera 3")
            ],
            label="Camera",
            width=Props.DROPDOWN_WIDTH,
            border_radius=Props.BORDER_RADIUS,
            on_change=self.__camera_dropdown_changed
        )

        self.test_button = ft.ElevatedButton(
            text="Test",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
            height=Props.BUTTON_HEIGHT, 
            on_click=self.__test_button_clicked
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

        # VALIDATIONS
        if test_camera_is_not_selected():
            self.show_alert("Please, select a camera to test")
            return
        
        self.show_alert(f"Testing camera {Props.CURRENT_TEST_CAMERA}")
    
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