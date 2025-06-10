import flet as ft
from src.resources.properties import Properties as Props
from src.resources.controls.custom.header_control import HeaderControl
from src.resources.utils.servers_controller import Servers


class ServerDialog:
    def __init__(self, page: ft.Page, title: str):
        self.page = page
        self.title = ft.Row(
            [
                ft.Icon(
                    name=ft.Icons.EDIT_DOCUMENT
                ),
                HeaderControl(title)
            ]
        )

        self.save_button = ft.ElevatedButton(
            text="Save",
            disabled=False,
            icon=ft.Icons.SAVE_SHARP,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
            height=Props.BUTTON_HEIGHT,
            width=Props.BUTTON_WIDTH,
            on_click=self.__save_button_clicked
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

        self.display_name_input = ft.TextField(label="Display Name", hint_text="Alias for this server")
        self.host_name_input = ft.TextField(label="Server", hint_text="http://<host>:<port>")

        self.dialog = ft.AlertDialog(
            modal=True,
            shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        self.title,
                        ft.Column(
                            [
                                self.display_name_input,
                                self.host_name_input                                
                            ]
                        ),
                        ft.Row(
                            [
                                self.save_button,
                                self.cancel_button
                            ],
                            alignment=ft.MainAxisAlignment.END
                        )
                    ],
                    spacing=Props.TAB_PADDING,
                    alignment=ft.MainAxisAlignment.CENTER,
                    height=Props.LOADING_DIALOG_HEIGHT+Props.BUTTON_HEIGHT*3,
                    width=Props.STAGE_CARD_WIDTH
                )
            )
        )

    def __save_button_clicked(self, e):
        
        if (
            self.display_name_input.value == None or
            self.display_name_input.value == ""
            ):
            self.show_alert("Input proper Display Name for host.")
            return

        if (
            self.host_name_input.value == None or
            self.host_name_input.value == ""
            ):
            self.show_alert("Input proper Host.")
            return

        Servers.add_server(
            display_name=self.display_name_input.value,
            host_name=self.host_name_input.value,
            paths=[]
        )

        self.show_alert(f"Added server: {self.display_name_input.value}")
        self.hide()
        self.update_servers_dropdown()

    def __close_button_clicked(self, e):
        self.hide()

    def update_servers_dropdown(self):
        server_list = Servers.get_available_servers()
        controls = []

        for server in server_list:
            controls.append(
                ft.DropdownOption(text=server)
            )

        Props.SERVERS_DROPDOWN.options = controls
        Props.SERVERS_DROPDOWN.update()

    def show(self):
        self.page.overlay.append(self.dialog)
        self.dialog.open = True
        self.page.update()

    def hide(self):
        self.dialog.open = False
        self.page.update()

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