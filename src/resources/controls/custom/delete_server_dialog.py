import flet as ft
from src.resources.properties import Properties as Props
from src.resources.controls.custom.header_control import HeaderControl
from src.resources.utils.servers_controller import Servers


class DeleteServerDialog:
    def __init__(self, page: ft.Page, title: str):
        self.page = page
        self.title = ft.Row(
            [
                ft.Icon(
                    name=ft.Icons.ERROR_OUTLINE
                ),
                HeaderControl(title)
            ]
        )

        self.legend = ft.Text(
            value=f"Are you sure you want to delete server '{Props.SELECTED_SERVER}' ?"
        )

        self.cancel_button = ft.OutlinedButton(
            text="Cancel",
            disabled=False,
            icon=ft.Icons.CLOSE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
            height=Props.BUTTON_HEIGHT,
            width=Props.BUTTON_WIDTH,
            on_click=self.__close_button_clicked
        )
        self.delete_button = ft.ElevatedButton(
            text="Delete",
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
        Servers.remove_server(display_name=Props.SELECTED_SERVER)
        self.show_alert(f"Server deleted: {Props.SELECTED_SERVER}")
        Props.SELECTED_SERVER = ""
        self.hide()
        self.update_server_options()
    
    def __close_button_clicked(self, e):
        self.hide()

    def show(self):
        self.page.overlay.append(self.dialog)
        self.dialog.open = True
        self.page.update()

    def hide(self):
        self.dialog.open = False
        self.page.update()

    def update_server_options(self):

        server_list = Servers.get_available_servers()
        controls = []

        for server in server_list:
            controls.append(
                ft.DropdownOption(text=server)
            )

        Props.SERVERS_DROPDOWN.options = controls
        Props.SERVERS_DROPDOWN.update()

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