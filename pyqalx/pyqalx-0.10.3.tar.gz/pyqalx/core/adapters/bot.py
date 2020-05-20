import logging

from pyqalx.core.adapters.adapter import (
    QalxUnpackableAdapter,
    QalxNamedEntityAdapter,
    QalxUpdateStatusAdapter,
)
from pyqalx.core.entities import Bot
from pyqalx.core.entities.worker import Worker

logger = logging.getLogger(__name__)


class QalxBot(
    QalxUnpackableAdapter, QalxNamedEntityAdapter, QalxUpdateStatusAdapter
):
    _entity_class = Bot
    child_entity_class = Worker
    _user_only_methods = ["add"]
    _bot_only_methods = ["replace_workers"]

    def _should_unpack(self):
        return True

    def _kids_for_lookup(self, entity):
        """
        The kids on a bot are just a list of guids
        """
        return entity[self.kids]

    def _unpacked_entities_to_valid_children(self, entity, unpacked_entities):
        """
        The unpacked entities are just a list on a Bot, therefore
        just return them

        :param entity: The Bot entity
        :param unpacked_entities: The unpacked Worker entities
        :return: The unpacked Worker entities
        """
        return unpacked_entities

    def _child_list_response(self, child_adapter, entity, **kwargs):
        """
        A bot needs to pass itself through to the child adapter in order
        to correctly build the list endpoint for Worker.  Don't
        filter the workers by anything - always return all of them for
        the given bot

        :param child_adapter: The child_adapter
        :param entity: The `QalxBot` entity
        :return: The child_adapter list response
        """
        return child_adapter.find(bot_entity=entity)

    def _pack_kids_for_request(self, kwargs):
        """
        Bots don't get added with workers - so just bypass the packing
        of the kids
        :param kwargs: kwargs sent to `add` method
        :return: kwargs
        """
        return kwargs

    def get_kids_keys_to_save(self, kids_to_save):
        """
        The kids on a Bot are a list, whereas normal packed entities are a dict
        Therefore, return the kids guids as a list
        :param kids_to_save: The kids on the Bot (either fully inflated or
        just the guids)
        :type kids_to_save: list
        :return:A list of guids of the kids on this Bot
        """
        return [
            str(k["guid"]) if isinstance(k, dict) else k for k in kids_to_save
        ]

    def cache_original_kids(self, kids):
        """
        The kids on a Bot are a list, so we need to cache them as a list
        :param kids: The kids on the bot
        :type kids: list
        :return: A list of the kids
        """
        return [k for k in kids]

    def add(self, name, config, meta=None, **kwargs):
        """
        Creates a `Bot` instance.

        :param name: The name that this bot will be given
        :type name: str
        :param config: The bots config
        :type config: dict
        :param meta: A dictionary of metadata to store
        :type meta: dict
        :return: The newly created `Bot` instance
        """
        return super(QalxBot, self).add(
            host=self.session._host_info,
            name=name,
            meta=meta,
            config=config,
            **kwargs,
        )

    def replace_workers(self, bot_entity, workers):
        """
        Completely replaces any Workers on the given bot.  Will return the
        replaced workers in an unpacked state

        :param bot_entity: The ~entities.bot.Bot entity that is being changed
        :param workers: The number of workers that this bot should have
        :return: A ~entities.bot.Bot instance with the updated workers
        """
        guid = bot_entity["guid"]
        detail_endpoint = self.detail_endpoint(guid=guid)
        endpoint = f"{detail_endpoint}/replace-workers"
        logger.debug(
            f"replace workers {self.entity_class.entity_type} with"
            f" guid {guid} with {endpoint}"
        )

        entity = self._process_api_request("patch", endpoint, workers=workers)
        entity = self.entity_class(entity)
        entity = self._attempt_unpack(entity)
        return entity

    def _signal_workers(self, entity, signal_method, *args, **kwargs):
        """
        Helper method for calling signals on workers.  A bot doesn't have
        the concept of `signals`.  Instead, we call a signal method we just
        apply this to all the workers on the bot
        """

        for worker in entity.get(self.kids, []):
            worker_method = getattr(self.session.worker, signal_method)
            worker_method(worker, bot_entity=entity, *args, **kwargs)

    def stop(self, entity, **kwargs):
        """
        Stops all the workers on the bot
        """
        self._signal_workers(entity, signal_method="stop", **kwargs)

    def resume(self, entity, **kwargs):
        """
        Resumes all the workers on the bot
        """
        self._signal_workers(entity, signal_method="resume", **kwargs)

    def terminate(self, entity, *args, **kwargs):
        """
        Terminates all the workers on the bot
        """
        self._signal_workers(
            entity, signal_method="terminate", *args, **kwargs
        )  # noqa
