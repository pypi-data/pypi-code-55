import codecs
import os
import pickle
from collections import deque
from datetime import datetime
from tempfile import TemporaryDirectory, TemporaryFile
from uuid import uuid4
from typing import Iterable

from dash.dependencies import Input, Output
from dash_html_components import Div
from dash_infra.core import Callback, Component, as_callback
from flask import current_app as app
from flask import request


class Storage(Component):
    """
    A storage component modifies a callback so
    it writes into a single serialized dictionary.
    This dictionary (state) has one key per registered
    callback, storing the output of the callback.
    """

    def __init__(self, id: str, use_inner_store=False):
        super().__init__(id)
        self.use_inner_store = use_inner_store
        self.keys = []
        self.clients = []
        self.providers = []

    def layout(self):
        return Div(id=self.id)

    def _serializer(self, client_id: str, callback_id: str, *outputs):
        """
        Serializes the result of a provider callback to the store.
        """
        raise NotImplementedError

    def _deserializer(self, client_id, trigger_keys, states):
        """
        Deserializes the store as an input to a client callback.
        """
        raise NotImplementedError

    def _trigger(self):
        """
        Generates a random string triggering the dependant callbacks.
        """
        return str(uuid4())

    def serializer(self, client_id: str, callback_id: str, *outputs):
        if not outputs:
            outputs = ""

        return self._serializer(client_id, callback_id, *outputs)

    def add_provider(self, callback: Callback, copy=False):
        """
        Registers a callback as a provider to the store.
        It first creates a pre-hook that stores the client ID into the callback state.
        It then creates a post-hook that injects the store's serializer into the callback.
        """
        callback.is_provider[self.id] = True

        def pre_hook(state, client_id, *inputs):
            state.client_id = client_id
            return inputs

        def post_hook(state, callback_output):
            if callback_output is not None:
                return self.serializer(state.client_id, callback.name, callback_output)
            else:
                return {}

        callback._pre_function_hooks.insert(0, pre_hook)
        callback._post_function_hooks.append(post_hook)
        self.providers.append(callback)

        return callback

    def _add_store_prehook(self, callback: Callback):
        """
        Registers a callback as a client to the store.
        It injects a pre-hook that deserializes the content
        of the store as an additional input to the callback.
        """
        if not callback.is_provider[self.id]:

            def pre_hook(s, client_id, *triggers_states_inputs):
                num_triggers = len(callback.dependencies)
                trigger_keys = callback.dependencies

                if self.use_inner_store:
                    states = triggers_states_inputs[num_triggers : 2 * num_triggers]
                    other_inputs = triggers_states_inputs[2 * num_triggers :]
                else:
                    states = []
                    other_inputs = triggers_states_inputs[num_triggers:]

                result = self._deserializer(client_id, trigger_keys, states)

                if callback.unpack_args:
                    return tuple([r for r in result.values()] + list(other_inputs))
                else:
                    return tuple([result] + list(other_inputs))

        else:

            def pre_hook(s, *triggers_states_inputs):
                num_triggers = len(callback.dependencies)
                trigger_keys = callback.dependencies

                if self.use_inner_store:
                    states = triggers_states_inputs[num_triggers : 2 * num_triggers]
                    other_inputs = triggers_states_inputs[2 * num_triggers :]
                else:
                    states = []
                    other_inputs = triggers_states_inputs[num_triggers:]

                result = self._deserializer(callback.client_id, trigger_keys, states)
                if callback.unpack_args:
                    return tuple([r for r in result.values()] + list(other_inputs))
                else:
                    return tuple([result] + list(other_inputs))

        callback._pre_function_hooks.append(pre_hook)

    def add_client(self, callback, unpack_args=False):
        callback.unpack_args = unpack_args
        self.clients.append(callback)

    def _before_registry(self, app):
        """
        This hook is called before the component is registered to the store.
        It configures the inputs and outputs for all client callbacks and provider
        callbacks, so they can use the store.
        """

        super()._before_registry(app)
        for provider in self.providers:
            provider.prepend_input(("main-div", "title"))
            provider.set_outputs((self.id, f"trigger-{provider.name}"))
            self.keys.append(provider.name)

            if self.use_inner_store:
                provider.add_outputs([(self.id, f"value-{provider.name}")])

        for client in self.clients:
            if not client.dependencies:
                client.dependencies = self.keys

            old_inputs = client.dash_inputs
            client.set_inputs(
                [("main-div", "title")]
                + [(self.id, f"trigger-{key}") for key in client.dependencies]
            )
            client.dash_inputs = client.dash_inputs + [
                i for i in old_inputs if i not in client.dash_inputs
            ]

            if self.use_inner_store:
                client.set_states(
                    [
                        (self.id, f"value-{key}")
                        for key in client.dependencies
                        if key != client.name
                    ]
                )

            self._add_store_prehook(client)

    def register_callback(self, callback, **kwargs):
        return self.add_provider(callback, **kwargs)


class PickleStorage(Storage):
    """
    A storage that stores the output of the function as a pickled string
    in a hidden div.
    """
    def __init__(self, id):
        super().__init__(id, use_inner_store=True)

    def _serializer(self, client_id, callback_id, *outputs):
        if len(outputs) == 1:
            outputs = outputs[0]

        serialized = codecs.encode(pickle.dumps(outputs), "base64").decode()
        return self._trigger(), serialized

    def _deserializer(self, client_id, trigger_names, states):
        obj = {}
        for name, state in zip(trigger_names, states):
            obj[name] = pickle.loads(codecs.decode(state.encode(), "base64"))
        return obj


class FileStorage(Storage):
    """
    A storage that stores the output of the function as a pickled
    temporary file.
    """
    import tempfile

    def __init__(self, id, maxsize=20):
        super().__init__(id)
        self.stores = deque(maxlen=maxsize)
        self.maxsize = maxsize
        self._directory = TemporaryDirectory()
        self.directory = self._directory.name

    def get_store(self, client_id):
        if client_id not in self.stores:
            if len(self.stores) == self.maxsize:
                last_id = self.stores.popleft()
                os.remove(os.path.join(self.directory, last_id))
            self.stores.append(client_id)

        store_path = os.path.join(self.directory, client_id)
        return store_path

    def _serializer(self, client_id, callback_id, *outputs):
        path = self.get_store(client_id)
        with open(path, "w+b") as fp:
            if len(outputs) == 1:
                outputs = outputs[0]

            if os.path.getsize(path) > 0:
                state = pickle.load(fp)
                state[callback_id] = outputs
            else:
                state = {callback_id: outputs}

            fp.seek(0)
            pickle.dump(state, fp)

        return self._trigger()

    def _deserializer(self, client_id, trigger_names, _):
        path = self.get_store(client_id)
        with open(path, "rb") as fp:
            obj = pickle.load(fp)
            return {name: obj[name] for name in trigger_names}


class ContextStorage(Storage):
    """
    Stores the output of the function in the application server context.
    """
    def __init__(self, id, maxsize=20):
        super().__init__(id, use_inner_store=False)
        self.stores = deque(maxlen=maxsize)
        self.maxsize = maxsize

    def _before_registry(self, app):
        super()._before_registry(app)
        app.server.store = {}

    def get_store(self, client_id):
        stores = app.store
        if client_id not in self.stores:
            stores[client_id] = {}
            if len(self.stores) == self.maxsize:
                last_id = self.stores.popleft()
                del stores[last_id]
            self.stores.append(client_id)

        return stores[client_id]

    def _serializer(self, client_id, callback_id, *outputs):
        store = self.get_store(client_id)
        if len(outputs) == 1:
            outputs = outputs[0]
        store[callback_id] = outputs
        return self._trigger()

    def _deserializer(self, client_id, trigger_names, _):
        store = self.get_store(client_id)
        return {name: store.get(name) for name in trigger_names}
