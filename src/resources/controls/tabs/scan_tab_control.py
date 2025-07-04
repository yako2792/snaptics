import flet as ft

from src.resources.controls.custom.header_control import HeaderControl
from src.resources.controls.custom.image_viewer_control import ImageViewer
from src.resources.controls.custom.options_control import OptionsControl
from src.resources.controls.custom.preset_control import PresetControl
from src.resources.controls.custom.use_control import UseControl
from src.resources.properties import Properties as Props


class ScanTab(ft.Tab):
    """
    Scan tab in Workspace frame

    This tab provides an interface for interacting with connected cameras,
    including viewing live or static previews and performing scan actions.
    """
    def __init__(self, page: ft.Page, title: str):
        super().__init__()
        self.page = page
        self.text = title
        self.icon = ft.Icon(ft.Icons.CAMERA, size=Props.TAB_ICON_SIZE, visible=Props.TAB_ICON_ENABLED)

        # Custom controls
        self.image_viewer = ImageViewer(self.page)
        self.options_control = OptionsControl()
        self.use_control = UseControl()
        self.presets_control = PresetControl(self.page, self.options_control, self.use_control)
        Props.OPTIONS_CONTROL = self.options_control
        Props.USE_CONTROL = self.use_control

        self.content=ft.Container(
            padding=Props.TAB_PADDING,
            content=ft.Column(
                [
                    # TOP
                    HeaderControl("Ver"),
                    self.image_viewer,

                    # BOTTOM
                    ft.Row(
                        [
                            ft.Container(
                                ft.Column(
                                    [
                                        HeaderControl("Opciones"),
                                        self.options_control
                                    ],
                                    alignment=ft.alignment.top_left
                                ),
                                alignment=ft.alignment.top_left,
                                expand=1
                            ),
                            ft.Container(
                                ft.Column(
                                    [
                                        HeaderControl("Usar cámaras"),
                                        self.use_control
                                    ],
                                    alignment=ft.alignment.top_left
                                ),
                                alignment=ft.alignment.top_left,
                                expand=1
                            )
                        ]
                    ),

                    # PRESETS
                    HeaderControl("Presets"),
                    self.presets_control
                ],
                scroll=ft.ScrollMode.AUTO
            )
        )

    def modify_button_radius(self, new_radius: int):
        """
        Modify Scan buttons border radius.
        :param new_radius: Radius value to be applied
        :return:
        """
        Props.BORDER_RADIUS = new_radius
        self.image_viewer.update_all_radius()
        self.options_control.update_all_radius()
        self.use_control.update_all_radius()
        self.presets_control.update_all_radius()
        self.update()

    def modify_view_image_size(self, width: int, height: int):
        """
        Modify image viewer size
        :param width: int width to be applied
        :param height: int height to be applied
        :return:
        """
        Props.IMAGE_VIEW_WIDTH = width
        Props.IMAGE_VIEW_HEIGHT = height

        self.image_viewer.update_view_image_size()
        self.update()
