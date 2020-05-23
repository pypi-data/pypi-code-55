import pyautogui
import json
from pynput import keyboard
click_list = []
x = []
y = []
current = set()
mousecombo = {keyboard.Key.alt, keyboard.KeyCode.from_char("p")}
end = {keyboard.Key.alt, keyboard.KeyCode.from_char("f")}
print("ready!")
def on_press(key):
    """Ignore for end-user"""
    if key in mousecombo:
        current.add(key)
        print("Position Marked")
        click_list.append(pyautogui.position())
    elif key in end:
        current.add(key)
        print("ended \n, processing, this might take a few seconds.")
        return False

def on_release(key):
    """Ignore for end-user"""
    if key == keyboard.Key.esc:
        # Stop listener
        return False
    try: current.remove(key)
    except KeyError: pass


def get_input(file_name = 'data.json'):
    """file_name: the file name that you would like the logs to go to. By default it's data.json.
    If you change it here, be sure to specify it on other functions like click.autoclick().
    This function gets the input from the user that it is supposed to replicate"""
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    listener.join() # wait till listener will stop
    # other stuff        
    #x = [i[0] for i in click_list]
    #y = [i[1] for i in click_list]
    with open(file_name, 'w') as outfile:
        json.dump(click_list, outfile)
    return(0)