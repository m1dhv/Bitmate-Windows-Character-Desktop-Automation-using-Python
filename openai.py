import pyautogui
import time

def askai(msg):
    pyautogui.hotkey('win','r')
    pyautogui.write('Brave')
    pyautogui.press('enter')
    time.sleep(3)
    pyautogui.hotkey('ctrl','l')
    pyautogui.write('https://chatgpt.com/')
    pyautogui.press('enter')
    time.sleep(5)
    pyautogui.write(msg)
    pyautogui.press('enter')
    print(msg)
