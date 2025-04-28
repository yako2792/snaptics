import flet as ft
from src.resources.properties import Properties as Props

class HeaderControl(ft.Container):
    """
    A header control used to display a title or label.

    This container represents a header section with a text value
    and a bottom border. It is typically used to label sections
    of the application interface.
    """

    def __init__(self, text: str):
        """
        Initializes the header control.

        Args:
            text (str): The text to be displayed in the header.
        """
        super().__init__()
        self.content = ft.Text(
            value=text,
            size=Props.CUSTOM_HEADER_TEXT_SIZE,
            weight=ft.FontWeight.BOLD
        )
        self.alignment = ft.alignment.top_left