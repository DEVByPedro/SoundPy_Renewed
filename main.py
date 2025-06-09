import setup.bin.InstallDependencies as insDep
import setup.bin.CreateJSONS as createJSONs
insDep.installDependencies()
createJSONs.createJsonSetup()

import configs.MusicConfig                    as musicConfig
import configs.UserConfig                      as userConfig
import configs.PlaylistConfig                 as playlistConfig
import infra.BodyContent                        as bodyContent
import infra.Home                                    as homePage
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

    playlists_buttons = []
    submenu = ft.Column(controls=playlists_buttons, opacity=1.0, animate_opacity=300)

    expanded = False

    playlist_modal = ft.AlertDialog(
        open=False,
        modal=True,
        title=ft.Text("Criar Playlist:"),
        content=ft.TextField(hint_text="Nome da Playlist", border_color=text_primary),
        bgcolor=card_color,
        actions=[
            ft.ElevatedButton(
                text="Criar",
                bgcolor=foreground_color,
                color="white",
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=2)),
                on_click=lambda e: [
                    playlistConfig.add_playlist(playlist_modal.content.value),
                    page.close(playlist_modal),
                    upgrade_playlist(),
                ],
            ),
            ft.ElevatedButton("Cancel",
                              color="white",
                              on_click=lambda e: page.close(playlist_modal),
                              style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=2))),
        ]
    )

    page.add(playlist_modal)

    criarPlaylistButton = ft.ElevatedButton(
        text="Criar Nova Playlist",
        bgcolor=card_color,
        color="white",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=2)),
        height=40,
        width=250,
        on_click=lambda e: page.open(playlist_modal)
    )

    def upgrade_playlist():
        playlists_buttons.clear()
        playlists_buttons.append(criarPlaylistButton)
        for playlist in range(len(playlistConfig.get_all_playlists())):
            button = ft.ElevatedButton(
                content=ft.Row([
                    ft.Icon(ft.Icons.MUSIC_NOTE_ROUNDED),
                    ft.Column([
                        ft.Text(value=playlistConfig.getPlaylistNameByIndex(playlist+1), size=12),
                        ft.Text("Duração: "+playlistConfig.getDuration(playlist+1), size=10, color="grey")
                    ]),
                ]),
                color="white",
                bgcolor=card_color,
                height=50,
                width=250,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=2)),
                on_click=lambda e, playlist_id=playlist+1: playlistConfig.getPlaylistMusicsById(e, playlist_id, body, page)
            )

            playlists_buttons.append(button)
        submenu.controls = playlists_buttons
        page.update()
    def toggle_sidebar(e):
        nonlocal  expanded
        if e.data == "true":
            sidebar.bgcolor=foreground_color
            for txt in text_refs:
                txt.opacity = 1
                txt.offset = ft.Offset(0, 0)
            for btn in buttons:
                btn.width = 180
            sidebar.width = 200
        else:
            expanded = False
            submenu.visible = False
            for btn in submenu.controls:
                btn.opacity = 0.0
            sidebar.bgcolor=foreground_color
            for btn in buttons:
                btn.width = 40
            for txt in text_refs:
                txt.opacity = 0
                txt.offset = ft.Offset(-0.3, 0)
            sidebar.width = 60
        page.update()
    def toggle_menu(e):
        nonlocal expanded
        expanded = not expanded

        if expanded:
            upgrade_playlist()
            submenu.visible = True
            submenu.opacity = 1.0
            submenu.animate_opacity = 300
            for btn in submenu.controls:
                btn.visible = True
                btn.opacity = 1.0
                btn.animate_opacity = 300
        else:
            submenu.opacity = 0.0
            submenu.animate_opacity = 300
            for btn in submenu.controls:
                btn.visible = False
                btn.opacity = 0.0
                btn.animate_opacity = 300

        page.update()
    def show_all_fav(e):
        print("Método ainda não construído")
    def show_mainMenu(e):
        body.content=homePage.body(page)
        page.update()
    def create_hover_handler(txt, icon):
            def handle_hover(e):
                txt.color = text_secondary if e.data == "true" else text_primary
                icon.color = text_secondary if e.data == "true" else text_primary
                txt.update()
                icon.update()

            return handle_hover
    def set_user_pfp():
        response = userConfig.get_user_pfp()
        if response != None:
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
        (ft.Text(value="Home", weight=700), ft.Icon(ft.Icons.HOME, size=20, color="white"), lambda e: show_mainMenu(e)),
        (ft.Text(value="Fav. Songs", weight=700), ft.Icon(ft.Icons.BOOKMARK_ADD_SHARP, size=20, color="white"), lambda e: show_all_fav(e)),
        (ft.Text(value="Playlists", weight=700), ft.Icon(ft.Icons.PLAYLIST_PLAY_SHARP, size=20, color="white"), lambda e: toggle_menu(e)),
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
    buttons.append(submenu)

    sidebar = ft.Container(
        content=ft.Column(buttons),
        bgcolor=foreground_color,
        width=60,
        alignment=ft.alignment.center_left,
        padding=ft.Padding(top=10, right=0, left=10, bottom=0),
        animate=ft.Animation(200, "easeInOut"),
        on_hover=toggle_sidebar,
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
                    content=ft.Row([ft.Text(f"Hello, {userConfig.getUserName()}!"), userProfileButton], width=300, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    mouse_cursor=ft.MouseCursor.BASIC,
                )
            ],

        )

    # Top Bar
    topContents = [
        ft.Text(width=80),
        ft.TextField(border_color="white", width=550, hint_text="Procurar Musicas"),
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
        margin=ft.Margin(left=-10, top=-10, bottom=0, right=0),
        content=ft.Container(homePage.body(page)),
        height=page.window.height - 10,
        padding=10,
        expand=True
    )

    layout = ft.Row([
        ft.Column([
            topbar,
            ft.Row([
                sidebar,
                body,
            ], expand=True),
        ], expand=True),
    ],expand=True)

    page.add(layout)

ft.app(target=main)
