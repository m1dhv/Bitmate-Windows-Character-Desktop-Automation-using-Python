import pyautogui
import time


def open_software(software_name: str):
    # Open Start menu
    pyautogui.press('win')
    time.sleep(1)  # Wait for the menu to open

    # Type the software name
    pyautogui.write(software_name, interval=0.1)
    time.sleep(1)  # Wait for the search results

    # Press Enter to launch the application
    pyautogui.press('enter')
    print(f"Opening {software_name}...")