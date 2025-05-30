import subprocess
import sys

def installDependencies():
    try:
        import flet
    except Exception as e:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flet"])
        import flet

    return