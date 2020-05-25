from collections import defaultdict, deque
from copy import deepcopy
from functools import partial, wraps
from inspect import Signature, signature
from itertools import repeat

from dash.dependencies import Input, Output, State


class Callback(object):
    def __init__(
        self,
        func,
        pre_func_hooks=None,
        post_func_hooks=None,
        inputs=None,
        outputs=None,
        states=None,
        to_api=True,
        tee=False,
    ):
        self.dash_inputs = self._to_dash(inputs, Input) or []
        self.dash_outputs = self._to_dash(outputs, Output) or []
        self.dash_states = self._to_dash(states, State) or []

        self._pre_function_hooks = pre_func_hooks or []
        self._post_function_hooks = post_func_hooks or []
        self.to_api = to_api
        self.current_inputs = []
        self.func = func
        self.is_provider = defaultdict(bool)
        self.tee = tee

    def unpack(self, f, args):
        if isinstance(args, tuple):
            return f(*args)
        return f(args)

    def pre_function_hook(self, inputs):
        for f in self._pre_function_hooks:
            inputs = self.unpack(partial(f, self), inputs)

        self.current_inputs = inputs
        return inputs

    def post_function_hook(self, outputs):
        for f in self._post_function_hooks:
            outputs = self.unpack(partial(f, self), outputs)

        return outputs

    def run(self, *inputs):
        if self._pre_function_hooks:
            function_inputs = self.pre_function_hook(inputs)
        else:
            function_inputs = inputs

        function_output = self.unpack(self.func, function_inputs)
        if self._post_function_hooks:
            return self.unpack(self.post_function_hook, function_output)

        if self.tee:
            return tuple(repeat(function_output, len(self.dash_outputs)))

        return function_output

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def register(self, outputs, inputs, states):
        self.set_inputs(inputs)
        self.set_outputs(outputs)
        self.set_states(states)

    def to(self, component, copy=False, **kwargs):
        if copy:
            callback = deepcopy(self)
        else:
            callback = self

        component.register_callback(callback, **kwargs)
        return callback

    def _from_dash(self, obj, **kwargs):
        if isinstance(obj, list):
            return [
                (
                    o.component_id.format(**kwargs),
                    o.component_property.format(**kwargs),
                )
                for o in obj
            ]
        return (
            obj.component_id.format(**kwargs),
            obj.component_property.format(**kwargs),
        )

    def _to_dash(self, obj, dash_type):
        if obj is None:
            return []

        if isinstance(obj, list):
            return [dash_type(id, prop) for id, prop in obj]

        return dash_type(obj[0], obj[1])

    def _format(self, **kwargs):
        self.dash_inputs = self._to_dash(
            self._from_dash(self.dash_inputs, **kwargs), Input
        )
        self.dash_outputs = self._to_dash(
            self._from_dash(self.dash_outputs, **kwargs), Output
        )
        self.dash_states = self._to_dash(
            self._from_dash(self.dash_states, **kwargs), State
        )

    def prepend_input(self, input):
        if isinstance(self.dash_inputs, Input):
            self.dash_inputs = [Input(input[0], input[1]), self.dash_inputs]
        else:
            self.dash_inputs.insert(0, Input(input[0], input[1]))

    def add_inputs(self, inputs):
        if inputs is not None:
            self.dash_inputs += [Input(id, prop) for id, prop in inputs]
        return self

    def set_inputs(self, inputs):
        if inputs is not None:
            self.dash_inputs = self._to_dash(inputs, Input)
        return self

    def add_outputs(self, outputs):
        if outputs is not None:
            new_outputs = [Output(id, prop) for id, prop in outputs]
            if isinstance(self.dash_outputs, list):
                self.dash_outputs += new_outputs
            else:
                self.dash_outputs = [self.dash_outputs] + new_outputs
        return self

    def set_outputs(self, outputs):
        if outputs is not None:
            self.dash_outputs = self._to_dash(outputs, Output)
        return self

    def add_states(self, states):
        if states is not None:
            self.dash_states += [State(id, prop) for id, prop in states]
        return self

    def set_states(self, states):
        if states is not None:
            self.dash_states = self._to_dash(states, State)
        return self

    def add_figure_output(self, figure):
        figure.register_callback(self)
        return self

    def add_storage_output(self, storage, key=None, copy=False):
        if copy:
            callback = deepcopy(self)
        else:
            callback = self

        storage.add_provider(callback, key)
        return callback

    def use_storage_inputs(self, storage, *keys, copy=False, unpack_args=False):
        if copy:
            callback = deepcopy(self)
        else:
            callback = self

        keys = keys or storage.keys

        self.dash_inputs = [Input(storage.id, f"trigger-{key}") for key in keys]
        self.dependencies = keys or []
        storage.add_client(callback, unpack_args)

        return callback

    def register_api(self, app):
        app.callbacks.add(self)

    @property
    def description(self):
        return {
            "name": self.name,
            "parameters": self.parameters,
            "docstring": self.func.__doc__,
            "return_type": self.return_type,
        }

    @property
    def name(self):
        return self.func.__name__

    @property
    def parameters(self):
        sig = signature(self.func)
        params = []
        for name, param in sig.parameters.items():
            param_doc = {"name": name}
            if param.annotation is not param.empty:
                param_doc["type"] = str(param.annotation)
            if param.default is not param.empty:
                param_doc["default"] = param.default

            params.append(param_doc)

        return params

    @property
    def return_type(self):
        t = signature(self.func).return_annotation
        if t != Signature.empty:
            return t
        return


def as_callback(
    *mixins,
    pre_func_hooks=None,
    post_func_hooks=None,
    inputs=None,
    outputs=None,
    states=None,
    to_api=True,
    tee=False,
):
    def wrapper(func, *args, **kwargs):
        @wraps(func)
        def inner(*args, **kwargs):
            return func(*args, **kwargs)

        class NewCallback(Callback, *mixins):
            pass

        return NewCallback(
            inner,
            pre_func_hooks=pre_func_hooks,
            post_func_hooks=post_func_hooks,
            inputs=inputs,
            outputs=outputs,
            states=states,
            to_api=to_api,
            tee=tee,
        )

    return wrapper
