import json
import os
import setup.bin.InstallDependencies as installDep
import flet as ft
from mutagen.mp3 import MP3

fileJSON = os.path.join(os.path.abspath("configs/intern"), "Song.json")
def addMusic(path: str):

    if len(path) > 0:
        with open(fileJSON, "r") as file:
            song = json.load(file)
    else:
        return "No valid path given"

    try:
        index_of_song = song['paths'].index(path)
        if index_of_song >= 0:
            return "The path given is already existent"
    except Exception as e:
        if path.endswith(".mp3"):
            song['paths'].append(path)

            with open(fileJSON, "w") as file:
                json.dump(song, file, indent=4)

            return True
def getPathByIndex(index: int):
    try:
        with open(fileJSON, "r") as file:
            sngPaths = json.load(file)

        return sngPaths["paths"][index]

    except Exception as e:
        return "No path found on index: " + str(index)
def deleteByIndex(index: int):
    try:
        fileJson = os.path.join(os.path.abspath("configs/intern"), "Song.json")
        sngPaths = []
        with open(fileJson, "r") as file:
            sngPaths = json.load(file)

        sngPaths['paths'].pop(index)
        with open(fileJson, "w") as file:
            json.dump(sngPaths, file, indent=4)

        return True
    except Exception as e:
        return "No paths excluded."
def getDuration(index):
    total = 0
    if index == "all":
        with open(fileJSON, "r") as file:
            todas = json.load(file)

        if len(todas['paths']) > 0:
            for musicas in todas["paths"]:
                total += MP3(musicas).info.length

            seconds = 0
            minutes = 0
            hours   = 0

            seconds += total
            while seconds > 59:
                minutes += 1
                seconds -= 60
            while minutes > 59:
                minutes -= 59
                hours += 1

            totalInString = f"{round(hours):02d}:{round(minutes):02d}:{round(seconds):02d}"

            todas['total'] = totalInString

            with open(fileJSON, 'w') as file:
                json.dump(todas, file, indent=4)

            return totalInString
        return "00:00:00"
def get_all_musics():
    try:
        with open(fileJSON, 'r')as file:
            songs = json.load(file)

        if len(songs['paths']) >= 0:
            return songs['paths'][0]
        return ft.Text("No paths were found")
    except Exception as e:
        print(e)