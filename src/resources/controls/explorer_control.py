import flet as ft
from src.camera_controller import GPhoto2 as gp
from src.resources.controls.custom.header_control import HeaderControl
from src.resources.properties import Properties as Props


def get_cameras():

    # Create container
    cameras = ft.Column()

    for camera in Props.CAMERAS_DICT.keys():

        if camera == None:
            continue

        this_camera = ft.ExpansionTile(
            title=ft.Row(
                [
                    ft.Icon(ft.Icons.CAMERA_ALT_OUTLINED, size=Props.TAB_ICON_SIZE, visible=Props.TAB_ICON_ENABLED),
                    ft.Text(value=camera)
                ]
            ),
            initially_expanded=False,
            controls_padding=Props.TAB_PADDING,
        )

        # Extraer fotos de cada cámara
        # for photo in camera['photos']:
        #     filename = photo['filename']
        #     file_path = photo['file_path']
        #     capture_date = photo['capture_date']
        #
        #     this_camera.controls.append(
        #         ft.ListTile(
        #             title=ft.Row(
        #                 [
        #                     ft.Icon(ft.Icons.IMAGE_OUTLINED, size=Props.TAB_ICON_SIZE,
        #                             visible=Props.TAB_ICON_ENABLED),
        #                     ft.Text(value=filename)
        #                 ]
        #             )
        #         )
        #     )

        cameras.controls.append(this_camera)

    return cameras


class ExplorerControl(ft.Container):
    """
    Sidebar panel for file or element exploration.

    This container acts as the explorer panel where users can
    navigate and manage files or elements. It includes a header
    and is positioned on the left side of the layout.
    """

    def __init__(self, page: ft.Page):
        """
        Initializes the explorer control.
        :param page:
        """

        super().__init__()
        self.title = "Explorer"
        self.page = page
        self.bgcolor = Props.CONTAINER_BGCOLOR
        self.alignment = ft.alignment.top_left
        self.width = self.page.width * Props.EXPLORER_SIZE
        self.padding = Props.FRAME_PADDING
        self.cameras_list = get_cameras()

        # Cameras container
        self.content = ft.Container(
            content=ft.Column(
                [
                    HeaderControl("Cameras"),
                    self.cameras_list
                ]
            ),
            padding=Props.TAB_PADDING
        )

    def modify_width(self, new_width: float):
        """
        Modify Explorer frame width.
        :param new_width: New width to be set up
        :return: None
        """
        self.width = self.page.width * new_width
        Props.EXPLORER_SIZE = new_width
        self.update()