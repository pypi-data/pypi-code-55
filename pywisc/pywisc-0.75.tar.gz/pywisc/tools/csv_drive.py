"""
Nomenclador para hospitales públicos de gestión descentralizada de Argentina
"""
import csv
import json
import logging
import os
import requests


logger = logging.getLogger(__name__)


class DriveCSV:

    def __init__(self, name, unique_id_column, uid, gid, force_re_download=False):
        """ starts with Unique Doc ID and page/tab ID """
        self.name = name
        self.unique_id_column = unique_id_column
        self.uid = uid
        self.gid = gid
        self.url_csv = f'https://docs.google.com/spreadsheets/d/{uid}/export?format=csv&gid={gid}'
        # download if not exists
        here = os.path.dirname(os.path.realpath(__file__))
        self.data_folder = os.path.join(here, 'tmpdata')
        self.local_csv = os.path.join(self.data_folder, f'{name}.csv')
        if force_re_download or not os.path.isfile(self.local_csv):
            self.download()
        self.read_csv()
    
    def download(self):
        logger.info(f'Downloading from {self.url_csv}')
        req = requests.get(self.url_csv)
        if not os.path.isdir(self.data_folder):
            os.mkdir(self.data_folder)
        f = open(self.local_csv, 'wb')
        f.write(req.content)
        f.close()

    def read_csv(self):
        # read CSV and transfor to a useful JSON
        tree = []   # results
        f = open(self.local_csv, 'r')
        reader = csv.DictReader(f)
        
        for row in reader:
            logger.info(f'Reading row {row}')
            
            # uid = row[self.unique_id_column]
            new_row = {}
            for k, v in row.items():
                new_row[k] = v.strip()

            tree.append(new_row)

        f.close()

        self.tree = tree
        return tree
