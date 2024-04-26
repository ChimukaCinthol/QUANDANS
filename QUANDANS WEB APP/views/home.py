
import flet as ft

def home_page(page: ft.Page,token):

    home_aside_component = ft.Row(
        controls=[
            ft.Text(value="Ths is the home page")
        ]
    )
    home_aside_component_container = ft.Container(
        width=500,
        height=500,
        bgcolor=ft.colors.TEAL,
        border_radius=10,
        content=ft.Stack(
            controls=[home_aside_component]
        )
    )

    return home_aside_component_container

