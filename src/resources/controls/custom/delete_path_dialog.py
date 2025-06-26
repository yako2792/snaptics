import flet as ft
from src.resources.properties import Properties as Props
from src.resources.controls.custom.header_control import HeaderControl
from src.resources.utils.servers_controller import Servers


class DeletePathDialog:
    def __init__(self, page: ft.Page, title: str, parent_page):
        self.page = page
        self.parent_page = parent_page
        self.title = ft.Row(
            [
                ft.Icon(
                    name=ft.Icons.ERROR_OUTLINE
                ),
                HeaderControl(title)
            ]
        )

        self.legend = ft.Text(
            value=f"¿Estás seguro de borrar el directorio '{Props.SELECTED_PATH}' ?"
        )

        self.cancel_button = ft.OutlinedButton(
            text="Cancelar",
            disabled=False,
            icon=ft.Icons.CLOSE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
            height=Props.BUTTON_HEIGHT,
            width=Props.BUTTON_WIDTH,
            on_click=self.__close_button_clicked
        )
        self.delete_button = ft.ElevatedButton(
            text="Borrar",
            disabled=False,
            icon=ft.Icons.DELETE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
            height=Props.BUTTON_HEIGHT,
            width=Props.BUTTON_WIDTH,
            on_click=self.__delete_button_clicked
        )

        self.dialog = ft.AlertDialog(
            modal=True,
            shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        self.title,
                        self.legend,
                        ft.Row(
                            [
                                self.delete_button,
                                self.cancel_button
                            ],
                            alignment=ft.MainAxisAlignment.END
                        )
                    ],
                    spacing=Props.TAB_PADDING,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                height=Props.LOADING_DIALOG_HEIGHT+Props.BUTTON_HEIGHT,
                width=Props.STAGE_CARD_WIDTH
            )
        )

    def __delete_button_clicked(self, e):
        Servers.remove_path_in_server(display_name=Props.SELECTED_SERVER, path = Props.SELECTED_PATH)
        self.show_alert(f"Se borró el directorio correctamente: {Props.SELECTED_PATH}")
        Props.SELECTED_PATH = ""
        self.hide()
        self.update_paths_options()
        self.parent_page.show()
    
    def __close_button_clicked(self, e):
        self.hide()
        self.parent_page.show()

    def show(self):
        if self.dialog not in self.page.overlay:
            self.page.overlay.append(self.dialog)
        self.dialog.open = True
        self.page.update()

    def hide(self):
        self.dialog.open = False
        self.page.update()

    def update_paths_options(self):
        self.parent_page.update_paths()

    def update_legend(self, new_legend: str):
        self.legend.value = new_legend
        self.legend.update()

    def show_alert(self, message: str):
        """
        Displays a temporary snackbar alert with the given message.

        Args:
            message (str): The message to display in the snackbar.
        """
        snackbar = ft.SnackBar(
            content=ft.Text(value=message),
            duration=2000
        )
        snackbar.open = True
        self.page.open(snackbar)
        self.page.update()