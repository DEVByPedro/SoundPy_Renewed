import json
import os

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

    for id, playlistName in playlist['playlistNames']:
        print(id, playlistName)