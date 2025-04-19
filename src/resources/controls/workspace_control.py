import flet as ft
from src.resources.controls.tabs.preview_tab_control import PreviewTab
from src.resources.controls.tabs.properties_tab_control import PropertiesTab
from src.resources.controls.tabs.save_tab_control import SaveTab
from src.resources.controls.tabs.scan_tab_control import ScabTab
from src.resources.properties import *

class WorkspaceControl(ft.Container):
    """
    The main workspace area of the application.

    This container serves as the primary working space where
    users interact with content. It includes a header and can
    be expanded to fit available space.
    """

    def __init__(self, page: ft.Page):
        """
        Initializes the workspace control.

        Args:
            page (ft.Page): The main page instance of the application.
        """
        super().__init__()
        self.title = "Workspace"
        self.bgcolor = CONTAINER_BGCOLOR
        self.alignment = ft.alignment.top_left
        self.expand = 1
        self.padding = FRAME_PADDING

        self.content = ft.Column(
            [
                ft.Tabs(
                    selected_index=1,
                    animation_duration=ANIMATIONS_DURATION,
                    tabs=[
                        PreviewTab(PREVIEW_TAB_TITLE),
                        ScabTab(SCAN_TAB_TITLE),
                        SaveTab(SAVE_TAB_TITLE),
                        PropertiesTab(PROPERTIES_TAB_TITLE)
                    ],
                    expand=True
                )
            ]
        )
