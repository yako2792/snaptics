import flet as ft
from ..controls.explorer_control import ExplorerControl
from ..controls.workspace_control import WorkspaceControl

class Layout(ft.Row):
    """
    Main layout of the application based on a Row.

    This layout organizes two main controls:
    - 'ExplorerControl': A panel for file or element exploration.
    - 'WorkspaceControl': The main workspace area of the application.

    Both controls are arranged horizontally within a `Row`.
    """

    def __init__(self, page: ft.Page):
        """
        Initializes the main layout.

        Args:
            page (ft.Page): The main page instance of the application.
        """
        super().__init__()
        self.page = page
        self.expand = 1

        self.explorer_control = ExplorerControl(self.page)
        self.workspace_control = WorkspaceControl(self.page)

        self.controls = [
            self.explorer_control,
            self.workspace_control
        ]