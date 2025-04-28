import flet as ft
import json
from src.resources.controls.custom.header_control import HeaderControl
from src.resources.properties import Properties as Props


def get_cameras():

    # Get json file
    with open("src/resources/assets/camera_values.json","r") as file:
        data = json.load(file)

    # Create container
    cameras = ft.Column()

    for camera in data['cameras']:
        #print(f"Camera: {camera['model']} ({camera['id']})")

        this_camera = ft.ExpansionTile(
            title=ft.Row(
                [
                    ft.Icon(ft.Icons.CAMERA_ALT_OUTLINED, size=Props.TAB_ICON_SIZE, visible=Props.TAB_ICON_ENABLED),
                    ft.Text(value=camera['model'])
                ]
            ),
            #subtitle=ft.Text(value=camera['id']),
            #show_trailing_icon=False,
            #affinity=ft.TileAffinity.LEADING,
            initially_expanded=False,
            controls_padding=Props.TAB_PADDING,
        )


        # Extraer fotos de cada cámara
        for photo in camera['photos']:
            filename = photo['filename']
            file_path = photo['file_path']
            capture_date = photo['capture_date']

            # Procesar la imagen (aquí solo imprimimos la información)
            #print(f"  Filename: {filename}")
            #print(f"  File Path: {file_path}")
            #print(f"  Capture Date: {capture_date}")
            #print("-" * 40)
            this_camera.controls.append(
                ft.ListTile(
                    title=ft.Row(
                        [
                            ft.Icon(ft.Icons.IMAGE_OUTLINED, size=Props.TAB_ICON_SIZE, visible=Props.TAB_ICON_ENABLED),
                            ft.Text(value=filename)
                        ]
                    )
                )
            )

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

        Args:
            page (ft.Page): The main page instance of the application.
        """
        super().__init__()
        self.title = "Explorer"
        self.bgcolor = Props.CONTAINER_BGCOLOR
        self.alignment = ft.alignment.top_left
        self.width = page.width * Props.EXPLORER_SIZE
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