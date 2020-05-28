from copy import copy, deepcopy
import logging

log = logging.getLogger(__name__)


class dotdict(dict):
    """ dot.notation access to dictionary attributes
    useful mostly as a shortcut in notebooks or when setting parameters

    .. warning:: can cause issues where a dict is expected e.g. pd.DataFrame.from_dict does not work
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.convert_dicts()

    def __delattr__(self, k):
        del self[k]

    def __setattr__(self, k, v):
        self[k] = v

    def __getattr__(self, k):
        try:
            return self[k]
        except KeyError:
            # enable hasattr to return False
            raise AttributeError

    def copy(self):
        """ return a dotdict rather than a dict """
        return dotdict(super().copy())

    def convert_dicts(self):
        """ recursively convert dicts to dotdict
        """
        for k, v in self.items():
            if isinstance(v, dict) and not isinstance(v, dotdict):
                self[k] = dotdict(v)

    def to_dict(self):
        """ recursively convert dotdict to dict
        :return: dict
        """
        out = dict(self)
        for k, v in out.items():
            if isinstance(v, dotdict):
                out[k] = v.to_dict()
        return out

    def __getstate__(self):
        """ dict version undefined. required for pickle. note __dict__ is not used. """
        pass

    def __setstate__(self, d):
        """ dict version undefined. required for pickle. note __dict__ is not used. """
        pass


class autodict(dotdict):
    """ dotdict that automatically creates missing_params hierarchy of autodicts

    .. warning::
        This is convenient but can hide bugs so use sparingly

    .. note::
        hasattr will create the attribute and return true. to test if key exists use "in" operator.
    """

    def __getattr__(self, k):
        """ automatically create nested dotdict if item does not exist """
        # calling super methods avoids recursion errors
        try:
            return super().__getitem__(k)
        except KeyError:
            # ipython uses this to check if methods exist. reraise as we don't want to add it as a key.
            if k == "_ipython_canary_method_should_not_exist_":
                raise
            log.warning(f"missing_params key added automatically {k}")
            super().__setitem__(k, type(self)())
            return super().__getitem__(k)

    # for obj[index] automatically create nested autodict if item does not exist
    __getitem__ = __getattr__

    def __deepcopy__(self, x):
        """ dict version undefined so causes recursion. Not sure how to implement but don't need it """
        raise NotImplementedError(self)
