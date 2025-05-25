import flet as ft
from src.resources.controls.custom.header_control import HeaderControl
from src.resources.properties import Properties as Props
from src.resources.controls.custom.stages.stage_scan import StageScan
from src.resources.controls.custom.stages.stage_filter import StageFilter
from src.resources.controls.custom.stages.stage_save import StageSave


class RoutinesTab(ft.Tab):
    """
    Routines tab in Workspace frame
    """

    def __init__(self, page: ft.Page, title: str):
        super().__init__()
        self.page = page
        self.text = title
        self.icon = ft.Icon(ft.Icons.CONSTRUCTION, size=Props.TAB_ICON_SIZE, visible=Props.TAB_ICON_ENABLED)

        # region Tab: Controls
        self.stage_type_dropdown = ft.Dropdown(
            options=[
                ft.DropdownOption(text="Scan"),
                ft.DropdownOption(text="Filter"),
                ft.DropdownOption(text="Save")
            ],
            value=None,
            label="Type",
            width = Props.CHECKBOX_WIDTH,
            border_radius = Props.BORDER_RADIUS,
            # on_change=self.__stage_type_dropdown_changed
        )

        self.add_stage_button = ft.ElevatedButton(
            text="Add",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
            height=Props.BUTTON_HEIGHT,
            width=Props.BUTTON_WIDTH,
            on_click=self.__add_stage_button_clicked
        )

        self.start_routine_button = ft.Container(
            height=Props.BUTTON_HEIGHT,
            expand=True,
            alignment=ft.alignment.center_right,
            content=ft.ElevatedButton(
                text="Start",
                icon=ft.Icons.PLAY_ARROW,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
                height=Props.BUTTON_HEIGHT,
                width=Props.BUTTON_WIDTH,
                # on_click=self.__start_routine_button_clicked
            )
        )

        self.stages_list_container = ft.Container(
            expand = 1,
            content = ft.Column(
                controls = [],
                scroll = ft.ScrollMode.AUTO
            )
        )

        self.routine_loader_dropdown = ft.Dropdown(
            options=[],
            value=None,
            label="Name",
            width = Props.CHECKBOX_WIDTH,
            border_radius = Props.BORDER_RADIUS,
            # on_change=self.__stage_type_dropdown_changed
        )

        self.apply_routine_button = ft.ElevatedButton(
            text="Add",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
            height=Props.BUTTON_HEIGHT,
            width=Props.BUTTON_WIDTH,
            # on_click=self.__stage_add_button_clicked
        )

        self.routine_name_input = ft.TextField(
            label="Name",
            width=Props.DROPDOWN_WIDTH,
            border_radius=Props.BORDER_RADIUS
        )

        self.add_new_routine_button = ft.ElevatedButton(
            text="Add",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
            height=Props.BUTTON_HEIGHT,
            width=Props.BUTTON_WIDTH,
            # on_click=self.__stage_add_button_clicked
        )

        self.update_routine_button = ft.ElevatedButton(
            text="Update",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
            height=Props.BUTTON_HEIGHT,
            width=Props.BUTTON_WIDTH,
            # on_click=self.__stage_add_button_clicked
        )

        self.delete_routine_button = ft.ElevatedButton(
            text="Delete",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
            height=Props.BUTTON_HEIGHT,
            width=Props.BUTTON_WIDTH,
            # on_click=self.__stage_add_button_clicked
        )
        # endregion

        # region Tabs: Content
        self.content = ft.Container(
            padding = Props.TAB_PADDING,
            content = ft.Column(
                [
                    # Stages: Selector
                    HeaderControl("Stages"),
                    ft.Row(
                        [
                            self.stage_type_dropdown,
                            self.add_stage_button,
                            self.start_routine_button
                        ]
                    ),
                    
                    # Stages: List
                    self.stages_list_container,
                    
                    # Stages: Routine saver
                    HeaderControl("Routine"),
                    ft.Row(
                        [   
                            # Routine saver: Left
                            ft.Column(
                                [
                                    self.routine_loader_dropdown,
                                    self.apply_routine_button
                                ]
                            ),

                            # Routine saver: Right
                            ft.Column(
                                [
                                    self.routine_name_input,
                                    ft.Row(
                                        [
                                            self.add_new_routine_button,
                                            self.update_routine_button,
                                            self.delete_routine_button
                                        ]
                                    )
                                ]
                            )
                        ]
                    )

                ]
            )
        )
        # endregion

    # region Controllers
    def __add_stage_button_clicked(self, e):
        # Validations
        stage_value = self.stage_type_dropdown.value
        Props.STAGES_NUMBER += 1

        if (stage_value == None):
            self.show_alert("Select a stage type to continue.")
            return
        
        # Add stage
        match stage_value:
            case "Scan":
                self.stages_list_container.content.controls.append(
                    StageScan(
                        stage_number = Props.STAGES_NUMBER,
                        card_list = self.stages_list_container
                    )
                )
                self.stages_list_container.content.update()

            case "Filter":
                self.stages_list_container.content.controls.append(
                    StageFilter(
                        stage_number = Props.STAGES_NUMBER,
                        card_list = self.stages_list_container
                    )
                )
                self.stages_list_container.content.update()


            case "Save":
                self.stages_list_container.content.controls.append(
                    StageSave(
                        stage_number = Props.STAGES_NUMBER,
                        card_list = self.stages_list_container
                    )
                )
                self.stages_list_container.content.update()


            case _:
                self.show_alert("Unrecognized stage type: " + stage_value)
                return


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
    # endregion
