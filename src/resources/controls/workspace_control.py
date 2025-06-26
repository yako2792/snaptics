import flet as ft

from src.resources.controls.explorer_control import ExplorerControl
from src.resources.controls.tabs.preview_tab_control import PreviewTab
from src.resources.controls.tabs.properties_tab_control import PropertiesTab
from src.resources.controls.tabs.scan_tab_control import ScanTab
from src.resources.controls.tabs.routines_tab_control import RoutinesTab
from src.resources.properties import Properties as Props

class   WorkspaceControl(ft.Container):
    """
    The main workspace area of the application.

    This container serves as the primary working space where
    users interact with content. It includes a header and can
    be expanded to fit available space.
    """

    def __init__(self, page: ft.Page, explorer_control: ExplorerControl):
        """
        Initializes the workspace control.

        Args:
            page (ft.Page): The main page instance of the application.
        """
        super().__init__()
        self.page = page
        self.title = "Espacio de trabajo"
        self.bgcolor = Props.CONTAINER_BGCOLOR
        self.alignment = ft.alignment.top_left
        self.expand = 1
        self.padding = Props.FRAME_PADDING
        Props.WORKSPACE_TAB = self

        # Used tabs
        self.explorer_control = explorer_control
        self.preview_tab = PreviewTab(Props.PREVIEW_TAB_TITLE, self.page)
        self.scan_tab = ScanTab(self.page, Props.SCAN_TAB_TITLE)
        self.routines_tab = RoutinesTab(self.page, Props.ROUTINES_TAB_TITLE)

        self.properties_tab = PropertiesTab(
            Props.PROPERTIES_TAB_TITLE,
            self.page,
            {
                Props.EXPLORER_KEY: self.explorer_control,
                Props.PREVIEW_KEY: self.preview_tab,
                Props.SCAN_KEY: self.scan_tab,
                Props.ROUTINES_KEY: self.routines_tab
            }
        )

        self.tabs = ft.Tabs(
            selected_index=1,
            animation_duration = Props.ANIMATIONS_DURATION,
            tabs=[
                self.preview_tab,
                self.scan_tab,
                self.routines_tab,
                self.properties_tab
            ],
            expand=True
        )

        self.content = ft.Column(
            [
                self.tabs
            ]
        )

    def go_to_index_tab(self, index: int):
        self.tabs.selected_index = index
        self.tabs.update()
    
    def update_image_in_tab(self, file_path: str):
        self.preview_tab.update_image_preview(file_path)
        