import flet as ft
from src.resources.properties import *
from src.resources.utils.layout import Layout

def main(page: ft.Page) -> None:

        # PAGE: Properties
        page.title = PAGE_TITLE
        page.padding = PAGE_PADDING
        page.bgcolor = PAGE_BGCOLOR

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