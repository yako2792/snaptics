import flet as ft
from src.resources.properties import Properties as Props
from src.resources.utils.layout import Layout

def main(page: ft.Page) -> None:

        # PAGE: Properties
        page.title = Props.PAGE_TITLE
        page.padding = Props.PAGE_PADDING
        page.bgcolor = Props.PAGE_BGCOLOR
        page.window.width = Props.MIN_WINDOW_SIZE[0]
        page.window.height = Props.MIN_WINDOW_SIZE[1]
        page.window.min_width = Props.MIN_WINDOW_SIZE[0]
        page.window.min_height = Props.MIN_WINDOW_SIZE[1]

        # PAGE: Application
        app: ft.Control = Layout(page)

        # PAGE: Add
        page.add(app)
        page.update()

if __name__=="__main__":
    ft.app(
            target=main,
            view=ft.WEB_BROWSER
    )