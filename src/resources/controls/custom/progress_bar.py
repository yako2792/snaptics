import flet as ft
from src.resources.properties import Properties as Props
from src.resources.controls.custom.header_control import HeaderControl


class ProgressBar:
    def __init__(self, page: ft.Page, title: str):
        self.page = page
        self.title = HeaderControl(title)
        self.progress_bar = ft.ProgressBar(
            value=0,
            width=Props.STAGE_CARD_WIDTH
        )
        self.legend = ft.Text(
            value="In progress..."
        )

        self.percentage = ft.Text(
            value="0%"
        )

        self.close_button = ft.OutlinedButton(
            text="Close",
            disabled=True,
            icon=ft.Icons.CLOSE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
            height=Props.BUTTON_HEIGHT,
            width=Props.BUTTON_WIDTH,
            on_click=self.__close_button_clicked
        )
        self.cancel_button = ft.ElevatedButton(
            text="Stop",
            disabled=False,
            icon=ft.Icons.STOP,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
            height=Props.BUTTON_HEIGHT,
            width=Props.BUTTON_WIDTH,
            on_click=self.__cancel_button_clicked
        )

        self.dialog = ft.AlertDialog(
            modal=True,
            shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        self.title,
                        ft.Row(
                            [
                                self.progress_bar,
                                self.percentage
                            ]
                        ),
                        self.legend,
                        ft.Row(
                            [
                                self.cancel_button,
                                self.close_button
                            ],
                            alignment=ft.MainAxisAlignment.END
                        )
                    ],
                    spacing=Props.TAB_PADDING,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                height=Props.DIALOG_HEIGHT
            )
        )

    def show(self):
        self.page.overlay.append(self.dialog)
        self.dialog.open = True
        self.page.update()

    def hide(self):
        self.dialog.open = False
        self.page.update()
    
    def update_value(self, new_value: int):
        self.progress_bar.value = new_value
        self.percentage.value = str(int(new_value * 100)) + "%"

        if new_value == 1:
            self.close_button.disabled = False
            self.close_button.update()

            self.cancel_button.disabled = True
            self.cancel_button.update()

        self.progress_bar.update()
        self.percentage.update()

    def update_legend(self, new_legend: str):
        self.legend.value = new_legend
        self.legend.update()


    def __close_button_clicked(self, e):
        self.hide()

    def __cancel_button_clicked(self, e):
        self.hide()