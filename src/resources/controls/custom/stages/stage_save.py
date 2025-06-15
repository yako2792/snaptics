import os
import json
import flet as ft
from src.resources.controls.custom.header_control import HeaderControl
from src.resources.properties import Properties as Props
from src.resources.utils.servers_controller import Servers
from src.resources.utils.credentials_controller import Credentials

class StageSave(ft.Container):

    def __init__(self, stage_number: int, card_list: ft.Container):
        super().__init__()
        self.type = ": Save "
        self.card_list = card_list
        self.stage_number = stage_number
        self.stage_name: str = "Stage " + str(self.stage_number) + self.type
        self.margin = Props.MARGIN_ALL
        self.padding = ft.padding.only(left=Props.TAB_PADDING+100, top=Props.TAB_PADDING, right=Props.TAB_PADDING, bottom=Props.TAB_PADDING)
        self.width = Props.STAGE_CARD_WIDTH
        self.expand = True

        # region Stage card: Controls
        self.header_text = HeaderControl(self.stage_name)

        self.server_dropdown = ft.Dropdown(
            label="Server",
            options=[ft.dropdown.Option(name) for name in self.__load_available_servers()],
            width=Props.DROPDOWN_WIDTH * 0.7,
            border_radius=Props.BORDER_RADIUS,
            on_change=self.__server_dropdown_changed
        )

        self.path_dropdown = ft.Dropdown(
            label="Path",
            hint_text="Select a server",
            options=[],
            width=Props.DROPDOWN_WIDTH * 0.7,
            border_radius=Props.BORDER_RADIUS,
            on_change=self.__path_dropdown_changed
        )

        self.credentials_dropdown = ft.Dropdown(
            label="Credentials",
            options=[ft.dropdown.Option(name) for name in self.__load_available_credentials()],
            width=Props.DROPDOWN_WIDTH * 1.43,
            border_radius=Props.BORDER_RADIUS,
            on_change=self.__credentials_dropdown_changed
        )

        self.delete_button = ft.IconButton(
            icon = ft.Icons.DELETE,
            icon_size = Props.TAB_ICON_SIZE,
            on_click = self.__delete_button_clicked
        )

        # endregion

        # region Stage card: Content
        self.content = ft.Column(
            [
                ft.Row(
                    [
                        self.header_text,
                        self.delete_button
                    ]
                ),
                ft.Row(
                    [
                        self.server_dropdown,
                        self.path_dropdown
                    ]
                ),
                self.credentials_dropdown
            ]
        )
        # endregion

    # region Stage card: Controllers
    def __load_available_servers(self):
        """
        Returns the available servers.
        """
        return Servers.get_available_servers()
    
    def __load_available_paths(self):
        """
        Returns the available paths.
        """
        self.path_dropdown.value = None
        self.path_dropdown.options = [ft.dropdown.Option(path) for path in Servers.get_paths_in_server(Props.USE_SERVER)]
        self.path_dropdown.update()
    
    def __load_available_credentials(self):
        """
        Returns the available credentials.
        """
        return Credentials.get_available_users()
    
    def __path_dropdown_changed(self, e):
        """
        Set the use path value in global properties.
        """
        Props.USE_PATH = self.path_dropdown.value

    def __server_dropdown_changed(self, e):
        
        Props.USE_SERVER = self.server_dropdown.value
        Props.USE_PATH = ""
        self.__load_available_paths()

        address = Servers.get_server_ip(display_name=Props.USE_SERVER)
        address_split = address.split(':')
        Props.USE_IP = address_split[0]
        Props.USE_PORT = address_split[1]

    def __credentials_dropdown_changed(self, e):
        Props.USE_USER = self.credentials_dropdown.value
        Props.USE_PASSWORD = Credentials.get_user_password(Props.USE_USER)
        
        
    def __delete_button_clicked(self, e):
        self.card_list.content.controls.remove(self)
        new_cards_order = []

        Props.STAGES_NUMBER -= 1
        Props.CURRENT_ROUTINE["stages"].pop(self.stage_number-1)

        # Reindex
        for index, card in enumerate(self.card_list.content.controls, start=1):
            card.stage_number = index
            card.stage_name = "Stage " + str(index) + card.type 

            card.header_text.content.value = "Stage " + str(index) + card.type 
            card.header_text.update()

            new_cards_order.append(card)

        self.card_list.content.controls = new_cards_order
        self.card_list.content.update()
    # endregion
