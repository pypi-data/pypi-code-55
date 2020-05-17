import requests
import bs4
from bs4 import BeautifulSoup
import platform
import subprocess
from subprocess import call
import os
import sys 


class DriverDownloader:

    os = platform.platform()
    # Links for browser automation drivers

    def __init__(self):
        self.site = ""

    # Sets the website to get HTML page

    def set_site(self, site):
        self.site = site
        response = self.load_response()
        return self.parse_html(response)
    # Return the site visited in text

    def get_site(self):
        print(self.site)

    def set_savepath(self, path):
        self.savepath = path

    def get_savepath(self):
        return self.savepath
    # Loads download page web request responses

    def load_response(self):
        return requests.get(self.site, timeout=5)

    # Method for parsing HTML
    def parse_html(self, response_text):
        soup = BeautifulSoup(response_text.text, "html.parser")
        return soup

    # Search for particular element in HTML
    def search_attribute(self, attr):
        response = self.load_response()
        html = self.parse_html(response)
        search_attr = html.select(attr)
        return search_attr

    # Check OS of system
    @classmethod
    def get_os(cls):
        if ("Darwin" in cls.os):
            return "mac"
        elif ("Linux" in cls.os):
            return "lin"
        elif ("Windows" in cls.os):
            return "win"
        else:
            return "OS Unknown"

    # Allow user to choose browser automation driver
    def choose_driver(self):
        browser_choice = input(
            "Choose a Browser Driver for download:\n1.) GeckoDriver\n2.) ChromeDriver\n")
        if (browser_choice == str(1)):
            return 1
        elif (browser_choice == str(2)):
            return 2
        else:
            return None

    # Get CPU Architecture of system
    @classmethod
    def detect_arch(cls):
        if ("x86_64" in cls.os):
            return str(64)
        elif ("x64" in cls.os):
            return str(32)
        else:
            return None

    # Runs commands from command line of system
    @classmethod
    def run_cmd(cls, command):
        return str(subprocess.check_output(command, stdin=subprocess.PIPE, shell=True, universal_newlines=True))

    # Get version of Google Chrome
    def get_chrome_version(self):
        os = self.get_os()
        cmd = ""
        if (os == "mac"):
            cmd = "\"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome\" --version | cut -d ' ' -f 3"
        elif (os == "lin"):
            cmd = "google-chrome --version | cut -d ' ' -f 3"
        elif (os == "win"):
            pass
        else:
            return "None"

        return str(self.run_cmd(cmd))

    # Filers raw link data
    def filter_links(self, link_list):
        links = [link.get("href") for link in link_list]
        return links

    #
    def download_gecko(self, links):
        # Get OS of system
        os = self.get_os()
        # Get System aArchitecture of system
        arch_type = self.detect_arch()
        for link in links:
            if (os == "mac"):
                if (os in link):
                    return link
            else:
                if (os in link and arch_type in link):
                    return link

    # Sava the browser driver binary to a certain file
    def save_file(self, link):
        if link.find('/'):
            file_name = link.rsplit('/', 1)[1]
        response = requests.get(link, allow_redirects=True)
        dir = self.savepath
        files = str(self.run_cmd(f"ls {dir}"))

        file = open(f"{self.savepath}{file_name}", 'wb')
        file.seek(0)
        file.truncate()
        file.write(response.content)
        file.close()
        self.extract_file(file_name)
        return file_name

    def extract_file(self, filename):
        if "gecko" in filename:
            self.run_cmd(
                f"cd {self.savepath} && tar -xf {filename} && rm -rf {filename}")
        elif "chrome" in filename:
            self.run_cmd(
                f"cd {self.savepath} && rm -rf chromedriver && unzip {filename} && rm -rf {filename}")
        else:
            return None

    def download(self):
        # Get OS of system
        os_type = self.get_os()
        driver_choice = self.choose_driver()
        # Have conditions for each download choice
        if (driver_choice == 1):
            base_git = "https://www.github.com"
            gecko_site = self.set_site(
                "https://github.com/mozilla/geckodriver/releases")

            link_data = gecko_site.select(
                ".d-flex.flex-items-center.min-width-0")
            del link_data[4:-1]
            links = self.filter_links(link_data)
            link = self.download_gecko(links)
            github_link = base_git + link
            file_name = self.save_file(github_link)
            print(
                f"Geckodriver has been successfully installed in: {self.savepath}")

        elif (driver_choice == 2):
            chrome_release_base = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_"
            chrome_driver_baseurl = "https://chromedriver.storage.googleapis.com/"
            chrome_version = self.get_chrome_version()[0:9]
            chrome_release_full = chrome_release_base + chrome_version
            chromedriver_version = self.set_site(chrome_release_full)
            chromedriver_url = str(chrome_driver_baseurl +
                                   str(chromedriver_version) + "/")

            if (os_type == "mac"):
                chromedriver_url += "chromedriver_mac64.zip"
            elif (os_type == "lin"):
                chromedriver_url += "chromedriver_linux64.zip"
            elif (os_type == "win"):
                chromedriver_url += "chromedriver_win32.zip"
            else:
                return None
            file_name = self.save_file(
                chromedriver_url)
            print(
                f"Chromedriver has been successfully installed in: {self.savepath}")

        else:
            return None

    
if __name__ == "__main__":
    try:
        downloader = DriverDownloader()
        downloader.set_savepath(sys.argv[1] + "/")
        downloader.download()
    except (subprocess.CalledProcessError, IndexError) as error:
        print("Directory does not exist. Please try again")
        sys.exit(0)
        

