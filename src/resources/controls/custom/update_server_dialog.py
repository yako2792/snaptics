import flet as ft
from src.resources.properties import Properties as Props
from src.resources.controls.custom.header_control import HeaderControl
from src.resources.utils.servers_controller import Servers
from src.resources.controls.custom.path_dialog import PathDialog
from src.resources.controls.custom.update_path_dialog import UpdatePathDialog
from src.resources.controls.custom.delete_path_dialog import DeletePathDialog

class UpdateServerDialog:
    def __init__(self, page: ft.Page, title: str):
        self.page = page
        self.add_path_dialog = None
        self.update_path_dialog = None

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
            width=Props.DROPDOWN_WIDTH - 40, 
            on_change=self.__iso_dropdown_changed
        )

        self.add_path_button = ft.ElevatedButton(
            text="Add",
            disabled=False,
            icon=ft.Icons.ADD,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
            height=Props.BUTTON_HEIGHT,
            width=Props.BUTTON_WIDTH,
            on_click=self.__add_path_button_clicked
        )

        self.remove_path_button = ft.OutlinedButton(
            text="Delete",
            disabled=False,
            icon=ft.Icons.DELETE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
            height=Props.BUTTON_HEIGHT,
            width=Props.BUTTON_WIDTH,
            on_click=self.__delete_path_button_clicked
        )

        self.update_path_button = ft.ElevatedButton(
            text="Update",
            disabled=False,
            icon=ft.Icons.UPDATE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
            height=Props.BUTTON_HEIGHT,
            width=Props.BUTTON_WIDTH,
            on_click=self.__update_path_button_clicked
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
                                ft.Row(
                                    [
                                        self.paths_dropdown,
                                        self.add_path_button,
                                        self.update_path_button,
                                        self.remove_path_button
                                    ]
                                )
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

    def __add_path_button_clicked(self, e):
        self.hide()
        add_path_dialog = PathDialog(page=self.page, title="Add", parent_page=self)
        add_path_dialog.show()
    
    def __update_path_button_clicked(self, e):
        if Props.SELECTED_PATH == "":
            self.show_alert("Please, first select a path.")
            return
        
        self.hide()
        update_path_dialog = UpdatePathDialog(page=self.page, title="Update", parent_page=self)
        update_path_dialog.show()

    def __delete_path_button_clicked(self, e):
        if Props.SELECTED_PATH == "":
            self.show_alert("Please, first select a path.")
            return
        
        self.hide()
        update_path_dialog = DeletePathDialog(page=self.page, title="Update", parent_page=self)
        update_path_dialog.show()

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
    
    def __iso_dropdown_changed(self, e):
        """
        Callback for the paths dropdown menu.
        """
        Props.SELECTED_PATH = self.paths_dropdown.value
    
    def __save_button_clicked(self, e):

        if self.host_name_input.value == "":
            self.show_alert("Hostname should not be empty.")
            return

        if self.host_name_input.value == None:
            self.show_alert("Hostname should not be None.")
            return
        
        if self.display_name_input.value == "":
            self.show_alert("Display Name should not be empty.")
            return

        if self.display_name_input.value == None:
            self.show_alert("Display Name should not be None.")
            return
        
        Servers.update_server(
            display_name_old=Props.SELECTED_SERVER,
            display_name_new=self.display_name_input.value,
            host_name=self.host_name_input.value,
            paths=None
        )

        self.hide()

    def __close_button_clicked(self, e):
        self.hide()

    def update_paths(self):
        self.paths_dropdown.options = self.__get_available_paths_in_server()
        self.paths_dropdown.update()

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
        self.page.update()