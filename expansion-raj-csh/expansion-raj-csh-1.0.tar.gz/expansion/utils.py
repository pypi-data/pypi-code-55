"""This is the utilities module of the expansion package.
    Contains miscellaneous utilities,
    i.e. functions and classes that are not specific to the expansion package.
"""

__version__ = '1.0'
__author__ = 'Rajarshi Mandal'
__all__ = ['Timer',
           'stitch']

import os
import time

import cv2


class Timer:
    """Once instantiated, can be called to time a function.

        Args:
            func (function): Function to be timed.
            print_time (bool): If set to True, the time elapsed will be printed to sys.stdout.
    """
    def __init__(self, func, print_time=False):
        self.func = func
        self.print_time = print_time

        self._result = None
        self._timed = False

    @property
    def result(self):
        """Result of function passed to Timer,
            only accesible once Timer instance
            has been called.

            Raises:
                AttributeError: If accessed before Timer instance has been called.
        """
        if self._timed:
            return self._result

        raise AttributeError('Expansion: Timer.result has not been evaluated yet!')

    def __call__(self, *args, **kwargs):
        """Times a function with an arbitrary number of arguments.

            Args:
                *args: Positional arguments to be passed to the function.
                **kwargs: Keyword arguments to be passed to the function.

            Returns:
                (float): Time elapsed, from before calling the function
                         to after calling the function, in seconds.
        """
        old_time = time.time()
        self._result = self.func(*args, **kwargs)
        new_time = time.time()

        self._timed = True

        time_elapsed = new_time - old_time

        if self.print_time:
            print(f'Expansion: time elapsed: {time_elapsed}!\n')

        return time_elapsed

def stitch(directory, name, fps, dim, f_format):
    """Generates a video in '.avi' or '.mp4' format.
        Uses frames in a directory generated
        by the expansion.callbacks.Sample() callback
        used during ColoredPointHandler.simulate().
        Only accepts PNG files as frames.
        Saves video as dir/name.format

        Args:
            directory (str): Directory of the frames.
            name (str): Desired name of the video.
            fps (int): Desired frame rate of the video.
            dim (iterable)(int): An iterable consisting of two integers,
                                 representing the dimensions of each frame.
            f_format (str): Desired file format of the video, either 'avi' or 'mp4'.
    """
    # pylint: disable=no-member

    seq = []
    for i in range(len(os.listdir(directory))):
        img = cv2.imread(f'{directory}/{i}.png')
        seq.append(img)

    if 'avi' in f_format:
        vid = cv2.VideoWriter(f'{directory}/{name}.avi', cv2.VideoWriter_fourcc(*'XVID'), fps, dim)
    elif 'mp4' in f_format:
        vid = cv2.VideoWriter(f'{directory}/{name}.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, dim)

    for img in seq:
        vid.write(img)

    vid.release()

    # pylint: enable=no-member
