import sys
from CallOnce.Enums import ArgumentsMode, HashFunction, StorageMode
from functools import wraps

from CallOnce.ResultContainer import ResultContainer

if sys.version_info < (3, 4):
    raise Exception("Must be using Python 3.4")


class CallOnce(object):
    def __init__(self,
                 ttl=None,
                 args_mode=ArgumentsMode.IGNORE,
                 hash_mode=HashFunction.PYTHON,
                 storage_mode=StorageMode.Memory):
        self.args_mode = args_mode
        self.hash_mode = hash_mode
        self.storage_mode = storage_mode
        self.ttl = ttl
        self.cache = {}
        #if storage_mode == StorageMode.Disk:
        #    raise NotImplementedError()


    @classmethod
    def reset_persistent_storage(cls):
        print("ssss")

    @staticmethod
    def _get_object_instance(target, *args):
        if len(args) == 0:
            return None
        method = getattr(args[0], target.__name__, None)
        if not callable(method):
            return None
        return args[0] if id(method.__wrapped__) == id(target) else None

    def _compute_args_hash(self, *args, **kwargs):
        if self.args_mode == ArgumentsMode.IGNORE:
            return None
        import pickle
        serialised_data = pickle.dumps((args, kwargs))

        hash_function = hash
        if self.hash_mode == HashFunction.MD5:
            import hashlib

            def hash_md5(arg):
                m = hashlib.md5()
                m.update(arg)
                return m.digest()
            hash_function = hash_md5

        return hash_function(serialised_data)

    def _get_key(self, target, *args, **kwargs):
        obj = self._get_object_instance(target, *args)
        args_hash = self._compute_args_hash(*args, **kwargs)
        return id(target), id(obj), args_hash

    def _get_value(self, key, bound_f):
        if key not in self.cache:
            result_value = bound_f()
            self.cache[key] = ResultContainer(result_value)

        container = self.cache[key]
        if not container.check_if_valid_ttl(self.ttl):
            container = ResultContainer(bound_f())
            self.cache[key] = container

        return container.get_value()

    def __call__(self, target):
        @wraps(target)
        def wrapped_decorator(*args, **kwargs):
            key = self._get_key(target, *args, **kwargs)
            from functools import partial
            bound_f = partial(target, *args, **kwargs)
            return self._get_value(key, bound_f)
        return wrapped_decorator






