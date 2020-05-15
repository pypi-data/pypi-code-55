from time import time
from decorator import decorator
import logging


def timer_decorator(timer=None, tag=None, force_verbose=False):
    """

    :param timer:
    :param tag:
    :param force_verbose:
    :return:
    """
    if timer is None:
        timer = Timer()

    @decorator  # trick in order to propagate to the decorated function the docstring & signature of original function
    def with_timer_decorator(__func, *args, **kwargs):
        _verbose = force_verbose
        if not _verbose and 'verbose' in kwargs:
            _verbose = kwargs['verbose']
        timer.tic(tag)
        out = __func(*args, **kwargs)
        timer.toc(tag)
        if _verbose:
            print("[{}] Elapsed time: {:.04f} s".format(__func.__name__, timer.get_elapsed(tag)))
        logging.info('%s took %d seconds', __func.__name__, timer.get_elapsed(tag))
        return out

    return with_timer_decorator


class Timer(object):

    def __init__(self):
        self._origin = time()
        self._time = dict()
        self._key = -1
        self._tag_lut = dict()
        self._reverse_tag_lut = dict()
        self._tic_lut = dict()
        self._toc_lut = dict()

    def _get_key(self, key):
        return self._reverse_tag_lut[key] if key in self._reverse_tag_lut else None

    def _get_time(self, _key):
        return self._time[_key]

    def get_time(self, key):
        return self._time[key] if isinstance(key, int) else self._time[self._get_key(key)]

    def _get_keys(self):
        return self._time.keys()

    def get_landmarks(self):
        return {k: v for k, v in self._tag_lut.items() if k in self._time.keys()}

    def get_all_tic_toc(self):
        return {tag: self.get_elapsed(tag) for tag in self._toc_lut.keys()}

    def get_elapsed(self, *args):
        assert len(args) < 3
        if len(args) < 2:
            if len(args) == 0:
                # tic/toc without arguments
                assert None in self._toc_lut, "Error: {0}.get_elapsed() method called with no arguments should be " \
                                              "used only after using {0}.tic/toc() methods before.".format(type(self))
                tag = None
            else:
                tag = args[0]
                assert tag in self._toc_lut, "Error: {0}.get_elapsed(<tag>) method called with one argument should " \
                                             "be used only after using {0}.tic/toc(<tag>) methods before." \
                                             "".format(type(self))
            return self.get_elapsed(self._tic_lut[tag], self._toc_lut[tag])
        # key_start / key_end arguments
        key_start = args[0]
        key_end = args[1]
        return self.get_time(key_end) - self.get_time(key_start)

    def time(self, tag=None):
        self._key += 1
        self._time[self._key] = time()
        self._tag_lut[self._key] = tag
        if tag is not None:
            assert isinstance(tag, str), "Error: {}.time(<tag>) method only takes None or str type for parameter " \
                                         "<tag>.".format(type(self))
            self._reverse_tag_lut[tag] = self._key
        return self._key

    def tic(self, tag=None):
        self._tic_lut[tag] = self.time(None if tag is None else str(tag) + '_tic')

    def toc(self, tag=None):
        self._toc_lut[tag] = self.time(None if tag is None else str(tag) + '_toc')
        assert tag in self._tic_lut, "Error: {0}.toc(<tag>) method should be used only after having used " \
                                     "{0}.tic(<tag>) method before.".format(type(self))
        return self.get_elapsed(self._tic_lut[tag], self._toc_lut[tag])

    def __str__(self):
        string = "Timer(\n"
        string += "  {:25s}  {} s\n".format("origin:", self._origin)
        string += "  Landmarks:\n"
        for k in self._get_keys():
            _elapsed = self._get_time(k) - self._origin
            tag = self._tag_lut[k]
            if tag is None:
                string += "    {:25s}{} s\n".format("[{}]:".format(k), _elapsed)
            else:
                string += "    {:25s}{} s\n".format("[{}]({}):".format(k, str(tag)[-12:]), _elapsed)
        if self._toc_lut:
            string += "  Tic / Toc elapsed times:\n"
            for tag in self._toc_lut.keys():
                string += "    {:25s}{:.5f} s\n".format("({}):".format("" if tag is None else str(tag)),
                                                        self.get_elapsed(tag))
        string += ")\n"
        return string


def main():
    T = Timer()
    T.tic()
    T.time()
    T.time("yop")
    T.time("56")
    T.tic("hey")
    T.time()
    T.time("non")
    T.time("oui")
    T.time("non")
    T.time()
    print("hey ", T.toc("hey"))
    T.time()
    print(T)
    print(" ", T.toc())


if __name__ == "__main__":
    main()
