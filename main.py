from pygame.sprite import \
    collide_circle_ratio

import setup.bin.InstallDependencies as insDep
import setup.bin.CreateJSONS as createJSONs
insDep.installDependencies()
createJSONs.createJsonSetup()

import configs.UserConfig as userConfig
import configs.PlaylistConfig as playlistConfig
import infra.Home as homePage
import infra.BodyContent as bodyContent
import flet as ft

def main(page: ft.Page):
    page.padding = 0
    page.bgcolor = "#121212"

    # Cores
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

    # Modal para criar playlist
    playlist_modal = ft.AlertDialog(
        open=False,
        modal=True,
        title=ft.Text("Criar Playlist:"),
        content=ft.TextField(hint_text="Nome da Playlist",
                             border_color=text_primary,
                             on_submit=lambda e: [
                                playlistConfig.add_playlist(playlist_modal.content.value),
                                page.close(playlist_modal),
                                upgrade_playlist()]
                             ),
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
            ft.ElevatedButton(
                "Cancelar",
                color="white",
                on_click=lambda e: page.close(playlist_modal),
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=2)),
            ),
        ]
    )
    page.overlay.append(playlist_modal)

    criarPlaylistButton = ft.ElevatedButton(
        text="Criar Nova Playlist",
        bgcolor=card_color,
        color="white",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=2)),
        height=40,
        width=250,
        on_click=lambda e: page.open(playlist_modal)
    )

    # Body central
    body_column = ft.Column([], expand=True)
    body = ft.Container(
        bgcolor=background_color,
        content=body_column,
        padding=10,
        margin=ft.Margin(top=-10, bottom=0, left=-10, right=0),
        expand=True,
        alignment=ft.alignment.top_left,
    )

    def upgrade_playlist():
        playlists_buttons.clear()
        criarPlaylistButton.visible = True
        criarPlaylistButton.opacity = 1.0
        playlists_buttons.append(criarPlaylistButton)
        for idx, playlist in enumerate(playlistConfig.get_all_playlists()):
            button = ft.ElevatedButton(
                content=ft.Row([
                    ft.Icon(ft.Icons.MUSIC_NOTE_ROUNDED),
                    ft.Column([
                        ft.Text(value=playlist[1], size=12),
                        ft.Text("Duração: " + playlistConfig.getDuration(playlist[0]), size=10, color="grey")
                    ], height=40),
                ]),
                color="white",
                bgcolor=card_color,
                height=50,
                width=250,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=2)),
                on_click=lambda e, playlist_id=playlist[0]: playlistConfig.getPlaylistMusicsById(e, playlist_id, body, page)
            )
            playlists_buttons.append(button)
        criarPlaylistButton.visible = True
        submenu.controls = playlists_buttons
        page.update()
    def toggle_sidebar(e):
        nonlocal expanded
        if e.data == "true":
            sidebar.bgcolor = foreground_color
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
            sidebar.bgcolor = foreground_color
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
            criarPlaylistButton.visible = True
            for btn in submenu.controls:
                btn.visible = True
            submenu.opacity = 1.0
        else:
            submenu.opacity = 0.0
            for btn in submenu.controls:
                btn.visible = False
                btn.opacity = 0.0
        page.update()
    def show_all_fav(e):
        body_column.controls.clear()
        body_column.controls.append(ft.Container(
            content=ft.Text("Favoritos ainda não implementado.", color=text_secondary, size=20),
            alignment=ft.alignment.center,
            expand=True,
            bgcolor=background_color
        ))
        body_column.update()
        page.update()
    def create_hover_handler(txt, icon):
        def handle_hover(e):
            txt.color = text_secondary if e.data == "true" else text_primary
            icon.color = text_secondary if e.data == "true" else text_primary
            txt.update()
            icon.update()
        return handle_hover
    def show_all_msc(e):
        body_column.controls.clear()
        body_column.controls.append(bodyContent.AllSongs(page))
        body_column.update()
        page.update()
    def show_mainMenu(e):
        body_column.controls.clear()
        body_column.controls.append(homePage.body(page))
        body_column.update()
        page.update()
    def set_user_pfp():
        response = userConfig.get_user_pfp()
        if response:
            return ft.Image(src=response, width=50, height=50, border_radius=50, fit=ft.ImageFit.COVER)
        return ft.Icon(ft.Icons.PERSON_OUTLINE, color="white")
    def renew_user_pfp(e):
        if userConfig.find_pfp():
            new_image = set_user_pfp()
            userProfile.content = new_image

            new_userProfileButton = ft.Stack([new_image, changeButton], width=50, height=50)

            userProfile.items[0].content.controls[1] = new_userProfileButton

            page.update()
    def change_opacity(e):
        changeButton.opacity = 0.7 if e.data == "true" else 0
        changeButton.update()

    menu_items = [
        ("Home", ft.Icons.HOME, show_mainMenu),
        ("Fav. Songs", ft.Icons.BOOKMARK_ADD_SHARP, show_all_fav),
        ("Playlists", ft.Icons.PLAYLIST_PLAY_SHARP, toggle_menu),
    ]

    for label, icon_name, action in menu_items:
        text = ft.Text(
            value=label,
            size=15,
            weight=ft.FontWeight.W_400,
            color=text_primary,
            opacity=0,
            offset=ft.Offset(-0.3, 0),
            animate_opacity=100,
            animate_offset=200,
        )
        text_refs.append(text)

        icon = ft.Icon(icon_name, size=20, color="white")

        buttons.append(
            ft.ElevatedButton(
                content=ft.Container(
                    content=ft.Row([icon, text]),
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
                on_hover=create_hover_handler(text, icon),
            )
        )
    buttons.append(submenu)

    sidebar = ft.Container(
        content=ft.Column(buttons, scroll="auto", expand=True),
        bgcolor=foreground_color,
        width=60,
        alignment=ft.alignment.top_left,
        padding=ft.Padding(top=10, right=5, left=10, bottom=10),
        animate=ft.Animation(200, "easeInOut"),
        margin=ft.Margin(top=-10, bottom=0, left=0, right=0),
        on_hover=toggle_sidebar,
        expand=False
    )

    changeButton = ft.ElevatedButton(
        content=ft.Icon(ft.Icons.EDIT, color="white"),
        width=50,
        height=50,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=50)),
        opacity=0,
        on_click=renew_user_pfp,
        on_hover=change_opacity,
    )
    photoButton = set_user_pfp()

    userProfileButton = ft.Stack([
        photoButton,
        changeButton
    ], width=50, height=50)

    userProfile = ft.PopupMenuButton(
        width=50,
        height=50,
        content=set_user_pfp(),
        items=[
            ft.PopupMenuItem(
                content=ft.Row([
                    ft.Text(f"Olá, {userConfig.getUserName()}!"),
                    userProfileButton
                ], width=300, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                mouse_cursor=ft.MouseCursor.BASIC,
            )
        ],
    )

    # Top Bar
    topbar = ft.Container(
        content=ft.Row([
            ft.Text(width=80),
            ft.TextField(
                border_color=text_secondary,
                width=550,
                hint_text="Procurar Músicas",
                prefix_icon=ft.Icon(ft.Icons.SEARCH_OUTLINED, color=text_secondary, size=18),
                border_radius=25
            ),
            userProfile,
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        bgcolor=foreground_color,
        height=70,
        padding=10,
        margin=ft.Margin(top=0, bottom=0, left=0, right=0),
        animate=ft.Animation(200, "easeInOut"),
        expand=False
    )

    layout = ft.Row(
        controls=[sidebar, body],
        expand=True,
    )

    # Coluna principal para manter o layout estável
    main_column = ft.Column(
        controls=[topbar, layout],
        expand=True,
    )

    # Inicializa com a tela principal
    body_column.controls.clear()
    body_column.controls.append(homePage.body(page))

    page.add(main_column)

ft.app(target=main)