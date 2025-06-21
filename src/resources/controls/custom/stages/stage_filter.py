import os
import json
import flet as ft
from src.resources.controls.custom.header_control import HeaderControl
from src.resources.properties import Properties as Props

class StageFilter(ft.Container):

    def __init__(self, stage_number: int, card_list: ft.Container):
        super().__init__()
        self.type = ": Filter "
        self.card_list = card_list
        self.stage_number = stage_number
        self.stage_name: str = "Stage " + str(self.stage_number) + self.type
        self.margin = Props.MARGIN_ALL
        self.padding = ft.padding.only(left=Props.TAB_PADDING+50, top=Props.TAB_PADDING, right=Props.TAB_PADDING, bottom=Props.TAB_PADDING)
        self.width = Props.STAGE_CARD_WIDTH
        self.expand = True

        # region Stage card: Controls
        self.header_text = HeaderControl(self.stage_name)

        self.filter_dropdown = ft.Dropdown(
            label="Filters",
            options=[ft.dropdown.Option(name) for name in self.__load_filters()],
            width=Props.DROPDOWN_WIDTH,
            border_radius=Props.BORDER_RADIUS,
            on_change=self.__filter_dropdown_changed
        )

        self.delete_button = ft.IconButton(
            icon = ft.Icons.DELETE,
            icon_size = Props.TAB_ICON_SIZE,
            on_click = self.__delete_button_clicked
        )

        self.resolution_dropdown = ft.Dropdown(
            label="Resolution",
            options=[ft.dropdown.Option(name) for name in self.__load_resolutions()],
            width=Props.DROPDOWN_WIDTH,
            border_radius=Props.BORDER_RADIUS,
            visible=False,
            on_change = self.__resolution_dropdown_changed
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
                self.filter_dropdown,
                self.resolution_dropdown
            ]
        )
        # endregion

    # region Stage card: Controllers
    def __load_filters(self):
        """
        Read filters available in Filter.py.
        :return: list with all presets
        """
        return [
            "Remove background",
            "Resize image",
            "Fisheye correction",
            "CA Correction",
            "Crop Center",
        ]

    def __load_resolutions(self):
        """
        Read resolutions available in Filter.py.
        :return: list with all presets
        """
        return [
            "Small",
            "Medium",
            "Large",
            "Model"
        ]
    
    def __filter_dropdown_changed(self, e):
        Props.CURRENT_ROUTINE["stages"][self.stage_number - 1]["config"] = {
            "filter_name": self.filter_dropdown.value
        }

        if self.filter_dropdown.value == "Crop Center":
            self.add_resolution_dropdown()
        else:
            self.remove_resolution_dropdown()

    def add_resolution_dropdown(self):
        self.resolution_dropdown.visible = True
        self.content.update()
   
    def remove_resolution_dropdown(self):
        self.resolution_dropdown.visible = False
        self.content.update()

        # Reset resolution dropdown value
        self.resolution_dropdown.value = None

    def __resolution_dropdown_changed(self, e):
        Props.CURRENT_ROUTINE["stages"][self.stage_number - 1]["config"]["resolution"] = self.resolution_dropdown.value

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
