# -*- coding: utf-8 -*-
"""rhinovid class.

This class contains functions to rename videos.
"""
import pathlib
import sys
from dateutil import parser
import ffmpeg

from .rhinofile import Rhinofile


class Rhinovid(Rhinofile):
    """Class to rename video files.

    Supported types are defined in the `Rhinofile` class.
    """

    counter = 1

    def get_date(self, path: pathlib.PosixPath) -> str:
        """
        Retrieve the date of a video.

        The date is retrieved using `probe` function from the
        `ffmpeg-python` <https://kkroening.github.io/ffmpeg-python/>`_
        package.

        The cast is done using the `parse` function from the
        `dateutil <https://dateutil.readthedocs.io/en/stable/parser.html>`_
        package. All supported format are those from the library and may evolve.

        Parameters
        ----------
        path: pathlib.PosixPath
            Path containing the video to rename.

        Returns
        -------
        str
            Date as a string in the following format: %Y%m%d.
            If date is not found, return 'NoDateFound'.
        """
        meta = ffmpeg.probe(path)
        try:
            date = parser.parse(meta['format']['tags']['creation_time']).strftime('%Y%m%d')
        except ValueError:
            self.logger.error(f'Unable to get date from {path}. Format is probably not supported.',
                              file=sys.stderr)
            date = 'NoDateFound'

        return date

    def rename(self):
        """
        Rename the video file.

        Video are renamed with the given keyword and the date of the video.

        The counter is shared between instances.
        """
        date = self.get_date(self.path)
        new_name = (f'{self.keyword}_{date}_{str(Rhinovid.counter).rjust(self.nb_digits, "0")}'
                    f'{self.path.suffix}')
        new_path = self.path.with_name(new_name)

        if self.lowercase:
            new_path = new_path.with_suffix(new_path.suffix.lower())

        if not new_path.exists():
            if self.backup:
                with new_path.open(mode='xb') as fid:
                    fid.write(self.path.read_bytes())
                self.logger.info(f'Copying {self.path} to {new_path}.')
            else:
                self.path.replace(new_path)
                self.logger.info(f'Renaming {self.path} to {new_path}.')
            Rhinovid.counter += 1
        else:
            self.logger.info(f'Path {new_path} already exists.')

    def __str__(self):
        """String representation of class."""
        return f'Rhinovid: {self.path}'
