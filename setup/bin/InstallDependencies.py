import subprocess
import sys

def installDependencies():
    try:
        import flet
        import tkinter as tk
        from tkinter import filedialog
        from mutagen.mp3 import MP3
    except Exception as e:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flet"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "tkinter"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "mutagen"])
        import flet
        import tkinter as tk
        from tkinter import filedialog
        from mutagen.mp3 import MP3
    return