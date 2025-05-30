import json
import os

def addMusic(path: str):
    fileJSON = os.path.join(os.path.abspath("configs/intern"), "Song.json")
    song = []

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
        song['paths'].append(path)

        with open(fileJSON, "w") as file:
            json.dump(song, file, indent=4)

        return True

def getPathByIndex(index: int):
    try:
        fileJson = os.path.join(os.path.abspath("configs/intern"), "Song.json")
        sngPaths = []
        with open(fileJson, "r") as file:
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
