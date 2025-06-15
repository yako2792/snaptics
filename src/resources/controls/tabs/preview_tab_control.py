import flet as ft
from src.resources.properties import Properties as Props
from src.resources.controls.custom.header_control import HeaderControl


class PreviewTab(ft.Tab):
    """
    Preview tab in Workspace frame
    """
    def __init__(self, title: str, page: ft.Page):
        super().__init__()
        self.page = page
        self.text = title
        self.icon = ft.Icon(ft.Icons.PREVIEW, size=Props.TAB_ICON_SIZE, visible=Props.TAB_ICON_ENABLED)

        # Controls
        self.source_image = ft.Image(
            src="/images/example_01.png",
            fit=ft.ImageFit.CONTAIN
        )

        self.view_image = ft.Container(
            alignment=ft.alignment.center,
            expand=True,
            bgcolor=Props.PAGE_BGCOLOR,
            content=self.source_image
        )

        # Content
        self.content=ft.Container(
            padding=Props.TAB_PADDING,
            expand=True,
            content=ft.Column(
                [
                    HeaderControl("Image"),
                    self.view_image
                ],
                scroll=ft.ScrollMode.AUTO,
                expand=True
            )
        )

    # Methods
    def update_image_preview(self, file_path: str):
        relative_path = file_path.split("images", 1)[1]
        relative_path = "images" + relative_path
        
        self.source_image.src = relative_path
        self.source_image.update()