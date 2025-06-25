import os.path
import flet as ft
import tkinter as tk
from tkinter import filedialog

import pygame

import configs.Colors as colors
import configs.MusicConfig as musicConfig
import configs.PlaylistConfig as playlistConfig
import sysConf.Downloader as downloader

import configs.Core as music

def change_hover(e):
    e.control.bgcolor = colors.button_hover if e.data == "true" else colors.foreground_color
    e.control.update()

def AllPlaylistSongs(page: ft.Page, id):
    ytLink = ft.TextField()

    imagePlaylist = ft.Image(src=musicConfig.getPathByIndex(0).replace(".mp3", ".jpg"), width=100, height=100, fit=ft.ImageFit.COVER)

    def deletePlaylist(e, playlist_id):
        playlistConfig.remove_playlist_by_name(playlistConfig.getPlaylistNameByIndex(playlist_id))
        page.close(modal_confirm)

    def downloadMusic(e, link, id):
        page.close(modal)
        if downloader.download_mp3(e, ytLink.value, id) == True:
            allSongsContainer.controls.clear()
            insert_all_songs(limit[0])
            page.update()

    modal_confirm = ft.AlertDialog(
        modal=True,
        open=False,
        title=ft.Text("Confirmar Exclusão:"),
        content=ft.Text("Você tem certeza que deseja excluir esta playlist?"),
        actions=[
            ft.ElevatedButton(
                text="Excluir",
                on_click=lambda e: deletePlaylist(e, id),
                bgcolor="red",
                color="white",
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=6),
                ),
            ),
            ft.ElevatedButton(
                text="Cancelar",
                on_click=lambda e: page.close(modal_confirm),
                bgcolor=colors.foreground_color,
                color="white",
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=6),
                )
            )
        ]
    )

    modal = ft.AlertDialog(
        modal=True,
        open=False,
        title=ft.Text("Cole o link do YouTube:"),
        content=ytLink,
        actions=[
            ft.ElevatedButton(
                text="Ok",
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=6),
                    padding=ft.Padding(top=0, right=10, left=10, bottom=0),
                    bgcolor="white",
                    color="black"
                ),
                on_click=lambda e: downloadMusic(e, ytLink.value, id)
            ),
            ft.ElevatedButton(
                text="Cancelar",
                on_click=lambda e: page.close(modal)
            )
        ]
    )
    page.overlay.append(modal)
    page.overlay.append(modal_confirm)

    allCheckedSongs = []
    music_checkboxes = []
    limit = [40]
    current_playing_path = [None]

    def getMusicName(path: str):
        count = path.count("-")
        while count > 0:
            indexOfTrace = path.index("-")
            path = path[indexOfTrace + 2:]
            count -= 1
        return path
    def add_msc(e):
        try:
            tki = tk.Tk()
            tki.withdraw()
            tki.attributes("-topmost", True)
            file_path = filedialog.askopenfiles(title="Selecione músicas", filetypes=[("MP3 Files", ".mp3")])
            for file in file_path:
                if not playlistConfig.containsMusic(id, file.name):
                    playlistConfig.addMusic(id, file.name)
            allSongsContainer.controls.clear()
            insert_all_songs(limit[0])

            page.update()
        except Exception as ex:
            return
    def change_checkBox_visibility(e):
        checkBox.visible = not checkBox.visible
        confirmButton.visible = not confirmButton.visible
        checkBox.value = False
        for cb in music_checkboxes:
            cb.visible = not cb.visible
        page.update()
    def changeAllCheckBox(e):
        for cb in music_checkboxes:
            cb.value = True if e.data == 'true' else False
            if e.data == 'true':
                for path in playlistConfig.get_all_playlist_musics(id, "all"):
                    if path not in allCheckedSongs:
                        allCheckedSongs.append(path)
        if e.data == 'false':
            allCheckedSongs.clear()
        page.update()
    def excludeSongs(e):

        if allCheckedSongs:
            for path in allCheckedSongs:
                playlistConfig.deleteByIndex(id, playlistConfig.getIndexByPath(id, path))
                musicConfig.deleteByIndex(musicConfig.getIndexByPath(path))
        checkBox.visible = False
        confirmButton.visible = False
        for cb in music_checkboxes:
            cb.visible = False
            cb.value = False
        allSongsContainer.controls.clear()
        insert_all_songs(limit[0])

        musicConfig.stopSong()

        page.update()
    def getArtist(name):
        return name.split("-")[0] if "-" in name else "Unknown Artist"
    def insert_all_songs(limit):
        allPaths = playlistConfig.get_all_playlist_musics(id, limit)

        imagePlaylist.src = get_first_music_image(id)

        for idx, path in enumerate(allPaths) :
            nowId = playlistConfig.getIndexByPath(id, path)
            basename = os.path.basename(path)
            name = basename.replace(".mp3", "")

            music_checkbox = ft.Checkbox(
                visible=False,
                width=20,
                height=20,
                on_change=lambda e, p=path: (
                    allCheckedSongs.append(p) if e.data == 'true' and p not in allCheckedSongs else
                    allCheckedSongs.remove(p) if e.data == 'false' and p in allCheckedSongs else None
                )
            )
            music_checkboxes.append(music_checkbox)

            playlistImage = ft.Image(src=path.replace(".mp3", ".jpg"), width=50, height=50, fit=ft.ImageFit.COVER)

            allSongsContainer.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Row([
                            music_checkbox,
                            ft.ElevatedButton(
                                width=30,
                                content=ft.Icon(ft.Icons.PLAY_ARROW, color="white", size=20),
                                style=ft.ButtonStyle(
                                    bgcolor="transparent",
                                    overlay_color="transparent",
                                    elevation=0,
                                    padding=ft.Padding(top=0, left=0, right=5, bottom=0)
                                ),
                                on_click=lambda e, p=path: changeAndPlayMusic(e, p, e.control),
                            ),
                            playlistImage,
                            ft.Column([
                                ft.Text(str(nowId+1) + ". " + getMusicName(name), weight=ft.FontWeight.W_700),
                                ft.Text("by " + getArtist(name))
                            ])
                        ], width=400),
                        ft.Container(
                            ft.Column([ft.Row([ft.Text(musicConfig.getIndividualDuration(path)),],
                                        width=400, alignment=ft.MainAxisAlignment.SPACE_BETWEEN)]),
                            padding=ft.Padding(top=5, right=0, left=0, bottom=0))
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    on_hover=change_hover,
                    bgcolor=colors.foreground_color,
                    height=70,
                    padding=10,
                    border_radius=5,
                    animate=ft.Animation(100, "easeIn"),
                )
            )
    def get_first_music_image(playlist_id):
        musics = playlistConfig.get_all_playlist_musics(playlist_id, limit=1)
        if musics:
            return musics[0].replace(".mp3", ".jpg")
        return "nothing/found"
    def on_save_click(e):
        playlistConfig.editPlaylistName(id, nameTxtField.value)
        currentPlaylistTitle.value = nameTxtField.value + ":"
        currentPlaylistTitle.update()
        page.update()
        page.close(modal_change_playlist_name)
    def changeAndPlayMusic(e, path, button):
        if current_playing_path[0] == path:
            music.setArtist("Nome Desconhecido")
            return
        current_playing_path[0] = path
        musicConfig.playMusic(e, path)
        update_play_icons()

        allSongs.update()
        page.update()
    def update_play_icons():
        for idx, cb in enumerate(music_checkboxes):
            container = allSongsContainer.controls[idx]
            play_button = container.content.controls[0].controls[1]
            duration_text = container.content.controls[1].content.controls[0].controls[0]
            music_name = container.content.controls[0].controls[3].controls[0]
            music_artist = container.content.controls[0].controls[3].controls[1]
            path_btn = playlistConfig.get_all_playlist_musics(id, limit[0])[idx]
            if path_btn == current_playing_path[0]:
                play_button.content = ft.Icon(ft.Icons.PLAY_ARROW, color=colors.current_music_color, size=20)
                music_name.color = colors.current_music_color
                music_artist.color = colors.current_music_color
                duration_text.color = colors.current_music_color
            else:
                play_button.content = ft.Icon(ft.Icons.PLAY_ARROW, color="white", size=20)
                music_name.color = "white"
                music_artist.color = "white"
                duration_text.color = "white"
            play_button.update()
            page.update()
    def check_checkboxes(e):
        if (checkBox.visible == True and confirmButton.visible == True):
            checkBox.visible = False
            confirmButton.visible = False
            for box in music_checkboxes:
                box.visible = False
        page.update()

    allSongsContainer = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    checkBox = ft.Checkbox(
        value=True,
        width=20,
        height=20,
        visible=False,
        on_change=changeAllCheckBox
    )

    confirmButton = ft.ElevatedButton(
        content=ft.Icon(ft.Icons.DELETE, color="white"),
        bgcolor="red",
        width=20,
        height=20,
        visible=False,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=2), padding=ft.Padding(top=0, right=3, left=0, bottom=0)),
        on_click=excludeSongs,
    )

    insert_all_songs(limit[0])

    currentPlaylistTitle = ft.Text(playlistConfig.getPlaylistNameByIndex(id) + ":", size=34, weight=ft.FontWeight.W_500)
    durTot                       = ft.Text("Duração: " + playlistConfig.getDuration(id))
    nameTxtField           = ft.TextField(value=playlistConfig.getPlaylistNameByIndex(id), color="white", border_color="white", on_submit=on_save_click)

    modal_change_playlist_name = ft.AlertDialog(
        modal=True,
        open=False,
        title=ft.Text("Editar Nome da Playlist:"),
        content=nameTxtField,
        actions = [
            ft.ElevatedButton(
                text="Salvar",
                bgcolor=colors.background_color,
                color="white",
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=6),
                ),
                on_click=on_save_click
            ),
            ft.ElevatedButton(
                text="Cancelar",
                bgcolor=colors.foreground_color,
                color="white",
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=6),
                ),
                on_click=lambda e: page.close(modal_change_playlist_name)
            ),
        ])

    configPlaylistButton = ft.PopupMenuButton(
        content=ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.EXPAND_MORE_OUTLINED, color="white", size=20)
            ]),
            bgcolor=colors.background_color,
            border_radius=3,
            padding=5
        ),
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=3)),
        width=30,
        height=30,
        on_open=check_checkboxes,
        items=[
            ft.PopupMenuItem(
                content=ft.Row([
                    ft.Icon(ft.Icons.EDIT, color="white"),
                    ft.Text("Editar Nome Playlist")]),

                on_click=lambda e: page.open(modal_change_playlist_name),
            ),
            ft.PopupMenuItem(
                content=ft.Row([ft.Icon(ft.Icons.ADD, color="white"), ft.Text("Adicionar Música", color="white")]),
                on_click=add_msc
            ),
            ft.PopupMenuItem(
                content=ft.Row([
                    ft.Icon(ft.Icons.DOWNLOAD, color='white'),
                    ft.Text("Baixar Músicas")
                ]),
                on_click=lambda e: page.open(modal)
            ),
            ft.PopupMenuItem(
                content=ft.Row([
                    ft.Icon(ft.Icons.FOLDER_DELETE, color='white'),
                    ft.Text("Excluir Playlist")
                ]),
                on_click=lambda e: page.open(modal_confirm)
            ),
            ft.PopupMenuItem(
                content=ft.Row([ft.Icon(ft.Icons.DELETE, color="white"), ft.Text("Deletar Músicas", color="white")]),
                on_click=change_checkBox_visibility
            )
        ],
    )
    bottomBar = ft.Container(
                content=ft.Row([
                    ft.Text("Limite:", size=17),
                    ft.TextField(
                        value=limit[0],
                        width=50,
                        height=30,
                        content_padding=0,
                        text_align=ft.TextAlign.CENTER,
                        color="white",
                        border_color="white",
                        on_submit=lambda e: {
                            limit.pop(0),
                            limit.append(e.control.value),
                            allSongsContainer.controls.clear(),
                            insert_all_songs(limit[0]), allSongs.update()
                        }
                    ),
                ], alignment=ft.MainAxisAlignment.CENTER),
                bgcolor=colors.background_color,
                padding=5,
            )
    allSongs = ft.Container(
        content=ft.Column([
            ft.Container(
                height=int(30/100 * page.height),
                expand=True,
                margin=ft.Margin(bottom=10, left=0, right=0, top=0),
            ),
            ft.Row([
                ft.Row([
                    ft.Container(content=imagePlaylist),
                    ft.Column([
                        currentPlaylistTitle,
                        durTot,
                    ]),
                ]),
                ft.Row([
                    ft.ElevatedButton(
                        content=ft.Icon(ft.Icons.PLAY_ARROW, color="black", size=25),
                        bgcolor="#27e91d",
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=50)),
                        width=50,
                        height=50,
                    ),
                    configPlaylistButton,
                ]),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(
                content=ft.Row([
                    ft.Row([
                        ft.Row([checkBox, confirmButton]),
                        ft.Text("Nome", width=200, text_align=ft.TextAlign.CENTER)
                    ], width=250,
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    ft.Text("Duração", text_align=ft.TextAlign.CENTER),
                    ft.Text("")
                ],  alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=ft.Padding(top=10, left=0, bottom=0, right=-100),
                    bgcolor=colors.background_color,
                    margin=ft.Margin(top=20, left=0, right=0, bottom=0)
            ),
            ft.Container(
                ft.Column([
                    allSongsContainer,
                    bottomBar
                ],
                    height=int(57/100 * page.height),
                    scroll=ft.ScrollMode.AUTO,
                ),
                padding=ft.Padding(top=0, left=10, right=0, bottom=0),
                bgcolor=colors.card_color,
                border_radius=20,

            )
        ], expand=True,
            scroll=ft.ScrollMode.AUTO,
        ),
        padding=20,
        margin=ft.Margin(top=0, left=10, right=0, bottom=0),
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.center,
            colors=[playlistConfig.getPhotoImage(playlistConfig.getMusicByIndex(id, 0)), colors.card_color],
        ),
        border_radius=10,
        animate=ft.Animation(150, "ease-in"),
        expand=True,
    )


    return allSongs