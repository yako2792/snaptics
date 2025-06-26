import os
import flet as ft
from src.resources.properties import Properties as Props
from src.resources.controls.custom.header_control import HeaderControl


class ResetDialog:
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
            value=f"¿Estás seguro de que quieres reiniciar el sistema? Esta acción reiniciará el dispositivo y puede provocar la pérdida de cambios no guardados.",
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
            text="Reiniciar",
            disabled=False,
            icon=ft.Icons.RESTART_ALT,
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
        self.hide()
        os.system("sudo /sbin/reboot now")
    
    def __close_button_clicked(self, e):
        self.hide()

    def show(self):
        if self.dialog not in self.page.overlay:
            self.page.overlay.append(self.dialog)
        self.dialog.open = True
        self.page.update()

    def hide(self):
        self.dialog.open = False
        self.page.update()

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