#!/usr/bin/env python3

"""Connects online using standard urllib libraries."""

from json import loads
from json.decoder import JSONDecodeError
from io import BytesIO
from bs4 import BeautifulSoup
from requests import exceptions
from requests import Session
from shutil import copyfileobj
from urllib.error import HTTPError
from os.path import abspath, exists
from dvk_archive.processing.string_processing import extend_int
from dvk_archive.processing.string_processing import get_extension


def get_headers() -> dict:
    """Return headers to use when making a URL connection."""
    headers = {
        "User-Agent":
        "Mozilla/5.0 (X11; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0",
        "Accept-Language":
        "en-US,en;q=0.5"}
    return headers


def bs_connect(
        url: str = None,
        encoding: str = "utf-8",
        data: dict = None) -> BeautifulSoup:
    """
    Connect to a URL and returns a BeautifulSoup object.

    Incapable of working with JavaScript.

    Parameters:
        url (str): URL to retrieve
        encoding (str): Text encoding to use
        data (dict): Request payload for post requests

    Returns:
        BeautifulSoup: BeautifulSoup object of the url page
    """
    html = basic_connect(url, encoding, data)
    if html is None or html == "":
        return None
    return BeautifulSoup(html, features="lxml")


def json_connect(
        url: str = None,
        encoding: str = "utf-8",
        data: dict = None) -> dict:
    """
    Connect to a URL and returns a dictionary based on JSON data.

    Incapable of working with JavaScript.

    Parameters:
        url (str): URL to retrieve
        encoding (str): Text encoding to use
        data (dict): Request payload for post requests

    Returns:
        dict: Dictionary from JSON data
    """
    html = basic_connect(url, encoding, data)
    if html is None or html == "":
        return None
    try:
        json = loads(html)
        return json
    except JSONDecodeError:
        return None


def basic_connect(
        url: str = None,
        encoding: str = "utf-8",
        data: dict = None) -> str:
    """
    Connect to a URL and returns a the HTML source.

    Incapable of working with JavaScript.

    Parameters:
        url (str): URL to retrieve
        encoding (str): Text encoding to use
        data (dict): Request payload for post requests

    Returns:
        str: HTML source
    """
    if url is None or url == "":
        return None
    session = Session()
    headers = get_headers()
    try:
        if data is None:
            request = session.get(url, headers=headers)
        else:
            request = session.post(url, data=data)
        if encoding is None:
            request.encoding = request.apparent_encoding
        else:
            request.encoding = encoding
        return request.text
    except (exceptions.ConnectionError,
            exceptions.MissingSchema,
            ConnectionResetError):
        return None
    return None


def download(url: str = None, filename: str = None) -> dict:
    """
    Download a file from a given url to a given file path.

    Parameters:
        url (str): URL from which to download
        filename (str): File path to save to
    """
    if (url is not None
            and not url == ""
            and filename is not None
            and not filename == ""):
        file = abspath(filename)
        if exists(file):
            extension = get_extension(filename)
            base = filename[0:len(filename) - len(extension)]
            num = 1
            while exists(file):
                file = base + "(" + str(num) + ")" + extension
                num = num + 1
        # SAVE FILE
        try:
            session = Session()
            headers = get_headers()
            response = session.get(url, headers=headers)
            byte_obj = BytesIO(response.content)
            byte_obj.seek(0)
            with open(file, "wb") as f:
                copyfileobj(byte_obj, f)
            return response.headers
        except (HTTPError,
                exceptions.ConnectionError,
                exceptions.MissingSchema,
                ConnectionResetError):
            print("Failed to download:" + url)
    return dict()


def get_last_modified(headers: dict = None) -> str:
    """
    Return the time a webpage was last formatted from its request headers.

    Parameters:
        headers (dict): HTML request headers

    Returns:
        str: Last formatted date and time in DVK format
    """
    if headers is None:
        return ""
    try:
        modified = headers["Last-Modified"]
    except KeyError:
        return ""
    try:
        day = int(modified[5:7])
        month_str = modified[8:11].lower()
        year = int(modified[12:16])
        hour = int(modified[17:19])
        minute = int(modified[20:22])
        # GET MONTH
        months = [
            "jan", "feb", "mar", "apr", "may", "jun",
            "jul", "aug", "sep", "oct", "nov", "dec"]
        month = 0
        while month < 12:
            if month_str == months[month]:
                break
            month += 1
        month += 1
        if month > 12:
            return ""
        time = extend_int(year, 4) + "/" + extend_int(month, 2) + "/"
        time = time + extend_int(day, 2) + "|" + extend_int(hour, 2)
        time = time + ":" + extend_int(minute, 2)
        return time
    except ValueError:
        return ""


def remove_header_footer(input_str: str = None) -> str:
    """
    Return html string with header and footer removed.

    Parameters:
        input_str (str): Given HTML string

    Returns:
        str: String with header and footer removed
    """
    if input_str is None or input_str == "":
        return ""
    # REMOVE FOOTER
    final = input_str.replace("\n", "")
    if final[len(final) - 1] == ">":
        end = final.rfind("<")
        final = final[0:end]
    # REMOVE HEADER
    if len(final) > 0 and final[0] == "<":
        try:
            start = final.index(">") + 1
            final = final[start:]
        except ValueError:
            pass
    # REMOVE START SPACE
    start = 0
    while start < len(final) and final[start] == " ":
        start += 1
    final = final[start:]
    # REMOVE END SPACE
    end = len(final) - 1
    while end > -1 and final[end] == " ":
        end -= 1
    final = final[0:end + 1]
    return final
