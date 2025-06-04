import os.path
from ctypes import \
    windll

import flet as ft
import tkinter as tk
from tkinter import filedialog

import configs.MusicConfig      as musicConfig

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

    def add_msc(e):
        tki = tk.Tk()
        tki.withdraw()
        tki.attributes("-topmost", True)

        file_path = filedialog.askopenfiles(title="Select a music", filetypes=[("MP3 Files", ".mp3")])
        for file in file_path:
            musicConfig.addMusic(file.name)

        allSongsContainer.controls.clear()
        insert_all_songs()

        durTot.value = "Duração Total: "+musicConfig.getDuration()

        durTot.update()
        page.update()

    allSongsContainer = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )

    def insert_all_songs():

        allPaths = musicConfig.get_all_musics()
        for path in allPaths:

            # Trimming path for visibility
            basename = os.path.basename(path)
            name = basename

            if os.path.basename(path).count("-") > 1:
                name = basename.replace(basename[0:basename.index("-") + 2], "", 1)
            if os.path.basename(path).count("(") == 1:
                name = basename.replace(basename[basename.index("("):basename.index(")") + 1], "")
            updatedPath = path.replace(basename, name)

            allSongsContainer.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Row([
                            ft.Image(src=path.replace(".mp3", ".jpg"), width=50, height=50, fit=ft.ImageFit.COVER),
                            ft.Column([
                                ft.Text(name.replace(" .mp3", "")[:40]),
                                 ft.Text("by "+name[:name.index(" -")])], width=300),]),
                        # Duração Musica
                        ft.Text(musicConfig.getIndividualDuration(path)),
                        ft.ElevatedButton(content=ft.Icon(ft.Icons.PLAY_ARROW, color='white'), bgcolor="#0D0D0D", width=40, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=4), padding=10))],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    on_hover=change_hover,
                    bgcolor=foreground_color,
                    height=70,
                    padding=10,
                    border_radius=5
                )
            )

    insert_all_songs()

    ft.Container(
        content=allSongsContainer,
        padding=10,
    )

    durTot = ft.Text("Duração Total: "+ musicConfig.getDuration())

    allSongs = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Column([
                    ft.Text("Todas as Musicas:", size=34, weight=ft.FontWeight.W_500),
                    durTot,
                ]),

                ft.Row([
                    ft.ElevatedButton(
                        content=ft.Row([ft.Icon(ft.Icons.DOWNLOAD, color="white")]),
                        bgcolor=background_color,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=3), padding=10),
                        width=40
                    ),
                    ft.ElevatedButton(
                        content=ft.Row([ft.Icon(ft.Icons.ADD, color="white"), ft.Text("Add Music!", color="white")]),
                        bgcolor=background_color,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=3), padding=10),
                        on_click=add_msc
                    )
                ]),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Column([
                ft.Container(content=ft.Row([
                    ft.Row([
                        ft.Text("Nome")],
                        width=250),
                    ft.Text("Duração"),
                    ft.Text("")],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=ft.Padding(top=10,left=130,bottom=10,right=80),
                    bgcolor=background_color,
                    margin=ft.Margin(top=20, left=0, right=0, bottom=0))
            ]),
             allSongsContainer
        ]),padding=20,
        margin=ft.Margin(top=20,left=0,right=0,bottom=0),
        bgcolor=card_color,
        border_radius=10,
        expand=True,
    )

    all = ft.Container(content=ft.Column([
        allSongs
    ]), bgcolor=background_color,
        border_radius=10,
    expand=True)

    page.update()

    return all