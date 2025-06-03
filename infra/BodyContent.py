import flet as ft
import configs.MusicConfig      as musicConfg
import os

background_color = "#121212"
card_color = "#1E1E1E"
text_primary = "#FFFFFF"
text_secondary = "#C7C7C7"
button_hover = "#2C2C2C"
border_color = "#404040"
icon_color = "#E0E0E0"
equalizer_bar = "#6C6C6C"
foreground_color = "#141414"

def change_hover(e):
    e.control.bgcolor = button_hover if e.data == "true" else foreground_color
    e.control.update()

def contents(page: ft.Page):

    carroselPlaylists = ft.Container(ft.Column([
        ft.Text("Suas Playlists:", size=34, weight=ft.FontWeight.W_500),
        ft.Row([
            ft.Container(bgcolor="red", width=100, height=100),
            ft.Container(bgcolor="red", width=100, height=100),
            ft.Container(bgcolor="red", width=100, height=100),
            ft.Container(bgcolor="red", width=100, height=100),
            ft.Container(bgcolor="red", width=100, height=100),
            ft.Container(bgcolor="red", width=100, height=100),
            ft.Container(bgcolor="red", width=100, height=100),
            ft.Container(bgcolor="red", width=100, height=100),
            ft.Container(bgcolor="red", width=100, height=100),
        ], scroll=ft.ScrollMode.ALWAYS)
    ]), padding=20,
        bgcolor=card_color,
        border_radius=10)

    allSongsContainer = ft.Column([
            ft.Row([
                ft.Text(value=os.path.basename(musicConfg.get_all_musics()))
            ], width=400, height=60)
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )

    allSongs = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text("Todas as Musicas:", size=34, weight=ft.FontWeight.W_500),
                ft.ElevatedButton(content=ft.Icon(ft.Icons.PLAY_ARROW,
                                                  color="white"),
                                  bgcolor="#121212",
                                  width=50,
                                  height=50)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Column([
                ft.Container(content=ft.Row([ft.Text("Nome"), ft.Text("Duração"), ft.Text("Total: "+musicConfg.getDuration("all"))], alignment=ft.MainAxisAlignment.SPACE_BETWEEN), padding=10, bgcolor=background_color)
            ]),
            allSongsContainer
        ]),padding=20,
        margin=ft.Margin(top=20,left=0,right=0,bottom=0),
        width=(page.width - ((40/100) * page.width)),
        bgcolor=card_color,
        border_radius=10,
        expand=True,
    )

    all = ft.Container(content=ft.Column([
        carroselPlaylists,
        allSongs
    ]), bgcolor=background_color,
        border_radius=10,
    width=page.width - ((40/100) * page.width),
    expand=True)

    return all