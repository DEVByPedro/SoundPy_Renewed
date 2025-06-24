import flet as ft

import configs.Colors as colors

def body(page: ft.Page):

    return ft.Container(
            content=ft.Text("Home ainda não implementado.", color=colors.text_secondary, size=20),
            alignment=ft.alignment.center,
            expand=True,
            bgcolor=colors.background_color
        )
