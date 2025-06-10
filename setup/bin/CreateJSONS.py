import os.path
import json

path = os.path.abspath("configs/intFiles")
def createPlaylistJson():
    caminho_file = os.path.join(path, "Playlist.json")

    # Cria a pasta se não existir
    if not os.path.exists(caminho_file):
        os.makedirs(path, exist_ok=True)

        # Cria os dados iniciais
        dados = {
            "playlistNames": [[1, "Todas as Musicas"]],
            "playlistMusics": [[1, "all"]]
        }

        with open(caminho_file, "w", encoding="utf-8") as file:
            json.dump(dados, file, indent=4, ensure_ascii=False)
def createSongJson():
    caminho_file = os.path.join(path, "Song.json")

    # Cria a pasta se não existir
    if not os.path.exists(caminho_file):
        os.makedirs(path, exist_ok=True)

        # Cria os dados iniciais
        dados = {
            "paths": [],
            "duration": 0
        }

        with open(caminho_file, "w", encoding="utf-8") as file:
            json.dump(dados, file, indent=4, ensure_ascii=False)
def createUserJson():
    caminho_file = os.path.join(path, "User.json")

    # Cria a pasta se não existir
    if not os.path.exists(caminho_file):
        os.makedirs(path, exist_ok=True)
        # Cria os dados iniciais
        dados = {
            "name": "User",
            "pfp_path": "",
            "email": ""
        }

        with open(caminho_file, "w", encoding="utf-8") as file:
            json.dump(dados, file, indent=4, ensure_ascii=False)
        return True
    else:
        return True

def createJsonSetup():
    createUserJson()
    createPlaylistJson()
    createSongJson()
