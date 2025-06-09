import json
import os
import tkinter as tk
from tkinter import filedialog
import setup.bin.CreateJSONS as createJSONs

fileJSON = os.path.join(os.path.abspath("configs/intFiles"), "User.json")

def get_user_pfp():
    if createJSONs.createJsonSetup():

        with open (fileJSON, "r") as file:
            userProf = json.load(file)

        if userProf['pfp_path'] == "":
            return ""
        else:
            return userProf['pfp_path']
def find_pfp():
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    file_path = filedialog.askopenfile(title="Select a picture", filetypes=[ ("JPG", ".jpg"),("PNG", ".png"), ("JPEG", ".jpeg")])
    if add_pfp(file_path.name) == True:
        return True
def add_pfp(path: str):
    if os.path.exists(path):
        if path.endswith(".jpg" or ".png" or ".jpeg"):
            with open(fileJSON, "r") as file:
                userConf = json.load(file)

            userConf["pfp_path"] = path
            with open(fileJSON, "w") as file:
                json.dump(userConf, file, indent=4)
            return True
        return "Invalid type of file. (Only accepts .jpg, .png and .jpeg)"
    return "The path given does not exists."
def getUserName():
    try:
        with open(fileJSON, "r") as file:
            user = json.load(file)

        return user["name"]
    except Exception as e:
        return f"Error: {e}"