import json
from sys import \
    hash_info

import setup.bin.InstallDependencies as installDependencies
import configs.MusicConfig                   as musicConfig
import os
import time
import configs.UserConfig                      as userConfig
import infra.BodyContent                       as bodyContent
import flet as ft

def main(page: ft.Page):
    page.padding = 0

    background_color = "#121212"
    card_color = "#1E1E1E"
    text_primary = "#FFFFFF"
    text_secondary = "#C7C7C7"
    button_hover = "#2C2C2C"
    border_color = "#404040"
    icon_color = "#E0E0E0"
    equalizer_bar = "#6C6C6C"
    foreground_color = "#141414"


    buttons = []
    text_refs = []

    def toggle_sidebar(e):
        if e.data == "true":
            sidebar.bgcolor=foreground_color
            for txt in text_refs:
                txt.opacity = 1
                txt.offset = ft.Offset(0, 0)
            for btn in buttons:
                btn.width = 180
            sidebar.width = 200
        else:
            sidebar.bgcolor=foreground_color
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
    def create_hover_handler(txt, icon):
            def handle_hover(e):
                txt.color = text_secondary if e.data == "true" else text_primary
                icon.color = text_secondary if e.data == "true" else text_primary
                txt.update()
                icon.update()

            return handle_hover
    def set_user_pfp():
        response = userConfig.get_user_pfp()
        if response != "":
            return ft.Image(src=response, width=50, height=50, border_radius=50, fit=ft.ImageFit.COVER)
        return ft.Icon(ft.Icons.PERSON_OUTLINE, color="white")
    def renew_user_pfp(e):
        if userConfig.find_pfp() == True:
            photoButton.src = userConfig.get_user_pfp()
            userProfile.content.src = userConfig.get_user_pfp()
            photoButton.update()
            userProfile.update()
    def change_opacity(e):
            changeButton.opacity = 0.7 if e.data == "true" else 0
            changeButton.update()

    menu_items = [
        (ft.Text(value=" - All Songs", weight=700), ft.Icon(ft.Icons.MY_LIBRARY_MUSIC, size=20, color="white"), lambda e: show_all_msc(e)),
        (ft.Text(value=" - Fav. Songs", weight=700), ft.Icon(ft.Icons.BOOKMARK_ADD_SHARP, size=20, color="white"), lambda e: show_all_fav(e)),
        (ft.Text(value=" - Playlists", weight=700), ft.Icon(ft.Icons.PLAYLIST_PLAY_SHARP, size=20, color="white"), lambda e: toggle_menu(e)),
    ]

    for label, icon, action in menu_items:
        text = ft.Text(
            value=label.value,
            size=15,
            weight=ft.FontWeight.W_400,
            color=text_primary,
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
                    bgcolor=card_color,
                    shape=ft.RoundedRectangleBorder(radius=5),
                    overlay_color=button_hover,
                ),
                width=40,
                height=40,
                animate_scale=200,
                on_click=action,
                on_hover=create_hover_handler(text, icon)
            )
        )

    sidebar = ft.Container(
        content=ft.Column(buttons),
        bgcolor=foreground_color,
        width=60,
        alignment=ft.alignment.center_left,
        padding=ft.Padding(top=10, right=0, left=10, bottom=0),
        animate=ft.Animation(200, "easeInOut"),
        on_hover=toggle_sidebar
    )

    changeButton = ft.ElevatedButton(content= ft.Icon(ft.Icons.EDIT, color="white"),
                                              width=50,
                                              height=50,
                                              style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=50)),
                                              opacity=0,
                                              on_click=renew_user_pfp,
                                              on_hover=change_opacity)
    photoButton = set_user_pfp()

    userProfileButton = ft.Stack(
                        controls=[
                            photoButton,
                            changeButton],
        width=50,
        height=50)

    userProfile = ft.PopupMenuButton(
            width=50,
            height=50,
            content=set_user_pfp(),
            items= [
                ft.PopupMenuItem(
                    content=ft.Row([ft.Text("Hello, User!"), userProfileButton], width=300, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    mouse_cursor=ft.MouseCursor.BASIC,
                )
            ],

        )

    # Top Bar
    topContents = [
        ft.Text("Welcome"),
        ft.TextField(border_color="white", width=550, hint_text="Search Musics"),
        userProfile
    ]

    topbar = ft.Container(
        content=ft.Row(topContents, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        bgcolor=foreground_color,
        height=70,
        alignment=ft.alignment.center,
        margin=ft.Margin(left=-10, top=0, bottom=0, right=0),
        padding=5,
        animate=ft.Animation(200, "easeInOut"),
    )

    # Body

    body = ft.Container(
        bgcolor=background_color,
        expand=True,
        margin=ft.Margin(left=-10, top=-10, bottom=0, right=0),
        content=bodyContent.contents(page),
        padding=10
    )

    layout = ft.Row([
        sidebar,
        ft.Column([
            topbar,
            body
        ],
        expand=True)],
    expand=True)

    page.add(layout)

ft.app(target=main)
