import json

import Lib.setup.bin.InstallDependencies as installDependencies
import Lib.configs.MusicConfig                   as musicConfig
import os

import flet as ft

def main(page: ft.Page):
    page.padding = 0

    buttons = []
    text_refs = []
    playlist_btn = []
    def toggle_sidebar(e):
        if e.data == "true":
            for txt in text_refs:
                txt.opacity = 1
                txt.offset = ft.Offset(0, 0)
            for btn in buttons:
                btn.width = 180
            sidebar.width = 200
        else:
            for btn in buttons:
                btn.width = 40
            for txt in text_refs:
                txt.opacity = 0
                txt.offset = ft.Offset(-0.3, 0)
            sidebar.width = 60
        page.update()
    def toggle_menu(e):
        print("Método ainda não construído")
    def show_all_fav(e):
        print("Método ainda não construído")
    def show_all_msc(e):
        print("Método ainda não construído")

    menu_items = [
        (" - All Songs", ft.Icon(ft.Icons.MY_LIBRARY_MUSIC, size=20, color="white"), lambda e: show_all_msc(e)),
        (" - Fav. Songs", ft.Icon(ft.Icons.BOOKMARK_ADD_SHARP, size=20, color="white"), lambda e: show_all_fav(e)),
        (" - Playlists", ft.Icon(ft.Icons.PLAYLIST_PLAY_SHARP, size=20, color="white"), lambda e: toggle_menu(e)),
    ]

    for label, icon, action in menu_items:
        text = ft.Text(
            value=label,
            size=15,
            weight=ft.FontWeight.W_400,
            color="white",
            opacity=0,
            offset=ft.Offset(-0.3, 0),
            animate_opacity=100,
            animate_offset=200,
        )
        text_refs.append(text)

        buttons.append(
            ft.ElevatedButton(
                content=ft.Container(
                    content=ft.Row(
                        [icon,
                         text,]
                    ),
                    alignment=ft.alignment.center_left,
                    expand=True,
                ),
                style=ft.ButtonStyle(
                    bgcolor="#1a1a1a",
                    shape=ft.RoundedRectangleBorder(radius=5),
                    overlay_color="#2c2c2c",
                    color="white",
                ),
                width=40,
                height=40,
                animate_scale=200,
                on_click=action,
            )
        )

    sidebar = ft.Container(
        content=ft.Column(buttons),
        bgcolor="#0a0a0a",
        width=60,
        alignment=ft.alignment.center_left,
        padding=ft.Padding(
            top=10,
            right=0,
            left=10,
            bottom=0),
        animate=ft.Animation(200, "easeInOut"),
        on_hover=toggle_sidebar
    )

    topbar = ft.Container(
        content=ft.Row(topContents),
        bgcolor="#0a0a0a",
        width=60,
        alignment=ft.alignment.center_left,
        padding=ft.Padding(
            top=10,
            right=0,
            left=10,
            bottom=0),
        animate=ft.Animation(200, "easeInOut"),
        on_hover=toggle_sidebar
    )

    layout = ft.Row([
        sidebar
    ], expand=True)

    page.add(layout)

ft.app(target=main)
