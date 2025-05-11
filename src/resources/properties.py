"""
This module contains configurable properties for the Fleet-based web application.
It centralizes settings, ensuring easy configuration and avoiding hardcoding values in the codebase.
"""

import os
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

    # FRAMES
    EXPLORER_SIZE: float = 0.3
    FRAME_PADDING: int = 3

    # TABS
    PREVIEW_TAB_TITLE: str = "Preview"
    SCAN_TAB_TITLE: str = "Scan"
    PREVIEW_KEY: str = "Preview"
    SCAN_KEY: str = "Scan"
    EXPLORER_KEY: str = "Explorer"
    PROPERTIES_TAB_TITLE: str = "Properties"

    TAB_ICON_SIZE: int = 18
    TAB_ICON_ENABLED: bool = True
    TAB_PADDING: int = 15

    # CONTROLS STYLE
    IMAGE_VIEW_WIDTH: int = 640
    IMAGE_VIEW_HEIGHT: int = 360
    CHECKBOX_WIDTH: int = 350
    CHECKBOX_HEIGHT: int = 49
    DROPDOWN_WIDTH: int = 350
    BUTTON_WIDTH: int = 100
    BUTTON_HEIGHT: int = 49
    BORDER_RADIUS: int = 0

    # PROPERTIES TAB
    EXPLORER_SETTINGS_TITLE: str = "Properties: Explorer"
    EXPLORER_SETTINGS_SUBTITLE: str = "Customize some values from the Explorer frame."
    SCAN_SETTINGS_TITLE: str = "Properties: Scan Tab"
    SCAN_SETTINGS_SUBTITLE: str = "Customize some values from the Scan tab."
    CAMERA_SETTINGS_TITLE: str = "Properties: Cameras"
    CAMERA_SETTINGS_SUBTITLE: str = "Customize some camera properties."
    INITIALLY_EXPANDED_PROPERTIES: bool = True

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

    # SCAN STATUS
    IS_SCANNING: bool = False
    IS_TESTING: bool = False

    # GENERAL PORPOISE TEXTS
    NO_IMAGE: str = "No image"
    DEFAULT_HINT: str = "Empty"

    # CAMERAS TEST CLASS
    RAW_EXTENSION: str = ".ARW"
    JPEG_EXTENSION: str = ".jpg"
    ISO_CAMERA_CONFIG: str = "iso"
    SHUTTERSPEED_CAMERA_CONFIG: str = "shutterspeed"
    FORMAT_CAMERA_CONFIG: str = "imagequality"
    RESOLUTION_CAMERA_CONFIG: str = "imagesize"

    CAMERAS_DICT: dict[str, str] = gp.get_cameras()
    CAMERAS_LIST: list[str] = list(CAMERAS_DICT.keys())
    DEFAULT_CAMERA_PORT: str = next(iter(CAMERAS_DICT.values()))
    ISOS_DICT: dict[str, str] = gp.get_config(camera_port=DEFAULT_CAMERA_PORT,camera_config=ISO_CAMERA_CONFIG)
    SHUTTERSPEEDS_DICT: dict[str, str] = gp.get_config(camera_port=DEFAULT_CAMERA_PORT,camera_config=SHUTTERSPEED_CAMERA_CONFIG)
    FORMATS_DICT: dict[str, str] = gp.get_config(camera_port=DEFAULT_CAMERA_PORT,camera_config=FORMAT_CAMERA_CONFIG)
    RESOLUTIONS_DICT: dict[str, str] = gp.get_config(camera_port=DEFAULT_CAMERA_PORT,camera_config=RESOLUTION_CAMERA_CONFIG)