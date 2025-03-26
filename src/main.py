import flet as ft

def main(page: ft.Page):
        page.add(ft.Text(value="Hello World"))
        page.update()

if __name__=="__main__":
    ft.app(main)