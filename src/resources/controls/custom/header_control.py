import flet as ft

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
            weight=ft.FontWeight.BOLD
        )