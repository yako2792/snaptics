import flet as ft
from src.resources.properties import Properties as Props
from src.resources.controls.custom.header_control import HeaderControl
from src.resources.utils.credentials_controller import Credentials


class DeleteCredentialsDialog:
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
            value=f"Are you sure you want to delete credential '{Props.SELECTED_USER}' ?"
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
        Credentials.remove_user(user_name=Props.SELECTED_USER)
        self.show_alert(f"Credential deleted: {Props.SELECTED_USER}")
        Props.SELECTED_USER = ""
        self.hide()
        self.update_credentials_options()
    
    def __close_button_clicked(self, e):
        self.hide()

    def show(self):
        self.page.overlay.append(self.dialog)
        self.dialog.open = True
        self.page.update()

    def hide(self):
        self.dialog.open = False
        self.page.update()

    def update_credentials_options(self):

        credentials_list = Credentials.get_available_users()
        controls = []

        for credential in credentials_list:
            controls.append(
                ft.DropdownOption(text=credential)
            )

        Props.CREDENTIALS_DROPDOWN.options = controls
        Props.CREDENTIALS_DROPDOWN.update()

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