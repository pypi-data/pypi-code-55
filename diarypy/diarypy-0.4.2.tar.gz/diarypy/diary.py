#!/usr/bin/env python
"""Diary to create notebooks and store intermediate results and figures

This class can be used to save the intermediate results of any experiment
run in python. It will create a folder for the specific experiment and
save all the information and images in a structured and sorted manner.
"""
__docformat__ = 'restructedtext en'
import os
import sys
import shutil
import errno
import csv
import json
import datetime
import logging

from diarypy import DESCR_FILENAME
from diarypy import DIARY_VERSION_DELIMITER


def preprocess_row(row):
    if type(row) is dict:
        row = sum([[key, str(value).replace('\n', '\\n')] for key, value in row.items()], [])
    for i, element in enumerate(row):
        if isinstance(element, bool):
            row[i] = 'True' if element else 'False'


def postprocess_row(row):
    for i, element in enumerate(row):
        if isinstance(element, str) and (element in ['True', 'False']):
            row[i] = element == 'True'


class Notebook(object):
    def __init__(self, name, diary, verbose=False, header=None, mode='w'):
        self.name = name
        self.filename = "{}.csv".format(name)
        self.diary = diary
        self.entry_number = 0
        self.verbose = verbose
        self.history = []
        self.mode = mode
        if header is not None:
            with open(os.path.join(self.diary.path, self.filename), 'a') as csvfile:
                writer = csv.writer(csvfile, delimiter=',', quotechar='|',
                                    quoting=csv.QUOTE_NONNUMERIC)
                row = ['id1', 'id2', 'date', 'time'] + header
                writer.writerow(row)

        if mode == 'r':
            self.__load_notebook(name)

    def add_entry(self, row):
        if self.mode == 'r':
            print('Error: Entry not added. This notebook is in read mode only.')
            return

        general_entry_number = self.diary.increase_entry_number()
        self.entry_number += 1
        preprocess_row(row)
        with open(os.path.join(self.diary.path, self.filename), 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='|',
                                quoting=csv.QUOTE_NONNUMERIC)
            now = datetime.datetime.now()
            row = [general_entry_number, self.entry_number,
                    now.date().__str__(),
                   now.time().__str__()] + row
            self.history.append(row)
            writer.writerow(row)
        if self.verbose:
            print(row)

    def __load_notebook(self, name):
        with open(os.path.join(self.path, self.filename), 'r', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|',
                                quoting=csv.QUOTE_NONNUMERIC)
            for row in reader:
                postprocess_row(row)
                self.history.append(row)

    @property
    def path(self):
        return self.diary.path


class Diary(object):

    def __init__(self, name, path='diary', overwrite=False, image_format='png',
                 fig_format='svg', stdout=True, stderr=True, fig_entry=False,
                 mode='w', verbose=False):
        '''
        Parameters
        ==========
        fig_entry : bool
            If True the name of the figure contains the entry number
        '''
        if name is None:
            self.__load_diary(path)
            return

        self.creation_date = datetime.datetime.now()
        self.name = name
        self.root = path
        self.version = 0
        self.overwrite = overwrite
        self.mode = mode
        self.verbose = verbose

        self.image_format = image_format
        self.fig_format = fig_format
        self.entry_number = 0
        self.fig_entry = fig_entry
        self.all_paths = self._create_all_paths(overwrite)
        self._save_description()

        self.red_stdout = stdout
        self.red_stderr = stderr

        if stdout:
            self.redirect_stdout(self.path)
        if stderr:
            self.redirect_stderr(self.path)

        self.notebooks = {}

    def __load_diary(self, path):
        with open(os.path.join(path, DESCR_FILENAME), 'r') as fp:
            all_attributes = json.load(fp)
            for attribute, value in all_attributes.items():
                self.__dict__[attribute] = value
        self.notebooks = self.__load_notebooks()

    def __load_notebooks(self):
        notebooks = {}
        for filename in os.listdir(self.path):
            if filename.endswith(".csv"):
                name = os.path.splitext(filename)[0]
                notebooks[name] = Notebook(name, diary=self, mode='r')
        return notebooks

    @property
    def path(self):
        return '{}{}{}'.format(os.path.join(self.root, self.name),
                               DIARY_VERSION_DELIMITER,
                               self.version)

    @property
    def all_attributes(self):
            return dict(vars(self), path=self.path)

    def redirect_stdout(self, path, filename='stdout.txt'):
        self.original_stdout = sys.stdout
        sys.stdout = open(os.path.join(path, filename), 'w')
        logging.StreamHandler(sys.stdout)

    def redirect_stderr(self, path, filename='stderr.txt'):
        self.original_stderr = sys.stderr
        sys.stderr = open(os.path.join(path, filename), 'w')

    def add_notebook(self, name, **kwargs):
        self.notebooks[name] = Notebook(name, self, **kwargs)
        return self.notebooks[name]

    def _create_all_paths(self, overwrite):
        original_path = self.path
        created = False
        if overwrite and os.path.exists(self.path):
            shutil.rmtree(self.path)
        while not created:
            while os.path.exists(self.path):
                self.version +=1

            self.path_images = os.path.join(self.path, 'images')
            self.path_figures = os.path.join(self.path, 'figures')
            all_paths = [self.path,]
            try:
                os.makedirs(self.path)
                created = True
            except OSError as exception:
                if exception.errno != errno.EEXIST:
                    raise
        return all_paths

    def _save_description(self):
        with open(os.path.join(self.path, DESCR_FILENAME), 'w') as fp:
            if self.verbose:
                print("Saving :\n{}".format(self))
            json.dump(self.__dict__, fp, indent=1, default=str)

    def add_entry(self, notebook_name, row):
        self.notebooks[notebook_name].add_entry(row)

    def increase_entry_number(self):
        self.entry_number += 1
        return self.entry_number

    def save_image(self, image, filename='', extension=None):
        if self.path_images not in self.all_paths:
            try:
                os.makedirs(self.path_images)
            except OSError as exception:
                if exception.errno != errno.EEXIST:
                    raise
            self.all_paths.append(self.path_images)
        if extension == None:
            extension = self.image_format
        image.save(os.path.join(self.path_images,
                                "{}_{}.{}".format(filename, self.entry_number,
                                                  extension)))

    # TODO add support to matplotlib.pyplot.figure or add an additional
    # function
    def save_figure(self, fig, filename=None, extension=None):
        if self.path_figures not in self.all_paths:
            try:
                os.makedirs(self.path_figures)
            except OSError as exception:
                if exception.errno != errno.EEXIST:
                    raise
            self.all_paths.append(self.path_figures)
        if extension == None:
            extension = self.fig_format
        fig.tight_layout()
        if filename is None:
            filename = fig.get_label()

        if self.fig_entry:
            filename = "{}_{}.{}".format(filename, self.entry_number, extension)
        else:
            filename = "{}.{}".format(filename, extension)

        fig.savefig(os.path.join(self.path_figures, filename))

    def __str__(self):
        return json.dumps(self.all_attributes, indent=1, default=str,
                          sort_keys=True)

    def get_shared_vars(self):
        s_vars = vars(self)
        s_vars['notebooks'] = {}
        return s_vars

    def set_shared_vars(self, s_vars):
        for key, value in s_vars.items():
            self.__dict__[key] = value

    def __del__(self):
        if hasattr(self, 'red_stdout') and self.red_stdout:
            sys.stdout.close()
            sys.stdout = self.original_stdout
        if hasattr(self, 'red_stderr') and self.red_stderr:
            sys.stderr.close()
            sys.stderr = self.original_stderr


class SharedDiary(Diary):
    def __init__(self, s_vars, unique_id):
        self.set_shared_vars(s_vars)
        self.creation_date = datetime.datetime.now()
        self.uid = unique_id

        if self.stdout:
            self.redirect_stdout(self.path, 'stdout_uid_{}.txt'.format(self.uid))
        if self.stderr:
            self.redirect_stderr(self.path, 'stderr_uid_{}.txt'.format(self.uid))

    def add_notebook(self, name, **kwargs):
        name = '{}_uid_{}'.format(name, self.uid)
        return super(SharedDiary, self).add_notebook(name, **kwargs)


if __name__ == "__main__":
    diary = Diary(name='world', path='hello', overwrite=False)

    diary.add_notebook('validation')
    diary.add_notebook('test')

    diary.add_entry('validation', ['accuracy', 0.3])
    diary.add_entry('validation', ['accuracy', 0.5])
    diary.add_entry('validation', ['accuracy', 0.9])
    diary.add_entry('test', ['First test went wrong', 0.345, 'label_1'])

    try:
        import PIL.Image as Image
    except ImportError:
        import Image

    image = Image.new(mode="1", size=(16,16), color=0)
    diary.save_image(image, filename='test_results')
