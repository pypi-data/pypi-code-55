#!/usr/bin/env python3

"""Handles DVK files."""

from os import remove, rename, pardir
from os.path import abspath, basename, exists, isfile, join
from json import dump, load
from random import seed, randint
from dvk_archive.processing.html_processing import add_escapes_to_html
from dvk_archive.processing.list_processing import clean_list
from dvk_archive.processing.string_processing import extend_int
from dvk_archive.processing.string_processing import get_filename
from dvk_archive.processing.string_processing import get_extension
from dvk_archive.web.basic_connect import download, get_last_modified


class Dvk:
    """
    Class for handling DVK files.

    Attributes:
        dvk_file (str): File path of the current DVK file
        id (str): DVK ID
        title (str): DVK title
        artists (list): DVK artist List
        time (str): DVK Time of publication (YYYY/MM/DD|hh:mm)
        web_tags (list): DVK web tag list
        description (str): DVK description
        page_url (str): DVK Page URL
        direct_url (str): DVK Direct URL
        secondary_url (str): DVK Secondary URL
        media_file (str): DVK media file path
        secondary_file (str): DVK secondary media file path
    """

    def __init__(self, file_path: str = None):
        """Initialize all DVK values, reading from a DVK file, if given."""
        # CLEAR DVK VALUES
        self.dvk_file = ""
        self.set_file(file_path)
        self.clear_dvk()

        if self.get_file() is not None:
            self.read_dvk()

    def clear_dvk(self):
        """Set all DVK data to their default values."""
        self.set_id()
        self.set_title()
        self.set_artist()
        self.set_time()
        self.set_web_tags()
        self.set_description()
        # WEB
        self.set_page_url()
        self.set_direct_url()
        self.set_secondary_url()
        # FILE
        self.set_media_file()
        self.set_secondary_file()

    def write_dvk(self):
        """Write DVK data to the currently set DVK file."""
        if self.can_write():
            data = dict()
            data["file_type"] = "dvk"
            data["id"] = self.get_id()
            # INFO
            dvk_info = dict()
            dvk_info["title"] = self.get_title()
            dvk_info["artists"] = self.get_artists()
            value = self.get_time()
            if not self.get_time() == "0000/00/00|00:00":
                dvk_info = self.add_to_dict(dvk_info, "time", value)
            value = self.get_web_tags()
            dvk_info = self.add_to_dict(dvk_info, "web_tags", value)
            value = self.get_description()
            dvk_info = self.add_to_dict(dvk_info, "description", value)
            data = self.add_to_dict(data, "info", dvk_info)
            # WEB
            dvk_web = dict()
            value = self.get_page_url()
            dvk_web = self.add_to_dict(dvk_web, "page_url", value)
            value = self.get_direct_url()
            dvk_web = self.add_to_dict(dvk_web, "direct_url", value)
            value = self.get_secondary_url()
            dvk_web = self.add_to_dict(dvk_web, "secondary_url", value)
            data = self.add_to_dict(data, "web", dvk_web)
            # FILE
            dvk_fd = dict()
            value = basename(self.get_media_file())
            dvk_fd = self.add_to_dict(dvk_fd, "media_file", value)
            if self.get_secondary_file() is not None:
                value = basename(self.get_secondary_file())
                dvk_fd = self.add_to_dict(dvk_fd, "secondary_file", value)
            data = self.add_to_dict(data, "file", dvk_fd)
            # WRITE
            try:
                with open(self.get_file(), "w") as out_file:
                    dump(data, out_file, indent=4, separators=(",", ": "))

            except IOError as e:
                print("File error: " + str(e))

    def write_media(self, get_time: bool = False):
        """
        Write the DVK file and downloads associated media, if available.

        Nothing is writen if DVK or media URLs are invalid.

        Parameters:
            get_time (bool): Whether to get the last modified time of URL
                             for the DVK's time published
        """
        self.write_dvk()
        if exists(self.get_file()):
            # DOWNLOAD MEDIA FILE
            mf = self.get_media_file()
            headers = download(self.get_direct_url(), mf)
            if exists(self.get_media_file()):
                # DOWNLOAD SECONDARY FILE
                if self.get_secondary_url() is not None:
                    download(
                        self.get_secondary_url(),
                        self.get_secondary_file())
                    if not exists(self.get_secondary_file()):
                        remove(self.get_media_file())
                        remove(self.get_file())
            else:
                remove(self.get_file())
        if get_time and exists(self.get_file()):
            self.set_time(get_last_modified(headers))
            self.write_dvk()

    def read_dvk(self):
        """Read DVK data from the currently set DVK file."""
        self.clear_dvk()
        if self.get_file() is not None and isfile(self.get_file()):
            try:
                with open(self.get_file()) as in_file:
                    data = load(in_file)
                    if data["file_type"] == "dvk":
                        # INFO
                        keys = ["id"]
                        org = self.get_id()
                        value = self.get_from_dict(data, keys, org)
                        self.set_id(value)
                        keys = ["info", "title"]
                        org = self.get_title()
                        value = self.get_from_dict(data, keys, org)
                        self.set_title(value)
                        keys = ["info", "artists"]
                        org = self.get_artists()
                        value = self.get_from_dict(data, keys, org)
                        self.set_artists(value)
                        keys = ["info", "time"]
                        org = self.get_time()
                        value = self.get_from_dict(data, keys, org)
                        self.set_time(value)
                        keys = ["info", "web_tags"]
                        org = self.get_web_tags()
                        value = self.get_from_dict(data, keys, org)
                        self.set_web_tags(value)
                        keys = ["info", "description"]
                        org = self.get_description()
                        value = self.get_from_dict(data, keys, org)
                        self.set_description(value)

                        # WEB
                        keys = ["web", "page_url"]
                        org = self.get_page_url()
                        value = self.get_from_dict(data, keys, org)
                        self.set_page_url(value)
                        keys = ["web", "direct_url"]
                        org = self.get_direct_url()
                        value = self.get_from_dict(data, keys, org)
                        self.set_direct_url(value)
                        keys = ["web", "secondary_url"]
                        org = self.get_secondary_url()
                        value = self.get_from_dict(data, keys, org)
                        self.set_secondary_url(value)

                        # FILE
                        keys = ["file", "media_file"]
                        org = self.get_media_file()
                        value = self.get_from_dict(data, keys, org)
                        self.set_media_file(value)
                        keys = ["file", "secondary_file"]
                        org = self.get_secondary_file()
                        value = self.get_from_dict(data, keys, org)
                        self.set_secondary_file(value)
            except IOError:
                print("Error reading DVK")
                self.clear_dvk()

    def add_to_dict(
            self,
            dictionary: dict = None,
            key: str = None,
            value=None) -> dict:
        """
        Add a key-value pair to dictionary unless values are invalid.

        Parameters:
            dictionary (dict): Dictionary of which to add values
            key (str): Dictionary key
            value(str): Value to pair to key

        Returns:
            dict: Dictionary with values added
        """
        return_dict = dictionary
        if dictionary is not None and key is not None and value is not None:
            return_dict[key] = value
        return return_dict

    def get_from_dict(
            self,
            dictionary: dict = None,
            keys: list = None,
            original=None):
        """
        Return the value of a dictionary from given keys.

        Parameters:
            dictionary (dict): Dictionary to read from
            keys (list): List of keys to read from dictionary
            original: Original value to return if key or dictionary are invalid

        Returns:
            Value of dictionary from keys
        """
        result = original
        if dictionary is not None and keys is not None and not keys == []:
            cur_dict = dictionary
            try:
                for key in keys:
                    result = cur_dict[key]
                    cur_dict = result
            except KeyError:
                result = original
        return result

    def can_write(self) -> bool:
        """
        Return whether the current DVK file is valid for writing.

        Returns false if DVK does not have enough information
        (No title, artists, etc.)

        Returns:
            bool: Whether the current DVK can be written to disk
        """
        if (self.get_file() is None
                or self.get_id() == ""
                or self.get_title() is None
                or self.get_artists() == []
                or self.get_page_url() is None
                or self.get_media_file() is None):
            return False
        return True

    def get_filename(self) -> str:
        """
        Return a filename for the DVK based on its title and ID.

        Returns:
            str: Filename
        """
        if self.get_title() is None or self.get_id() == "":
            return ""
        return get_filename(self.get_title()) + '_' + self.get_id()

    def rename_files(self, filename: str = None):
        """
        Rename the current Dvk file and any linked media files.

        Parameters:
            filename (str): Name to rename files. If none, use default.
        """
        if (self.get_file() is not None and exists(self.get_file())):
            rfile = filename
            if filename is None:
                rfile = self.get_filename()
            parent = abspath(join(self.get_file(), pardir))
            # RENAME DVK
            remove(self.get_file())
            self.set_file(join(parent, rfile + ".dvk"))
            # RENAME MEDIA FILE
            media = self.get_media_file()
            if media is not None and exists(media):
                num = 0
                extension = get_extension(media)
                ifile = "xxtempXXTEMP" + self.get_id() + "_N"
                path = join(parent, ifile + str(num) + extension)
                while exists(path):
                    num = num + 1
                    path = join(parent, ifile + str(num) + extension)
                rename(media, path)
                rpath = join(parent, rfile + extension)
                rename(abspath(path), abspath(rpath))
                self.set_media_file(join(parent, rfile + extension))
            else:
                self.set_media_file("NULL-invalid-file.none")
            # RENAME SECONDARY FILE
            secondary = self.get_secondary_file()
            if secondary is not None and exists(secondary):
                num = 0
                extension = get_extension(secondary)
                ifile = "xxtempXXTEMP" + self.get_id() + "_N"
                path = join(parent, ifile + str(num) + extension)
                while exists(path):
                    num = num + 1
                    path = join(parent, ifile + str(num) + extension)
                rename(secondary, path)
                rpath = join(parent, rfile + extension)
                rename(path, rpath)
                self.set_secondary_file(join(parent, rfile + extension))
            self.write_dvk()

    def set_file(self, file_path: str = None):
        """
        Set the current path for the DVK file.

        Parameters:
            file_path (str): Path for the DVK file
        """
        if file_path is None or file_path == "":
            self.dvk_file = None
        else:
            self.dvk_file = abspath(file_path)

    def get_file(self) -> str:
        """
        Return the current path of the DVK file.

        Returns:
            str: DVK file path
        """
        return self.dvk_file

    def generate_id(self, prefix: str = "", extra: str = ""):
        """
        Generate a psudorandom deterministic ID.

        Based on title, artists, and page URL.

        Parameters:
            prefix (str): String at the start of ID
            extra (str): Extra string for changing random seed
        """
        if (self.get_title() is not None
                and len(self.get_artists()) > 0
                and self.get_page_url() is not None):
            s = self.get_title() + str(self.get_artists())
            s = s + self.get_page_url() + extra
            seed(s)
            self.set_id(prefix + str(randint(1, 9999999999)))

    def set_id(self, id_str: str = None):
        """
        Set the ID for the current DVK file.

        Parameters:
            id_str (str): DVK ID
        """
        if id_str is None:
            self.id = ""
        else:
            self.id = id_str.upper()

    def get_id(self) -> str:
        """
        Return the ID for the current DVK file.

        Returns:
            str: DVK ID
        """
        return self.id.upper()

    def set_title(self, title_str: str = None):
        """
        Set the title for the current DVK file.

        Parameters:
            title_str (str): DVK title
        """
        self.title = title_str

    def get_title(self) -> str:
        """
        Return the title for the current DVK file.

        Returns:
            str: DVK title
        """
        return self.title

    def set_artist(self, artist_str: str = None):
        """
        Set the artists for the current DVK file for just a single artist.

        Parameters:
            artist_str (str): DVK Artist
        """
        a_list = [artist_str]
        self.set_artists(a_list)

    def set_artists(self, artist_list: list = None):
        """
        Set the artists for the current DVK file.

        Parameters:
            artist_list (list): DVK artists
        """
        if artist_list is None:
            self.artists = []
        else:
            self.artists = sorted(clean_list(artist_list))

    def get_artists(self) -> list:
        """
        Return a list of artists for the current DVK file.

        Returns:
            list: DVK artists
        """
        return self.artists

    def set_time_int(
            self,
            year_int: int = 0,
            month_int: int = 0,
            day_int: int = 0,
            hour_int: int = 0,
            minute_int: int = 0):
        """
        Set the Dvk's time published.

        Uses int values representing individual time units.

        Parameters:
            year_int (int): Int value of year published
            month_int (int): Int value of month published
            day_int (int): Int value of day published
            hour_int (int): Int value of hour published
            minute_int (int): Int value of minute published
        """
        if (year_int is None or year_int < 1
                or month_int is None or month_int < 1 or month_int > 12
                or day_int is None or day_int < 1 or day_int > 31
                or hour_int is None or hour_int < 0 or hour_int > 23
                or minute_int is None or minute_int < 0 or minute_int > 59):
            self.time = "0000/00/00|00:00"
        else:
            year_str = extend_int(year_int, 4)
            month_str = extend_int(month_int, 2)
            day_str = extend_int(day_int, 2)
            hour_str = extend_int(hour_int, 2)
            minute_str = extend_int(minute_int, 2)
            date = year_str + "/" + month_str + "/" + day_str
            self.time = date + "|" + hour_str + ":" + minute_str

    def set_time(self, time_str: str = None):
        """
        Set the current Dvk's time published using a formatted time string.

        If time string is invalid, sets the date to 0000/00/00|00:00

        Parameters:
            time_str (str): String representation of time published.
                            Should be formatted: YYYY/MM/DD/hh/mm
        """
        if time_str is None or not len(time_str) == 16:
            self.time = "0000/00/00|00:00"
        else:
            try:
                year = int(time_str[0:4])
                month = int(time_str[5:7])
                day = int(time_str[8:10])
                hour = int(time_str[11:13])
                minute = int(time_str[14:16])
                self.set_time_int(year, month, day, hour, minute)
            except ValueError:
                self.time = "0000/00/00|00:00"

    def get_time(self) -> str:
        """
        Return the time published for the current DVK file.

        Returns:
            str: Time string of the time published for the DVK file
        """
        return self.time

    def set_web_tags(self, web_tag_list: list = None):
        """
        Set the web tags for the current DVK file.

        Parameters:
            web_tag_list (list): DVK web tags
        """
        if web_tag_list is None or web_tag_list == []:
            self.web_tags = None
        else:
            self.web_tags = clean_list(web_tag_list)

    def get_web_tags(self) -> list:
        """
        Return the web tags for the current DVK file.

        Returns:
            list: DVK web tags
        """
        return self.web_tags

    def set_description(self, description_str: str = None):
        """
        Set the description for the current DVK file.

        Parameters:
            description_str (str): DVK description
        """
        if description_str is None or description_str == "":
            self.description = None
        else:
            self.description = add_escapes_to_html(description_str)

    def get_description(self) -> str:
        """
        Return the description for the current DVK file.

        Returns:
            str: DVK description
        """
        return self.description

    def set_page_url(self, page_url_str: str = None):
        """
        Set the page URL for the current DVK file.

        Parameters:
            page_url_str (str): Page URL
        """
        if page_url_str == "":
            self.page_url = None
        else:
            self.page_url = page_url_str

    def get_page_url(self) -> str:
        """
        Return the page URL for the current DVK file.

        Returns:
            str: Page URL
        """
        return self.page_url

    def set_direct_url(self, direct_url_str: str = None):
        """
        Set the direct media URL for the current DVK file.

        Parameters:
            direct_url_str (str): Direct media URL
        """
        if direct_url_str == "":
            self.direct_url = None
        else:
            self.direct_url = direct_url_str

    def get_direct_url(self) -> str:
        """
        Return the direct media URL for the current DVK file.

        Returns:
            str: Direct media URL
        """
        return self.direct_url

    def set_secondary_url(self, secondary_url_str: str = None):
        """
        Set the secondary media URL for the current DVK file.

        Parameters:
            secondary_url_str (str): Secondary media URL
        """
        if secondary_url_str == "":
            self.secondary_url = None
        else:
            self.secondary_url = secondary_url_str

    def get_secondary_url(self) -> str:
        """
        Return the secondary media URL for the current DVK file.

        Returns:
            str: Secondary media URL
        """
        return self.secondary_url

    def set_media_file(self, file_name: str = None):
        """
        Set the media file for the current DVK file based on a given filename.

        Sets file in the same directory as the DVK file.

        Parameters:
            file_name (str): Media filename for the current DVK file
        """
        if file_name is None or file_name == "" or self.get_file() is None:
            self.media_file = None
        else:
            parent = join(self.get_file(), pardir)
            self.media_file = abspath(join(parent, file_name))

    def get_media_file(self) -> str:
        """
        Return the media file for the current DVK file.

        Returns:
            path: DVK media file
        """
        return self.media_file

    def set_secondary_file(self, file_name: str = None):
        """
        Set the secondary media file for the current DVK file.

        Sets file in the same directory as the DVK file.

        Parameters:
            file_name (str): Secondary media filename for the current DVK file
        """
        if file_name is None or file_name == "" or self.get_file() is None:
            self.secondary_file = None
        else:
            parent = join(self.get_file(), pardir)
            self.secondary_file = abspath(join(parent, file_name))

    def get_secondary_file(self) -> str:
        """
        Return the secondary media file for the current DVK file.

        Returns:
            path: DVK secondary media file
        """
        return self.secondary_file
