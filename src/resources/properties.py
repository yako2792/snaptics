"""
This module contains configurable properties for the Fleet-based web application.
It centralizes settings, ensuring easy configuration and avoiding hardcoding values in the codebase.
"""

class Properties:
    # GENERAL PAGE
    PAGE_TITLE: str = "Snaptics"
    PAGE_PADDING: int = 10
    PAGE_BGCOLOR: str = "#2C323D"
    CONTAINER_BGCOLOR: str = "#2E3541"
    ANIMATIONS_DURATION: int = 0
    MIN_WINDOW_SIZE: tuple[int,int] = (1280,720)

    # FRAMES
    EXPLORER_SIZE: float = 0.3
    FRAME_PADDING: int = 3


    # TABS
    PREVIEW_TAB_TITLE: str = "Preview"
    SCAN_TAB_TITLE: str = "Scan"
    SAVE_TAB_TITLE: str = "Save"
    PROPERTIES_TAB_TITLE: str = "Properties"

    TAB_ICON_SIZE: int = 18
    TAB_ICON_ENABLED: bool = True
    TAB_PADDING: int = 15

    # CONTROLS STYLE
    CHECKBOX_WIDTH: int = 350
    CHECKBOX_HEIGHT: int = 49
    DROPDOWN_WIDTH: int = 350
    BUTTON_WIDTH: int = 100
    BUTTON_HEIGHT: int = 49
    BORDER_RADIUS: int = 0

    # GENERAL PORPOISE TEXTS
    NO_IMAGE: str = "No image"