from dash.dependencies import Output
from dash_infra.components.storage import ContextStorage, PickleStorage
from dash_infra.core import as_callback, as_component
from dash_infra.html_helpers.divs import Col, Row

from .groups import ComponentGroup


class StoreUser(ComponentGroup):
    """
    A Store User component is a component which features a store,
    and uses that store as the input for its display.
    """

    registered_stores = set()

    def __init__(
        self,
        id,
        display_component,
        display_properties,
        store=None,
        keys=None,
        container=Row,
        **kwargs,
    ):
        self.display_component = as_component(
            display_component, id, container=Col(), **kwargs
        )
        self.storage = store or ContextStorage(id=f"store-{id}")
        self.display_id = id
        self.display_properties = display_properties
        self.keys = keys or []
        self.registered_stores.add(store.id)
        if store:
            super().__init__(
                f"{id}-container", self.display_component, container=container
            )
        else:
            super().__init__(
                f"{id}-container", self.display_component, store, container=container
            )

        self.display_callback = self.create_display_callback()
        self.display_callback.use_storage_inputs(self.storage, *self.keys)

    def create_display_callback(self):
        if isinstance(self.display_properties, list):
            return as_callback(
                outputs=[(self.display_id, p) for p in self.display_properties]
            )(self._display_callback)
        else:
            return as_callback(outputs=(self.display_id, self.display_properties))(
                self._display_callback
            )

    def register_callback(self, callback):
        """
        Registers a callback
        """
        return callback.to(self.storage)

    def _before_registry(self, app):
        self.callbacks.add(self.display_callback)

    def _process_data(self, data):
        return data

    def _display_callback(self, data):
        data = self._process_data(data)
        return self.display(data)

    def display(self, data):
        raise NotImplementedError
