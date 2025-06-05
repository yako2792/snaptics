import flet as ft
from src.resources.properties import Properties as Props
from src.resources.controls.custom.header_control import HeaderControl


class LoadingDialog:
    def __init__(self, page: ft.Page, title: str):
        self.page = page
        self.title = HeaderControl(title)
        self.progress_bar = ft.ProgressBar(
            value=0,
            width=Props.STAGE_CARD_WIDTH
        )

        self.loading_gif = ft.Image(
            src="/images/gifs/loading.gif",
            width=Props.GIF_SIZE,
            height=Props.GIF_SIZE
        )

        self.legend = ft.Text(
            value="Loading..."
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
                                self.loading_gif,
                                self.legend
                            ]
                        )
                    ],
                    spacing=Props.TAB_PADDING,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                height=Props.LOADING_DIALOG_HEIGHT
            )
        )

    def show(self):
        self.page.overlay.append(self.dialog)
        self.dialog.open = True
        self.page.update()

    def hide(self):
        self.dialog.open = False
        self.page.update()

    def update_legend(self, new_legend: str):
        self.legend.value = new_legend
        self.legend.update()