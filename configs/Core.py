from configs.classes.CurrentMusic import CurrentMusic

music = CurrentMusic("Nome Musica", "Nome Artista")
def setArtist(artist):
    music.artist = artist
def getArtist():
    return music.artist

def getTitle():
    return music.title
def getArtist():
    return music.artist