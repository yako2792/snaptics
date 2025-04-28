import flet as ft
import json
from src.resources.controls.custom.header_control import HeaderControl
from src.resources.properties import Properties as Props


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

        self.content = ft.Column(
            [
                HeaderControl(self.title)
            ]
        )

"""
for camera in data['cameras']:
    print(f"Camera: {camera['model']} ({camera['id']})")
    
    # Extraer fotos de cada cámara
    for photo in camera['photos']:
        filename = photo['filename']
        file_path = photo['file_path']
        capture_date = photo['capture_date']
        
        # Procesar la imagen (aquí solo imprimimos la información)
        print(f"  Filename: {filename}")
        print(f"  File Path: {file_path}")
        print(f"  Capture Date: {capture_date}")
        print("-" * 40)

        
Camera: Canon EOS 5D (Canon_EOS_5D)
  Filename: IMG_001.jpg
  File Path: /store_00010001/IMG_001.jpg
  Capture Date: 2025-04-06T14:23:00
----------------------------------------
  Filename: IMG_002.jpg
  File Path: /store_00010001/IMG_002.jpg
  Capture Date: 2025-04-06T14:25:30
----------------------------------------
Camera: Nikon D750 (Nikon_D750)
  Filename: DSC_001.jpg
  File Path: /store_00010002/DSC_001.jpg
  Capture Date: 2025-04-06T15:00:00
----------------------------------------
  Filename: DSC_002.jpg
  File Path: /store_00010002/DSC_002.jpg
  Capture Date: 2025-04-06T15:02:30
----------------------------------------
"""