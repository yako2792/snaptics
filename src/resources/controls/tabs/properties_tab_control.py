import json
import flet as ft
from src.resources.properties import Properties as Props
from src.camera_controller import GPhoto2 as gp
from src.resources.utils.servers_controller import Servers
from src.resources.controls.custom.loading_dialog import LoadingDialog
from src.resources.controls.custom.delete_server_dialog import DeleteServerDialog
from src.resources.controls.custom.server_dialog import ServerDialog
from src.resources.controls.custom.credentials_dialog import CredentialsDialog
from src.resources.controls.custom.update_server_dialog import UpdateServerDialog


def convert_percentage_to_width_height(width: int, height: int):
    """
    Converts a resolution (width, height) into a corresponding percentage
    based on a predefined mapping.

    Args:
        width (int): Width in pixels.
        height (int): Height in pixels.

    Returns:
        int: Corresponding percentage. Returns 0 if the resolution is not in the map.
    """
    resolutions_to_percentage = {
        (320, 180): 40,
        (426, 240): 50,
        (480, 270): 60,
        (540, 300): 70,
        (640, 360): 80,
        (800, 450): 90,
        (960, 540): 100
    }

    return resolutions_to_percentage.get((width, height), 0)

def convert_percentage_to_resolution(percentage: int):
    """
    Converts a percentage value into a resolution (width, height) using
    a predefined mapping.

    Args:
        percentage (int): Size percentage (between 40 and 100).

    Returns:
        tuple[int, int]: Resolution as (width, height). Returns (0, 0) if percentage is not in the map.
    """
    percentage_to_resolutions = {
        40: (320, 180),
        50: (426, 240),
        60: (480, 270),
        70: (540, 300),
        80: (640, 360),
        90: (800, 450),
        100: (960, 540)
    }

    return percentage_to_resolutions.get(percentage, (0, 0))

class PropertiesTab(ft.Tab):
    """
    Properties tab for the workspace UI.

    This tab contains configurable settings for multiple sections of the application:
    Explorer, Scan, and Camera.

    Attributes:
        text (str): Tab title text.
        icon (ft.Icon): Icon displayed on the tab.
        explorer_tab (ft.Tab): Reference to the explorer tab.
        preview_tab (ft.Tab): Reference to the preview tab.
        scan_tab (ft.Tab): Reference to the scan tab.
        content (ft.Column): Main container with expandable tiles for each configuration section.
    """

    def __init__(self, title: str, page: ft.Page, tab_references: dict[str, ft.Tab]):
        super().__init__()
        self.text = title
        self.icon = ft.Icon(ft.Icons.SETTINGS_INPUT_COMPONENT, size=Props.TAB_ICON_SIZE,visible=Props.TAB_ICON_ENABLED)
        self.page = page

        self.explorer_tab = tab_references[Props.EXPLORER_KEY]
        self.preview_tab = tab_references[Props.PREVIEW_KEY]
        self.scan_tab = tab_references[Props.SCAN_KEY]

        self.iso_dropdown = ft.Dropdown(
            options=self.__get_available_isos(),
            label="ISO",
            width=Props.DROPDOWN_WIDTH, 
            on_change=self.__iso_dropdown_changed
        )

        self.shutterspeed_dropdown = ft.Dropdown(
            options=self.__get_available_shutterspeeds(),
            label="SHUTTERSPEED",
            width=Props.DROPDOWN_WIDTH, 
            on_change=self.__shutterspeed_dropdown_changed
        )

        self.resolution_dropdown = ft.Dropdown(
            options=[
                ft.DropdownOption(text="1080p"),
                ft.DropdownOption(text="720p"),
                ft.DropdownOption(text="480p"),
                ft.DropdownOption(text="360p"),
                ft.DropdownOption(text="240p"),
                ft.DropdownOption(text="144p"),
            ],
            label="RESOLUTION",
            width=Props.DROPDOWN_WIDTH, 
            on_change=self.__resolution_dropdown_changed
        )

        self.servers_dropdown = ft.Dropdown(
            options=self.__get_available_servers(),
            label = "SERVERS",
            width = Props.DROPDOWN_WIDTH,
            on_change=self.__servers_dropdown_changed
        )
        Props.SERVERS_DROPDOWN = self.servers_dropdown

        self.credentials_dropdown = ft.Dropdown(
            # options=self.__get_available_credentials,
            label = "CREDENTIALS",
            width = Props.DROPDOWN_WIDTH,
            # on_change=self.__servers_dropdown_changed
        )


        self.rm_bg_threshold_input = ft.Slider(
            min=20,
            max=180, 
            divisions=160,
            label="{value}", 
            on_change=self.__rm_bg_threshold_input_changed, 
            value=Props.RM_BG_THRESHOLD
        )

        self.add_server_button = ft.ElevatedButton(
            text="Add",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
            height=Props.BUTTON_HEIGHT,
            width=Props.BUTTON_WIDTH,
            on_click=self.__add_server
        )
        self.update_server_button = ft.ElevatedButton(
            text="Update",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
            height=Props.BUTTON_HEIGHT,
            width=Props.BUTTON_WIDTH,
            on_click=self.__udpate_server
        )
        self.delete_server_button = ft.OutlinedButton(
            text="Delete",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
            height=Props.BUTTON_HEIGHT,
            width=Props.BUTTON_WIDTH,
            on_click=self.__delete_server
        )

        self.add_credentials_button = ft.ElevatedButton(
            text="Add",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
            height=Props.BUTTON_HEIGHT,
            width=Props.BUTTON_WIDTH,
            on_click=self.__add_credentials
        )
        self.update_credentials_button = ft.ElevatedButton(
            text="Update",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
            height=Props.BUTTON_HEIGHT,
            width=Props.BUTTON_WIDTH,
            # on_click=self.__update_preset
        )
        self.delete_credentials_button = ft.OutlinedButton(
            text="Delete",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=Props.BORDER_RADIUS)),
            height=Props.BUTTON_HEIGHT,
            width=Props.BUTTON_WIDTH,
            on_click=self.__delete_credentials
        )

        # Explorer settings
        self.explorer_settings: ft.ExpansionTile = ft.ExpansionTile(
            title=ft.Text(value=Props.EXPLORER_SETTINGS_TITLE),
            subtitle=ft.Text(value=Props.EXPLORER_SETTINGS_SUBTITLE),
            affinity=ft.TileAffinity.LEADING,
            initially_expanded=Props.INITIALLY_EXPANDED_PROPERTIES,
            controls_padding=Props.TAB_PADDING,
            controls=[
                ft.ListTile(
                    title=ft.Text("Explorer width: "),
                    subtitle=ft.Slider(min=20, max=60, divisions=4, label="{value}%", on_change=self.__explorer_width_slider_changed, value=Props.EXPLORER_SIZE*100)
                )
            ]
        )

        # Scan settings
        self.scan_settings: ft.ExpansionTile = ft.ExpansionTile(
            title=ft.Text(value=Props.SCAN_SETTINGS_TITLE),
            subtitle=ft.Text(value=Props.SCAN_SETTINGS_SUBTITLE),
            affinity=ft.TileAffinity.LEADING,
            initially_expanded=Props.INITIALLY_EXPANDED_PROPERTIES,
            controls_padding=Props.TAB_PADDING,
            controls=[
                ft.ListTile(
                    title=ft.Text("View test image size: "),
                    subtitle=ft.Slider(min=40, max=100, divisions=6, label="{value}%", on_change=self.__image_viewer_size_slider_changed, value=convert_percentage_to_width_height(Props.IMAGE_VIEW_WIDTH, Props.IMAGE_VIEW_HEIGHT))
                )
            ]
        )

        # Filter settings
        self.filter_settings: ft.ExpansionTile = ft.ExpansionTile(
            title=ft.Text(value=Props.FILTERS_SETTINGS_TITLE),
            subtitle=ft.Text(value=Props.FILTERS_SETTINGS_SUBTITLE),
            affinity=ft.TileAffinity.LEADING,
            initially_expanded=Props.INITIALLY_EXPANDED_PROPERTIES,
            controls_padding=Props.TAB_PADDING,
            controls=[
                ft.ListTile(
                    title=ft.Text("Remove background threshold: "),
                    subtitle=self.rm_bg_threshold_input 
                ),
                ft.ListTile(
                    title=ft.Text("Resize image resolution: "),
                    subtitle=self.resolution_dropdown 
                )
            ]
        )

        # Camera settings
        self.camera_settings: ft.ExpansionTile = ft.ExpansionTile(
            title=ft.Text(value=Props.CAMERA_SETTINGS_TITLE),
            subtitle=ft.Text(value=Props.CAMERA_SETTINGS_SUBTITLE),
            affinity=ft.TileAffinity.LEADING,
            initially_expanded=Props.INITIALLY_EXPANDED_PROPERTIES,
            controls_padding=Props.TAB_PADDING,
            controls=[
                ft.ListTile(
                    title=ft.Text("Camera ISO: "),
                    subtitle=self.iso_dropdown 
                ),
                ft.ListTile(
                    title=ft.Text("Camera SHUTTERSPEED: "),
                    subtitle=self.shutterspeed_dropdown
                ),

            ]
        )

        # Save settings
        self.save_settings: ft.ExpansionTile = ft.ExpansionTile(
            title=ft.Text(value=Props.SAVE_SETTINGS_TITLE),
            subtitle=ft.Text(value=Props.SAVE_SETTINGS_SUBTITLE),
            affinity=ft.TileAffinity.LEADING,
            initially_expanded=Props.INITIALLY_EXPANDED_PROPERTIES,
            controls_padding=Props.TAB_PADDING,
            controls=[
                ft.ListTile(
                    title=ft.Text("Servers: "),
                    subtitle=ft.Row(
                        [
                            self.servers_dropdown,
                            self.add_server_button,
                            self.update_server_button,
                            self.delete_server_button
                        ]
                    ) 
                ),
                ft.ListTile(
                    title=ft.Text("Credentials: "),
                    subtitle=ft.Row(
                        [
                            self.credentials_dropdown,
                            self.add_credentials_button,
                            self.update_credentials_button,
                            self.delete_credentials_button
                        ]
                    )
                ),

            ]
        )

        # Layout
        self.content = ft.Column(
            [
                self.explorer_settings,
                self.scan_settings,
                self.camera_settings,
                self.filter_settings,
                self.save_settings
            ],
            scroll=ft.ScrollMode.AUTO
        )

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

    def __get_available_isos(self):

        isos_list: list[ft.DropdownOption] = []

        for iso in Props.ISOS_DICT.keys():
            isos_list.append(
                ft.DropdownOption(text=str(iso))
            )

        return isos_list

    def __get_available_shutterspeeds(self):

        shutterspeeds_list: list[ft.DropdownOption] = []

        for shutterspeed in Props.SHUTTERSPEEDS_DICT.keys():
            shutterspeeds_list.append(
                ft.DropdownOption(text=str(shutterspeed))
            )

        return shutterspeeds_list

    def __explorer_width_slider_changed(self, e):
        """
        Callback for the Explorer width slider.

        Updates the width of the Explorer tab based on the selected slider value.
        """
        new_width = e.control.value / 100
        self.explorer_tab.modify_width(new_width)

    def __image_viewer_size_slider_changed(self, e):
        """
        Callback for the image viewer size slider.

        Converts the percentage to a resolution and updates the test image viewer size.
        """
        percentage = int(e.control.value)
        new_width, new_height = convert_percentage_to_resolution(percentage)
        self.scan_tab.modify_view_image_size(new_width, new_height)

    def __iso_dropdown_changed(self, e):
        """
        Callback for the iso dropdown menu.
        """

        Props.CURRENT_ISO = self.iso_dropdown.value

        loading_dialog = LoadingDialog(page=Props.PAGE, title="Wait")
        loading_dialog.show()
        loading_dialog.update_legend(f"Applying iso: {Props.CURRENT_ISO}")

        for camera in Props.CAMERAS_LIST:
            
            loading_dialog.update_legend(f"Applying iso to camera: {camera}")

            gp.set_config(
                camera_port=Props.CAMERAS_DICT[camera],
                camera_config=Props.ISO_CAMERA_CONFIG,
                config_value=Props.ISOS_DICT[Props.CURRENT_ISO]
                )
            
            loading_dialog.update_legend(f"Iso applied to camera: {camera}")
        
        loading_dialog.update_legend(f"Finish!")
        loading_dialog.hide()

    def __shutterspeed_dropdown_changed(self, e):
        """
        Callback for the shutterspeed dropdown menu.
        """

        Props.CURRENT_SHUTTERSPEED = self.shutterspeed_dropdown.value

        loading_dialog = LoadingDialog(page=Props.PAGE, title="Wait")
        loading_dialog.show()
        loading_dialog.update_legend(f"Applying shutterspeed: {Props.CURRENT_ISO}")

        for camera in Props.CAMERAS_LIST:

            loading_dialog.update_legend(f"Applying shutterspeed to camera: {camera}")

            gp.set_config(
                camera_port=Props.CAMERAS_DICT[camera],
                camera_config=Props.SHUTTERSPEED_CAMERA_CONFIG,
                config_value=Props.SHUTTERSPEEDS_DICT[Props.CURRENT_SHUTTERSPEED]
                )
            
            loading_dialog.update_legend(f"Shutterspeed applied to camera: {camera}")
        
        loading_dialog.update_legend(f"Finish!")
        loading_dialog.hide()


    def __resolution_dropdown_changed(self, e):
        """
        Callback for the resolution dropdown menu.
        """
        Props.FILTER_RESOLUTION_OUTPUT = self.resolution_dropdown.value

    def __get_available_servers(self):
        """
        Callback for the servers dropdown menu.
        """
        server_list = Servers.get_available_servers()
        controls = []

        for server in server_list:
            controls.append(
                ft.DropdownOption(text=server)
            )
        
        return controls
    
    def __servers_dropdown_changed(self, e):
        """
        Callback for the servers dropdown changed.
        """
        Props.SELECTED_SERVER = self.servers_dropdown.value

    def __add_server(self, e):
        """
        Callback for add server action.
        """
        allert = ServerDialog(page = Props.PAGE, title="Add Server")
        allert.show()

    def __udpate_server(self, e):
        """
        Callback for update server action.
        """

        if Props.SELECTED_SERVER == "":
            self.show_alert("Please select a server first.")
            return

        allert = UpdateServerDialog(page = Props.PAGE, title="Server details")
        allert.show()

    def __delete_server(self, e):
        """
        Callback for delete server action.
        """
        if Props.SELECTED_SERVER == "":
            self.show_alert("Please, select a server first.")
            return

        allert = DeleteServerDialog(page = Props.PAGE, title="Wait!")
        allert.show()
    
    def __add_credentials(self, e):
        """
        Callback for add credentials action.
        """
        allert = CredentialsDialog(page = Props.PAGE, title="Add Credentials")
        allert.show()


    def __delete_credentials(self, e):
        """
        Callback for delete credentials action.
        """
        allert = DeleteServerDialog(page = Props.PAGE, title="Wait!")
        allert.show()

    def __rm_bg_threshold_input_changed(self, e):
        """
        Callback for the remove background threshold input.
        """
        Props.RM_BG_THRESHOLD = self.rm_bg_threshold_input.value

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