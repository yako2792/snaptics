import flet as ft
from src.resources.properties import Properties as Props
from src.resources.controls.custom.header_control import HeaderControl
from src.resources.utils.credentials_controller import Credentials


class CredentialsDialog:
    def __init__(self, page: ft.Page, title: str, parent):
        self.page = page
        self.parent_object = parent
        self.title = ft.Row(
            [
                ft.Icon(
                    name=ft.Icons.EDIT_DOCUMENT
                ),
                HeaderControl(title)
            ]
        )

        self.save_button = ft.ElevatedButton(
            text="Guardar",
            disabled=False,
            icon=ft.Icons.SAVE_SHARP,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
            height=Props.BUTTON_HEIGHT,
            width=Props.BUTTON_WIDTH,
            on_click=self.__save_button_clicked
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
        self.user_input = ft.TextField(label="Usuario", hint_text="Introduce tu usuario")
        self.password_input = ft.TextField(label="Contraseña", hint_text="Introduce tu contraseña", password=True, can_reveal_password=True)


        self.dialog = ft.AlertDialog(
            modal=True,
            shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        self.title,
                        ft.Column(
                            [
                                self.user_input,
                                self.password_input
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
                    height=Props.LOADING_DIALOG_HEIGHT+Props.BUTTON_HEIGHT*4,
                    width=Props.STAGE_CARD_WIDTH
                )
            )
        )

    def __close_button_clicked(self, e):
        self.hide()
    
    def __save_button_clicked(self, e):
        user_name = self.user_input.value
        password = self.password_input.value

        if user_name == None or user_name == "":
            self.show_alert("El nombre de usuario no debe estar vacío.")

        if password == None or password == "":
            self.show_alert("La contraseña no debe estar vacía.")

        Credentials.add_user_and_password(
            user_name=user_name,
            password=Credentials.encrypt_password(password)
        )

        self.hide()
        self.parent_object.reload_credentials()
        self.show_alert("Credenciales añadidas para el usuario: " + user_name)


    def show(self):
        if self.dialog not in self.page.overlay:
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