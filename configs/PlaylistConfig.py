import json
import os
from mutagen.mp3 import MP3

import configs.MusicConfig as musicConfig
import infra.BodyContent as bodyContent
import infra.PlaylistContent as playlistContent

fileJSON = os.path.join(os.path.abspath("configs/intFiles"), "Playlist.json")

def add_playlist(name: str):
    with open(fileJSON, "r") as file:
        playlist = json.load(file)
    maxId = 1
    for id, nameOfPlay in playlist['playlistNames']:
        if nameOfPlay == name:
            return "Already inserted"
        if id >= maxId:
            maxId = id + 1
    playlist["playlistNames"].append([maxId, name])
    playlist['playlistMusics'].append([maxId, []])
    with open(fileJSON, "w") as file:
        json.dump(playlist, file, indent=4)

def remove_playlist_by_name(name: str):
    with open(fileJSON, "r") as file:
        playlist = json.load(file)
    idx = None
    for i, pl in enumerate(playlist['playlistNames']):
        if pl[1] == name:
            idx = i
            break
    if idx is not None:
        playlist['playlistNames'].pop(idx)
        playlist["playlistMusics"].pop(idx)
    with open(fileJSON, "w") as file:
        json.dump(playlist, file, indent=4)

def get_all_playlists():
    with open(fileJSON, "r") as file:
        playlist = json.load(file)
    return playlist["playlistNames"]

def getPlaylistNameByIndex(index):
    with open(fileJSON, "r") as file:
        playlist = json.load(file)
    for pl in playlist["playlistNames"]:
        if pl[0] == index:
            return pl[1]
    return ""

def getDuration(id):
    with open(fileJSON, "r") as file:
        playlist = json.load(file)
    for playlistId in playlist["playlistMusics"]:
        if playlistId[0] == id:
            if playlistId[1] == "all":
                return musicConfig.getDuration()
            total = 0
            for path in playlistId[1]:
                try:
                    total += MP3(path).info.length
                except Exception:
                    continue
            seconds = int(total)
            minutes = seconds // 60
            hours = minutes // 60
            seconds = seconds % 60
            minutes = minutes % 60
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return "00:00:00"

def getPlaylistMusicsById(e, id, body, page):
    with open(fileJSON, "r") as file:
        playlist = json.load(file)
    for playlists in playlist["playlistNames"]:
        if playlists[0] == id:
            body.content.controls.clear()
            if playlists[1] == "all":
                body.content.controls.append(bodyContent.AllSongs(page))
            else:
                body.content.controls.append(playlistContent.AllPlaylistSongs(page, id))
            break
    body.content.update()
    body.update()
    page.update()

def get_all_playlist_musics(id):
    with open(fileJSON, "r") as file:
        playlist = json.load(file)
    for pl in playlist["playlistMusics"]:
        if pl[0] == id:
            if pl[1] == "all":
                return musicConfig.get_all_musics()
            return pl[1]
    return []

def deleteByIndex(idPlaylist, index):
    with open(fileJSON, "r") as file:
        playlist = json.load(file)
    for play in playlist["playlistMusics"]:
        if play[0] == idPlaylist:
            if play[1] == "all":
                all = musicConfig.get_all_musics()
                if index < 0 or index >= len(all):
                    return -1
                musicConfig.deleteByIndex(index)
                return 1
            if 0 <= index < len(play[1]):
                play[1].pop(index)
                with open(fileJSON, "w") as file:
                    json.dump(playlist, file, indent=4)
                return 1
    return -1

def getIndexByPath(idPlaylist, path):
    with open(fileJSON, "r") as file:
        playlist = json.load(file)
    for play in playlist["playlistMusics"]:
        if play[0] == idPlaylist:
            if play[1] == "all":
                all = musicConfig.get_all_musics()
                for row in all:
                    if row == path:
                        return all.index(row)
            if path in play[1]:
                return play[1].index(path)
    return None