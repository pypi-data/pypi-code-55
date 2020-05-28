#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pickle

from datetime import datetime

class Zettelkasten:

    def __init__(self, path):
        ''' Initializes the Zettelkasten object. '''

        self.path = os.path.expanduser(path)
        self.path_root = os.path.join(self.path, '.nik')
        self.path_index = os.path.join(self.path_root, 'index')
        self.supported = (('markdown', '.md'), ('org-mode', '.org'), ('ascii-doc', '.adoc'))

        # Initalize directory as Zettelkasten directory if necessary
        if not os.path.exists(self.path_root):
            self.init()

        # Try to deserialize the index from disk, otherwise create a new index
        if os.path.exists(self.path_index):
            self.index = ZettelkastenIndex.load(self.path_index)
        else:
            # Rescan and create a new index
            self.index = self.update()

        # If modification time of Zettelkasten folder changed, then files were added or deleted.
        if self.index < os.path.getmtime(self.path):
            # We need to rescan and create a new index
            self.index = self.update()

    def __str__(self):
        short = self.path.replace(os.getenv('HOME', ''), '~')
        return f'Zettelkasten <{short}>'

    def init(self):
        ''' Initializes an empty directory as Zettelkasten directory. '''

        # Create necessary directories if they do not yet exist
        root = os.path.join(self.path, '.nik')
        os.makedirs(root, exist_ok = True)
        html = os.path.join(root, 'html')
        os.makedirs(html, exist_ok = True)

    def update(self):
        ''' Performs a full scan, updates the index and saves it to disk. '''

        # Scan the entire directory for relevant files
        files, timestamp = self.scan()
        # Update the Zettelkasten index
        self.index = ZettelkastenIndex(self.path_index, files, timestamp)
        # Write index to disk
        self.index.save()

        return self.index

    def scan(self):
        ''' Scans the entire Zettelkasten directory for (new) files. '''

        print('scan()')

        files = []
        # Remember the timestamp
        timestamp = datetime.now().timestamp()

        for entry in os.scandir(self.path):

            # Skip directories
            if entry.is_dir():
                continue

            # That leaves us with files and symlinks...
            # @TODO: How to deal with symlinks?

            # Check if we have to deal with this file or not
            for f, ending in self.supported:
                if entry.name.endswith(ending):
                    break
            else:
                # Format not supported
                continue

            # Read out last modification timestamp (mtime on UNIX)
            mtime = entry.stat().st_mtime
            files.append((entry.name, entry.path, f, mtime))

        # Update the Zettelkasten index
        self.index = ZettelkastenIndex(self.path_index, files, timestamp)
        # Write index to disk
        self.index.save()

        return files, timestamp

class ZettelkastenIndex:
    ''' The index contains a tuple with all known (and relevant) files together with their last modification timestamp (mtime). '''

    def __init__(self, path, files = [], timestamp = None):
        ''' Initializes the ZettelkastenIndex object. '''

        self.path = os.path.expanduser(path)
        self.files = files
        self.timestamp = timestamp or datetime.now().timestamp()

    def __eq__(self, other):
        return self.timestamp == other

    def __gt__(self, other):
        return self.timestamp > other

    def __lt__(self, other):
        return not self.__gt__(other)

    def save(self):
        ''' Serializes all index metadata within the Zettelkasten to disk. '''

        with open(self.path, 'w+b') as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, path):
        ''' Deserializes all index metadata from disk and returns ZettelkastenIndex object. '''

        if os.path.exists(path):
            with open(path, 'rb') as f:
                return pickle.load(f)
