from selenium import webdriver
import time
import os
import shutil

def get_download_path():
    """Returns the default downloads path for linux or windows"""
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser('~'), 'downloads')

def download_cboe_data(refresh_seconds):
    browser = webdriver.Chrome()
    browser.set_window_size(1000, 1000)
    url = "http://www.cboe.com/delayedquote/quote-table-download"
    browser.get(url)

    while True:
        try:
            symbol_box = browser.find_element_by_id("txtTicker")
            symbol_box.send_keys("SPX")
            browser.find_element_by_id("cmdSubmit").click()
            symbol_box.clear()
            time.sleep(1)
            path = get_download_path()
            filename = max([path + "\\" + f for f in os.listdir(path)],key=os.path.getctime)
            shutil.move(filename,os.path.join(path,r"SPX_cboe.csv"))
            symbol_box.send_keys("VIX")
            browser.find_element_by_id("cmdSubmit").click()
            symbol_box.clear()
            time.sleep(1)
            filename = max([path + "\\" + f for f in os.listdir(path)],key=os.path.getctime)
            shutil.move(filename,os.path.join(path,r"VIX_cboe.csv"))
            time.sleep(refresh_seconds)
            if (refresh_seconds == 0):
                break
        except:
            print("Terminating program...")
            break
    browser.close()