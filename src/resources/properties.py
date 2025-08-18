"""
This module contains configurable properties for the Fleet-based web application.
It centralizes settings, ensuring easy configuration and avoiding hardcoding values in the codebase.
"""

import os
from cryptography.fernet import Fernet
from flet import Page, Container, Dropdown, Tab
from src.camera_controller import GPhoto2 as gp

class Properties:
    # GENERAL PAGE
    PAGE_TITLE: str = "Snaptics"
    PAGE_PADDING: int = 10
    PAGE_BGCOLOR: str = "#2C323D"
    CONTAINER_BGCOLOR: str = "#2E3541"
    ANIMATIONS_DURATION: int = 0
    MIN_WINDOW_SIZE: tuple[int,int] = (1280,720)
    CUSTOM_HEADER_TEXT_SIZE: int = 18
    PRESETS_PATH:str = os.path.join(
        os.path.dirname(__file__),
        "..", "resources", "assets", "presets", "presets.json"
    )
    PAGE: Page = None
    
    ROUTINES_DIRECTORY: str = "src/resources/assets/routines/routines.json"
    SERVERS_DIRECTORY: str = "src/resources/assets/servers.json"
    CREDENTIALS_DIRECTORY: str = "src/resources/assets/credentials/credentials.json"
    CAPTURES_DIRECTORY: str = "src/resources/assets/images/captures/"
    TEST_CAPTURES_DIRECTORY: str = "src/resources/assets/images/view_test/"
    FILTERED_IMAGES_DIRECTORY: str = "src/resources/assets/images/filtered_images/"
    
    OPTIONS_CONTROL: Container = None
    USE_CONTROL: Container = None
    PRESETS: Container = None
    ROUTINES: Tab = None

    # FRAMES
    EXPLORER_SIZE: float = 0.3
    FRAME_PADDING: int = 3

    # TABS
    PREVIEW_TAB_TITLE: str = "Vista previa"
    SCAN_TAB_TITLE: str = "Capturar"
    ROUTINES_TAB_TITLE: str = "Rutinas"
    PREVIEW_KEY: str = "Preview"
    SCAN_KEY: str = "Scan"
    ROUTINES_KEY: str = "Routines"
    EXPLORER_KEY: str = "Explorer"
    PROPERTIES_TAB_TITLE: str = "Propiedades"
    WORKSPACE_TAB: Container = None

    TAB_ICON_SIZE: int = 18
    TAB_ICON_ENABLED: bool = True
    TAB_PADDING: int = 15

    EXPLORER_CAMERAS: Container = None
    IMAGES_LIST_CAMERA1: list = []
    IMAGES_LIST_CAMERA2: list = []
    IMAGES_LIST_CAMERA3: list = []

    # CONTROLS STYLE
    IMAGE_VIEW_WIDTH: int = 640
    IMAGE_VIEW_HEIGHT: int = 360
    CHECKBOX_WIDTH: int = 350
    CHECKBOX_HEIGHT: int = 49
    DROPDOWN_WIDTH: int = 365
    BUTTON_WIDTH: int = 115
    BUTTON_HEIGHT: int = 49
    BORDER_RADIUS: int = 0
    MARGIN_ALL: int = 15
    STAGE_CARD_WIDTH: int = 640
    DIALOG_HEIGHT: int = 160
    GIF_SIZE: int = 30
    LOADING_DIALOG_HEIGHT: int = 90

    # PROPERTIES TAB
    EXPLORER_SETTINGS_TITLE: str = "Propiedades: Explorador"
    EXPLORER_SETTINGS_SUBTITLE: str = "Personaliza algunos valores del panel Explorador."
    SCAN_SETTINGS_TITLE: str = "Propiedades: Pestaña Capturar"
    SCAN_SETTINGS_SUBTITLE: str = "Personaliza algunos valores de la pestaña Escaneo."
    CAMERA_SETTINGS_TITLE: str = "Propiedades: Cámaras"
    CAMERA_SETTINGS_SUBTITLE: str = "Personaliza algunas propiedades de las cámaras."
    SAVE_SETTINGS_TITLE: str = "Propiedades: Guardar"
    SAVE_SETTINGS_SUBTITLE: str = "Modifica las opciones disponibles en la etapa de guardado."
    SYSTEM_SETTINGS_TITLE: str = "Propiedades: Sistema"
    SYSTEM_SETTINGS_SUBTITLE: str = "Opciones que afectan directamente al sistema. ¡Ten cuidado con ellas!"
    FILTERS_SETTINGS_TITLE: str = "Propiedades: Filtros"
    FILTERS_SETTINGS_SUBTITLE: str = "Personaliza algunas propiedades de los filtros."
    INITIALLY_EXPANDED_PROPERTIES: bool = False

    # SCAN TAB
    CURRENT_FREQUENCY: str = ""
    CURRENT_FORMAT: str = ""
    CURRENT_RESOLUTION: str = ""
    CURRENT_ISO: str = ""
    CURRENT_SHUTTERSPEED: str = ""
    CURRENT_USE_CAMERA1: str = False
    CURRENT_USE_CAMERA2: str = False
    CURRENT_USE_CAMERA3: str = False
    CURRENT_TEST_CAMERA: str = ""

    CAMERA1_DOWNLOAD_PATH: str = CAPTURES_DIRECTORY + "camera_1/"
    CAMERA2_DOWNLOAD_PATH: str = CAPTURES_DIRECTORY + "camera_2/"
    CAMERA3_DOWNLOAD_PATH: str = CAPTURES_DIRECTORY + "camera_3/"

    # SCAN STATUS
    IS_SCANNING: bool = False
    IS_TESTING: bool = False
    IS_FILTERING: bool = False
    IS_SAVING: bool = False

    # GENERAL PORPOISE TEXTS
    NO_IMAGE: str = "Sin imagen"
    DEFAULT_HINT: str = "Vacío"

    # CAMERAS TEST CLASS
    RAW_EXTENSION: str = ".ARW"
    JPEG_EXTENSION: str = ".png"
    CURRENT_FILE_EXTENSION: str = ".png"
    ISO_CAMERA_CONFIG: str = "iso"
    SHUTTERSPEED_CAMERA_CONFIG: str = "shutterspeed"
    FORMAT_CAMERA_CONFIG: str = "imagequality"
    RESOLUTION_CAMERA_CONFIG: str = "imagesize"

    CAMERAS_DICT: dict[str, str] = gp.get_cameras()
    CAMERAS_LIST = (lambda keys: list(keys)[:3] + [None] * (3 - len(list(keys))))(CAMERAS_DICT.keys())
    DEFAULT_CAMERA_PORT: str = next(iter(CAMERAS_DICT.values()))
    ISOS_DICT: dict[str, str] = gp.get_config(camera_port=DEFAULT_CAMERA_PORT,camera_config=ISO_CAMERA_CONFIG)
    SHUTTERSPEEDS_DICT: dict[str, str] = gp.get_config(camera_port=DEFAULT_CAMERA_PORT,camera_config=SHUTTERSPEED_CAMERA_CONFIG)
    FORMATS_DICT: dict[str, str] = gp.get_config(camera_port=DEFAULT_CAMERA_PORT,camera_config=FORMAT_CAMERA_CONFIG)
    RESOLUTIONS_DICT: dict[str, str] = gp.get_config(camera_port=DEFAULT_CAMERA_PORT,camera_config=RESOLUTION_CAMERA_CONFIG)

    # ROUTINES
    FAILED_TO_APPLY_FILTER: bool = False
    FAILED_TO_SAVE_STAGE: bool = False
    FAILED_TO_APPLY_PRESET: bool = False
    FAILED_TO_SAVE_IMAGE: bool = False
    STAGES_NUMBER: int = 0
    CURRENT_ROUTINE: dict = {
        "name": None,
        "stages": []
    }
    APPEND_FILTER: bool = False
    PRODUCT_ID: str = ""
    LETTER_PREFIX: str = ""

    # FILTERS
    FILTER_RESOLUTION_OUTPUT: str = "480p"
    RM_BG_THRESHOLD: int = 120
    CROP_RESLUTIONS: dict[str, tuple[int, int]] = {
        "Small": (70, 57),
        "Medium": (400, 328),
        "Large": (1200, 984),
        "Model": (640, 640)
    }

    # SERVERS AND CREDENTIALS
    SELECTED_SERVER: str = ""
    SERVERS_DROPDOWN: Dropdown = None
    CREDENTIALS_DROPDOWN: Dropdown = None
    SELECTED_PATH: str = ""
    SELECTED_USER: str = ""
    SELECTED_PASSWORD: str = ""
    
    USE_SERVER: str = ""
    USE_IP: str = ""
    USE_PORT: str = ""
    USE_PATH: str = ""
    USE_USER: str = ""
    USE_PASSWORD: str = ""

    # MOTOR
    DIR_PIN: int = 10
    STEP_PIN: int = 8