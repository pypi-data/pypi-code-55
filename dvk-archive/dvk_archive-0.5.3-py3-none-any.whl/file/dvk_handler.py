#!/usr/bin/env python3

"""Handles Dvk objects within given directory and sub-directories."""

from os import walk
from _functools import cmp_to_key
from os import listdir
from os.path import abspath, isdir
from tqdm import tqdm
from dvk_archive.file.dvk import Dvk
from dvk_archive.file.dvk_directory import DvkDirectory
from dvk_archive.processing.list_processing import clean_list
from dvk_archive.processing.list_processing import list_to_string
from dvk_archive.processing.string_compare import compare_strings
from dvk_archive.processing.string_compare import compare_alphanum


class DvkHandler:
    """
    Handle Dvk objects for given directories and their sub-directories.

    Attributes:
        dvk_directories (list): Loaded Dvk objects
        sorted (list): List of direct indexes to Dvks in a sorted order
    """

    def __init__(self):
        """Initialize DvkHandler attributes."""
        self.dvks = []
        self.sorted = []
        self.paths = []

    def get_paths(self) -> list:
        """
        Return list of paths loaded in the DvkHandler.

        Returns:
            list: List of pathlib paths
        """
        return self.paths

    def load_dvks(self, directory_strs: list = None):
        """
        Load DVK files from a given directory and sub-directories.

        Parameters:
            directory_strs (list): Directories from which to load DVK files
        """
        self.dvks = []
        self.paths = self.get_directories(directory_strs)
        print("Loading DVK Files:")
        for path in tqdm(self.paths):
            dvk_directory = DvkDirectory()
            dvk_directory.read_dvks(abspath(path))
            self.dvks.extend(dvk_directory.dvks)
        self.reset_sorted()

    def reset_sorted(self):
        """Reset the sorted list to the default order."""
        self.sorted = []
        size = len(self.dvks)
        for i in range(0, size):
            self.sorted.append(i)

    def get_size(self) -> int:
        """
        Return the number of DVK files loaded / size of sorted list.

        Returns:
            int: Number of DVK files loaded
        """
        return len(self.dvks)

    def get_dvk_sorted(self, index_int: int = -1) -> Dvk:
        """
        Return the Dvk object for a given index in the sorted index list.

        Parameters:
            index_int (int): Sorted index

        Returns:
            Dvk: Dvk object for the given index
        """
        if index_int > -1 and index_int < self.get_size():
            return self.get_dvk_direct(self.sorted[index_int])
        return Dvk()

    def get_dvk_direct(self, index_int: int = -1) -> Dvk:
        """
        Return the Dvk object for a given direct index.

        Parameters:
            index_int (int): Direct index

        Returns:
            Dvk: Dvk object for the given index
        """
        if index_int > -1 and index_int < self.get_size():
            return self.dvks[index_int]
        return Dvk()

    def get_directories(self, directory_strs: list = None) -> list:
        """
        Return a list of directories and sub-directories in a given file path.

        Parameters:
            directory_strs (list): Directories to search within

        Returns:
            list: Internal directories in the form of path strings
        """
        if directory_strs is None or len(directory_strs) < 1:
            return []
        paths = []
        for d in directory_strs:
            if d is not None and not d == "":
                directory_path = abspath(d)
                for p in walk(directory_path):
                    dir = abspath(p[0])
                    add = False
                    for file in listdir(dir):
                        if str(file).endswith(".dvk"):
                            add = True
                            break
                    if add:
                        paths.append(dir)
        single_path = abspath(directory_strs[0])
        return_list = []
        if isdir(single_path):
            return_list.append(single_path)
        return_list.extend(paths)
        return_list = sorted(clean_list(return_list))
        return return_list

    def contains_page_url(self, url: str = None) -> bool:
        """
        Return whether dvk list contains a given page URL.

        Parameters:
            url (str): Page URL to search for

        Returns:
            bool: Whether dvk list contains page_url
        """
        if url is not None:
            size = self.get_size()
            for i in range(0, size):
                if str(self.get_dvk_direct(i).get_page_url()) == str(url):
                    return True
        return False

    def contains_direct_url(self, url: str = None) -> bool:
        """
        Return whether dvk list contains a given direce URL.

        Parameters:
            url (str): Direct URL to search for

        Returns:
            bool: Whether dvk list contains direct_url
        """
        if url is not None:
            size = self.get_size()
            for i in range(0, size):
                if str(self.get_dvk_direct(i).get_direct_url()) == str(url):
                    return True
        return False

    def contains_id(self, id: str = None) -> bool:
        """
        Return whether dvk list contains a given ID.

        Parameters:
            id (str):ID to search for

        Returns:
            bool: Whether dvk list contains ID
        """
        if id is not None:
            size = self.get_size()
            for i in range(0, size):
                if str(self.get_dvk_direct(i).get_id()) == str(id):
                    return True
        return False

    def add_dvk(self, dvk: Dvk = None):
        """Add a Dvk object to the handler's list of Dvk objects."""
        if dvk is not None:
            self.dvks.append(dvk)

    def sort_dvks(
            self,
            sort_type: str = None,
            group_artists_bool: bool = False):
        """
        Sort all currently loaded DVK objects in dvks list.

        Parameters:
            sort_type (str): Sort type
                ("t": Time, "r": Ratings, "v": Views, "a": Alpha-numeric)
            group_artists_bool (bool): Whether to group DVKs of the same artist
        """
        print("Sorting DVK files...")
        self.group_artists = group_artists_bool
        if sort_type is not None and self.get_size() > 0:
            if sort_type == "t":
                comparator = cmp_to_key(self.compare_time)
            else:
                comparator = cmp_to_key(self.compare_alpha)
            self.dvks = sorted(self.dvks, key=comparator)

    def compare_alpha(self, x: Dvk = None, y: Dvk = None) -> int:
        """
        Compare two DVK objects alpha-numerically by their titles.

        Parameters:
            x (Dvk): 1st Dvk object to compare
            y (Dvk): 2nd Dvk object to compare

        Returns:
            int: Which Dvk should come first.
                -1 for x, 1 for y, 0 for indeterminate
        """
        if x is None or y is None:
            return 0
        result = 0
        if self.group_artists:
            result = self.compare_artists(x, y)
        if result == 0:
            result = compare_alphanum(x.get_title(), y.get_title())
        if result == 0:
            return compare_strings(x.get_time(), y.get_time())
        return result

    def compare_time(self, x: Dvk = None, y: Dvk = None) -> int:
        """
        Compare two DVK objects by their publication time.

        Parameters:
            x (Dvk): 1st Dvk object to compare
            y (Dvk): 2nd Dvk object to compare

        Returns:
            int: Which Dvk should come first.
                -1 for x, 1 for y, 0 for indeterminate
        """
        if x is None or y is None:
            return 0
        result = 0
        if self.group_artists:
            result = self.compare_artists(x, y)
        if result == 0:
            result = compare_strings(x.get_time(), y.get_time())
        if result == 0:
            return compare_alphanum(x.get_title(), y.get_title())
        return result

    def compare_artists(self, x: Dvk = None, y: Dvk = None) -> int:
        """
        Compare two DVK objects by their artists.

        Parameters:
            x (Dvk): 1st Dvk object to compare
            y (Dvk): 2nd Dvk object to compare

        Returns:
            int: Which Dvk should come first.
                -1 for x, 1 for y, 0 for indeterminate
        """
        x_artists = list_to_string(x.get_artists())
        y_artists = list_to_string(y.get_artists())
        return compare_alphanum(x_artists, y_artists)
