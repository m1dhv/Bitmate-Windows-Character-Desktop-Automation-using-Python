import json
import os
import pyautogui
import time
import pyperclip

# Define the JSON file name
JSON_FILE = 'data.json'

# Function to load data from the JSON file
def load_data():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r') as file:
            return json.load(file)
    return {}

# Function to save data to the JSON file
def save_data(data):
    with open(JSON_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Function to add a new name and link to the JSON file
def add_entry(name, link):
    data = load_data()
    data[name] = link
    save_data(data)
    print(f"Added: {name} -> {link}")

# Function to retrieve a link by name
def get_link(name):
    data = load_data()
    return data.get(name, "Name not found")

# Function to delete an entry by name
def delete_entry(name):
    data = load_data()
    if name in data:
        del data[name]
        save_data(data)
        print(f"Deleted: {name}")
    else:
        print(f"{name} not found in the data.")

def dircopy(Dirname):
    pyautogui.hotkey('alt','d')
    pyautogui.hotkey('ctrl','c')
    dir = pyperclip.paste()
    add_entry(Dirname,dir)

def diropen(Dirname):
    link = get_link(Dirname)

    if link == "Name not found":
        print("not found")
    else:
        pyautogui.hotkey('win','e')
        time.sleep(1)
        pyautogui.hotkey('alt','d')
        pyautogui.write(link)
        pyautogui.press('enter')


