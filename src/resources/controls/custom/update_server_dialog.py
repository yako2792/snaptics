import flet as ft
from src.resources.properties import Properties as Props
from src.resources.controls.custom.header_control import HeaderControl
from src.resources.utils.servers_controller import Servers


class UpdateServerDialog:
    def __init__(self, page: ft.Page, title: str):
        self.page = page

        # Controls
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
            on_click=self.__close_button_clicked
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

        self.display_name_input = ft.TextField(
            label="Display Name",
            value=Props.SELECTED_SERVER,
            width=Props.STAGE_CARD_WIDTH,
        )

        self.host_name_input = ft.TextField(
            label="Host Name",
            value=Servers.get_server_ip(Props.SELECTED_SERVER),
            width=Props.STAGE_CARD_WIDTH
        )

        self.paths_dropdown = ft.Dropdown(
            options=self.__get_available_paths_in_server(),
            label="PATHS",
            width=Props.STAGE_CARD_WIDTH, 
            # on_change=self.__iso_dropdown_changed
        )

        # Layout
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
                                self.host_name_input,
                                self.paths_dropdown
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

    def __get_available_paths_in_server(self):
        """
        Callback for the servers dropdown menu.
        """
        paths = Servers.get_paths_in_server(server_name=Props.SELECTED_SERVER)
        controls = []

        for path in paths:
            controls.append(
                ft.DropdownOption(text=path)
            )
        
        return controls
    

    def __close_button_clicked(self, e):
        self.hide()

    def show(self):
        self.page.overlay.append(self.dialog)
        self.dialog.open = True
        self.page.update()

    def hide(self):
        self.dialog.open = False
        self.page.update()