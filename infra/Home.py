import flet as ft

background_color = "#121212"
card_color = "#1E1E1E"
text_primary = "#FFFFFF"
text_secondary = "#C7C7C7"
button_hover = "#2C2C2C"
border_color = "#404040"
icon_color = "#E0E0E0"
equalizer_bar = "#6C6C6C"
foreground_color = "#141414"

def body(page: ft.Page):

    return ft.Container(
            content=ft.Text("Home ainda não implementado.", color=text_secondary, size=20),
            alignment=ft.alignment.center,
            expand=True,
            bgcolor=background_color
        )
