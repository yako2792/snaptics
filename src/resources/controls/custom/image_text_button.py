import os
import flet as ft
from src.resources.properties import Properties as Props

class ImageTextButton(ft.Container):
    def __init__(self, file_path: str):
        super().__init__()
        self.name = os.path.basename(file_path)
        self.file_path = file_path

        self.content = ft.TextButton(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.IMAGE_OUTLINED, size=Props.TAB_ICON_SIZE, visible=Props.TAB_ICON_ENABLED),
                    ft.Text(value=self.name, color="white")
                ]
            ),
            on_click=self.__open_preview_tab
        )
    
    def __open_preview_tab(self, e):
        print(f"Opening image: {self.file_path}")
        Props.WORKSPACE_TAB.go_to_index_tab(0)
        Props.WORKSPACE_TAB.update_image_in_tab(self.file_path)