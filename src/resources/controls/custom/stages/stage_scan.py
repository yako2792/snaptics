import os
import json
import flet as ft
from src.resources.controls.custom.header_control import HeaderControl
from src.resources.properties import Properties as Props

class StageScan(ft.Container):

    def __init__(self, stage_number: int, card_list: ft.Container):
        super().__init__()
        self.type = ": Scan "
        self.card_list = card_list
        self.stage_number = stage_number
        self.stage_name: str = "Stage " + str(self.stage_number) + self.type
        self.margin = Props.MARGIN_ALL
        self.padding = Props.TAB_PADDING
        self.width = Props.STAGE_CARD_WIDTH
        self.expand = True

        # region Stage card: Controls
        self.header_text = HeaderControl(self.stage_name)

        self.preset_dropdown = ft.Dropdown(
            label="Preset",
            options=[ft.dropdown.Option(name) for name in self.__load_presets()],
            width=Props.DROPDOWN_WIDTH,
            border_radius=Props.BORDER_RADIUS,
            on_change=self.__preset_dropdown_changed
        )

        self.product_code_input = ft.TextField(
            label="Id",
            hint_text="Product Id. e.g., 023498",
            width=Props.DROPDOWN_WIDTH,
            border_radius=Props.BORDER_RADIUS,
            on_change=self.__product_id_changed
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
                self.preset_dropdown,
                self.product_code_input
            ]
        )
        # endregion

    # region Stage card: Controllers
    def __load_presets(self):
        """
        Read presets in json file.
        :return: dict with all presets
        """
        if not os.path.exists(Props.PRESETS_PATH):
            with open(Props.PRESETS_PATH, "w") as file:
                json.dump({}, file, indent=2)
            return {}
        with open(Props.PRESETS_PATH, "r") as file:
            return json.load(file)
    
    def __preset_dropdown_changed(self, e):
        Props.CURRENT_ROUTINE["stages"][self.stage_number - 1]["config"] = {
            "preset_name": self.preset_dropdown.value
        }

    def __product_id_changed(self, e):
        Props.PRODUCT_ID = self.product_code_input.value
        
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
