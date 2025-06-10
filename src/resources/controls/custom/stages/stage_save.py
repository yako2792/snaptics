import os
import json
import flet as ft
from src.resources.controls.custom.header_control import HeaderControl
from src.resources.properties import Properties as Props

class StageSave(ft.Container):

    def __init__(self, stage_number: int, card_list: ft.Container):
        super().__init__()
        self.type = ": Save "
        self.card_list = card_list
        self.stage_number = stage_number
        self.stage_name: str = "Stage " + str(self.stage_number) + self.type
        self.margin = Props.MARGIN_ALL
        self.padding = Props.TAB_PADDING
        self.width = Props.STAGE_CARD_WIDTH
        self.expand = True

        # region Stage card: Controls
        self.header_text = HeaderControl(self.stage_name)

        self.server_dropdown = ft.Dropdown(
            label="Server",
            options=[ft.dropdown.Option(name) for name in self.__load_available_servers()],
            width=Props.DROPDOWN_WIDTH * 0.7,
            border_radius=Props.BORDER_RADIUS,
            # on_change=self.__server_dropdown_changed
        )

        self.path_dropdown = ft.Dropdown(
            label="Path",
            options=[ft.dropdown.Option(name) for name in self.__load_available_paths()],
            width=Props.DROPDOWN_WIDTH * 0.7,
            border_radius=Props.BORDER_RADIUS,
            # on_change=self.__path_dropdown_changed
        )

        self.credentials_dropdown = ft.Dropdown(
            label="Credentials",
            options=[ft.dropdown.Option(name) for name in self.__load_available_credentials()],
            width=Props.DROPDOWN_WIDTH * 1.43,
            border_radius=Props.BORDER_RADIUS,
            # on_change=self.__path_dropdown_changed
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
        return ["127.0.0.1", "0.0.0.0"]
    
    def __load_available_paths(self):
        """
        Returns the available paths.
        """
        return ["/path/psd/all", "/path/jpg", "/path/seed/"]
    
    def __load_available_credentials(self):
        """
        Returns the available credentials.
        """
        return ["Server1_Credentials", "Server2_Credentials"]
    
    def __server_dropdown_changed(self, e):
        Props.CURRENT_ROUTINE["stages"][self.stage_number - 1]["config"] = {
            "server": self.server_dropdown.value
        }
        
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
