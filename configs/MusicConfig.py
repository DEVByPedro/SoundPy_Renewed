import json
from mutagen.mp3 import MP3
import os
import pygame
import flet as ft

fileJSON = os.path.join(os.path.abspath("configs/intFiles"), "Song.json")
status = {"is_paused": None}
pygame.init()
mixer = pygame.mixer

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
            getDuration()

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
        with open(fileJSON, "r") as file:
            sngPaths = json.load(file)

        sngPaths['duration'] -= MP3(sngPaths['paths'][index]).info.length
        sngPaths['paths'].pop(index)

        with open(fileJSON, "w") as file:
            json.dump(sngPaths, file, indent=4)

        return True
    except Exception as e:
        return "No paths excluded."

def get_all_musics():
    try:
        with open(fileJSON, "r") as file:
            songs = json.load(file)
        allPaths = []

        for path in songs['paths']:
            allPaths.append(path)

        return allPaths
    except Exception as e:
        return "Error: "+ e

def getDuration():
    try:
        with open(fileJSON, "r") as file:
            songs = json.load(file)

        songs['duration'] = 0
        total = 0
        for path in songs["paths"]:
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

        songs['duration'] = round(float(total))
        with open(fileJSON, "w") as file:
            json.dump(songs, file, indent=4)
        return f"{round(hours):02d}:{round(minutes):02d}:{round(seconds):02d}"

    except Exception as e:
        return "00:00:00"

def getIndividualDuration(path: str):
    if os.path.exists(path):
        if path.endswith(".mp3"):
            total = MP3(path).info.length
            seconds = total
            minutes = 0

            while seconds > 59:
                seconds -= 60
                minutes += 1

            return f"{round(minutes):02d}:{round(seconds):02d}"
        return "Please, select a .mp3 file."
    return "Path given does not exists"

def getIndexByPath(path:  str):
    try:
        with open(fileJSON, "r") as file:
            songs = json.load(file)

        for pathIndex in range(len(songs['paths'])):
            if songs['paths'][pathIndex] == path:
                return pathIndex

    except Exception as e:
        return f"Error: {e}"

def playMusic(e, path: str):

    if not os.path.exists(path):
        return "Path given does not exists"

    if path.endswith(".mp3"):
        try:
            mixer.music.load(path)

            if status["is_paused"] == False:
                mixer.pause()
                status["is_paused"] = True
            elif status["is_paused"] == True:
                mixer.unpause()
                status["is_paused"] = False
            mixer.music.play()

            if mixer.get_busy() == False:
                status["is_paused"] = None

            e.control.style.color = "#27e91d"
            e.control = ft.Icon(ft.Icons.PAUSE_SHARP, color="white", size=20)
            e.update()
        except Exception as e:
            return f"Error playing music: {e}"
    return "Please, select a .mp3 file."

def stopSong():
    if mixer.get_busy():
        mixer.music.stop()
        return
    return