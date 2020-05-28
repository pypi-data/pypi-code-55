"""
MIT License

Copyright (c) 2020 LidaRandom

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from time import sleep
from pathlib import Path

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webelement import FirefoxWebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BrowserTab:
    """A simple abstraction over Selenium Firefox WebDriver,
       which makes common actions with webdriver as simple and safely.

       Require geckodriver in PATH.

       Args:
        url - site URL
    """

    def __init__(self, url: str):
        self._webpage_url = str(url)
        self._wait_time = 60
        self._webdriver = None
        self._download_dir = str(Path(__file__).parent.absolute())

    def _get_element(self, xpath: str) -> FirefoxWebElement:
        try:
            element = WebDriverWait(self._webdriver, self._wait_time).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            sleep(1)
            return element
        except TimeoutException:
            raise Exception(f"Element with {xpath} XPATH not finded.")

    def open(self):
        webdrive_options = FirefoxOptions()
        webdrive_options.headless = True
        webdrive_options.set_preference("browser.download.folderList", 2)
        webdrive_options.set_preference(
            "browser.download.dir", self._download_dir
        )
        webdrive_options.set_preference(
            "browser.download.useDownloadDir", True
        )
        webdrive_options.set_preference(
            "browser.helperApps.neverAsk.saveToDisk",
            "application/vnd.ms-excel",
        )
        self._webdriver = Firefox(
            options=webdrive_options, service_log_path="/dev/null"
        )
        if "http://" or "https://" not in self._webpage_url:
            self._webdriver.get(f"https://{self._webpage_url}")
        else:
            self._webdriver.get(self._webpage_url)

    def close(self):
        if self._webdriver is None:
            raise Exception("Open the site before closing it")
        self._webdriver.quit()
        self._webdriver = None

    def click(self, xpath: str, wait_for_element: str = None):
        self._get_element(xpath).click()
        if wait_for_element is not None:
            self._get_element(wait_for_element)

    def set_element_value(self, xpath: str, value: str):
        self._get_element(xpath).send_keys(value)

    def exec_js_file(self, script_name: str):
        with open(
            Path(__file__).parent.absolute() / Path(script_name)
        ) as file:
            self._webdriver.execute_script("\n".join(file.readlines()))


__all__ = ["BrowserTab"]
