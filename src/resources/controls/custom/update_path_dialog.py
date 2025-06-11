import flet as ft
from src.resources.properties import Properties as Props
from src.resources.controls.custom.header_control import HeaderControl
from src.resources.utils.servers_controller import Servers


class UpdatePathDialog:
    def __init__(self, page: ft.Page, title: str, parent_page):
        self.parent_page = parent_page
        self.page = page
        self.path_old = Props.SELECTED_PATH
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
        self.path_input = ft.TextField(value=Props.SELECTED_PATH, label="Path", hint_text="/output/directory")

        self.dialog = ft.AlertDialog(
            modal=True,
            shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        self.title,
                        ft.Column(
                            [
                                self.path_input
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

    def __close_button_clicked(self, e):
        self.hide()
        self.parent_page.show()

    def __save_button_clicked(self, e):

        if self.path_input.value == None:
            self.show_alert("Path should not be None.")
            return

        if self.path_input.value == "":
            self.show_alert("Path should not be empty.")
            return
        
        Servers.update_path_in_server(display_name=Props.SELECTED_SERVER, path_old=self.path_old, path_new=self.path_input.value)

        self.hide()
        self.parent_page.update_paths()
        self.parent_page.show()

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

    def show(self):

        if self.dialog not in self.page.overlay:
            self.page.overlay.append(self.dialog)

        self.dialog.open = True
        self.page.update()

    def hide(self):
        self.dialog.open = False
        self.page.overlay.remove(self.dialog)
        self.page.update()