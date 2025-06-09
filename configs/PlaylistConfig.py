import json
import os
from mutagen.mp3 import MP3

import configs.MusicConfig as musicConfig
import infra.BodyContent     as bodyContent
import infra.PlaylistContent as playlistContent

fileJSON = os.path.join(os.path.abspath("configs/intern"), "Playlist.json")
def add_playlist(name: str):

    with open(fileJSON, "r") as file:
        playlist = json.load(file)

    for id, nameOfPlay in playlist['playlistNames']:
        if nameOfPlay == name:
            return "Already inserted"
        maxId = id + 1

    playlist["playlistNames"].append([maxId, name])
    playlist['playlistMusics'].append([maxId, []])
    with open(fileJSON, "w") as file:
        json.dump(playlist, file, indent=4)
def remove_playlist_by_name(name: str):
    with open(fileJSON, "r") as file:
        playlist = json.load(file)

    for i in range(len(playlist['playlistNames'])):
        if playlist['playlistNames'][i][1] == name:
            playlist['playlistNames'].pop()
            playlist["playlistMusics"].pop()

    with open(fileJSON, "w") as file:
        json.dump(playlist, file, indent=4)
def get_all_playlists():
    with open(fileJSON, "r") as file:
        playlist = json.load(file)

    allPlaylists = []

    for playlist in playlist["playlistNames"]:
        allPlaylists.append(playlist)

    return allPlaylists
def getPlaylistNameByIndex(index):
    with open(fileJSON, "r") as file:
        playlist = json.load(file)

    for i in range(len(playlist["playlistNames"])):
        if i == index - 1:
            return playlist["playlistNames"][i][1]
def getDuration(id):
    with open(fileJSON, "r") as file:
        playlist = json.load(file)

    for playlistId in playlist["playlistMusics"]:
        if playlistId[0] == id:
            if playlistId[1] == "all":
                return musicConfig.getDuration()
            total = 0
            for path in playlistId[1]:
                total += MP3(path).info.length

                seconds = total
                minutes = 0
                hours = 0

                while seconds > 59:
                    seconds -= 60
                    minutes += 1
                while minutes > 59:
                    minutes -= 60
                    hours += 1

                return f"{round(hours):02d}:{round(minutes):02d}:{round(seconds):02d}"
        return "00:00:00"
def getPlaylistMusicsById(e, id, body, page):
    with open(fileJSON, "r") as file:
        playlist = json.load(file)

    for playlists in playlist["playlistNames"]:
        if playlists[0] == id:
            if playlists[1] == "all":
                body.content = bodyContent.AllSongs(page)
            else:
                body.content = playlistContent.AllPlaylistSongs(page, id)
            break
    page.update()
def get_all_playlist_musics(id):
    with open(fileJSON, "r") as file:
        playlist = json.load(file)

    for pl in playlist["playlistMusics"]:
        if pl[0] == id:
            if pl[1] == "all":
                return musicConfig.get_all_musics()
            return pl[1]
def deleteByIndex(idPlaylist, index):
    with open(fileJSON, "r") as file:
        playlist = json.load(file)

    for play in playlist["playlistMusics"]:
        if play[0] == idPlaylist:
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
            return play[1].index(path)
    return None
