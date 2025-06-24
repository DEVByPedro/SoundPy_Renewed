import subprocess
import sys

def installDependencies():
    try:
        import flet
        import tkinter as tk
        from mutagen.mp3 import MP3
        from PIL import Image
    except Exception as e:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flet"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "mutagen"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
        import flet
        from mutagen.mp3 import MP3
        from PIL import Image

    return