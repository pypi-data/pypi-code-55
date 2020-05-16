import yaml
import six
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


REGISTRY = dict()

KEYWORDS = ['procspec_version']

class Processor:
    def __init__(self):
        self.input_keys = None
        self.def_output_key = None
        self.procs = []

    def __call__(self, args, output_key=None):
        if self.input_keys is not None:
            input_args = None
        else:
            input_args = args
        for proc in self.procs:
            # each proc is modifying the input args
            v = proc(input_args)

        if output_key is None:
            output_key = self.def_output_key
        if output_key is not None:
            args[output_key] = v

        return v

def register_proc(name):
    def register_fn(cls):
        if name in KEYWORDS:
            raise Exception(f"'{name}' is a procspec keyword")
        REGISTRY[name] = cls
        return cls
    return register_fn

#TODO: support multiple output keys()

def parse_proc(spec_str=None, yaml_path=None, default_output=None):
    if spec_str is not None and yaml_path is not None or \
            spec_str is None and yaml_path is None:
        raise Exception("'parse_prco' takes one parameter -- "
                "either 'spec_str' or 'yaml_path'")
    if spec_str is None:
        with open(yaml_path, 'r') as f:
            spec = yaml.load(f, Loader=Loader)
    else:
        spec = yaml.load(spec_str, Loader=Loader)

    return _parse_proc(spec, default_output)

def _parse_proc(spec, default_output):
    if isinstance(spec, list):
        if isinstance(spec, str):
            if len(spec.keys()) != 1:
                raise Exception(f"{spec} is not a propper processor specification")
        proc = Processor()
        for ps in spec:
            proc.procs.append(_parse_proc(ps, default_output))

    elif isinstance(spec, dict):
        if len(spec.keys()) != 1:
            raise Exception(f"{spec} is not a propper processor specification")

        proc_type_name = list(spec.keys())[0]
        if proc_type_name not in REGISTRY:
            raise Exception(f"Processor type {proc_type_name} is not registered")
        proc_type = REGISTRY[proc_type_name]

        proc_def = spec[proc_type_name]
        if not isinstance(proc_def, dict):
            raise Exception(f"definition {proc_def} is not a propper definition "
                    "for processor {proc_type_name}")

        proc = Processor()

        if 'input_keys' in proc_def:
            proc.input_keys = proc_def['input_keys']
            del proc_def['input_keys']
        if 'output_key' in proc_def:
            proc.output_key = proc_def['output_key']
            del proc_def['output_key']
        else:
            proc.output_key = default_output

        params = {}
        if 'params' in proc_def:
            params = _parse_proc_params(proc_def['params'], default_output=default_output)
            del proc_def['params']

        proc.procs.append(proc_type(**params))

        if len(proc_def.keys()) != 0:
            raise Exception(f"Unkonwn arguments {proc_def.keys()} in specification "
                    "of {proc_type_name}")
    else:
        raise Exception(f"{spec} is not a propper processor specification")

    return proc

def parse_proc_params(params, default_output):
    if not isinstance(params, dict):
        raise Exception(f"{params} is not a propper parameter specification "
                "of {proc_type_name}")
    return _parse_proc_params(params, default_output)

def _parse_proc_params(params, default_output):
    if not isinstance(params, dict):
        return params

    for k, v in list(six.iteritems(params)):
        if k.startswith('procspec_'):
            new_k = k[len('procspec_'):]
            new_v = _parse_proc(v, default_output)
            params[new_k] = new_v
            del params[k]
        elif isinstance(v, dict):
            new_v = _parse_proc_params(v, default_output)
            params[k] = new_v
        elif isinstance(v, list) and not isinstance(v, str):
            new_v = [_parse_proc_params(i, default_output) for i in v]
            params[k] = new_v

    return params


