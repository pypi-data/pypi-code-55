import itertools

import click
from dateutil.parser import parse
from tabulate import tabulate

from pyqalx.core.entities.bot import Bot
from pyqalx.core.signals import QalxSignal


class QalxCLITabulation:
    """
    A helper class for building a table of entities to display to the user
    """

    prompt_text = None

    def __init__(self, qalx_session, name, entity_class, tabulate_single=False):
        """
        :param qalx_session: An instance of QalxSession
        :param name: The name of the entity that we are looking for
        :param entity_class: The entity class that is being tabulated
        :param tabulate_single: Whether we should tabulate if a single
        result is found or just return the entity
        """

        self.qalx_session = qalx_session
        self.name = name
        self.tabulate_single = tabulate_single
        self.entity_type = entity_class.entity_type

        # Get the entities for the prompt
        self.entities_for_prompt = self.get_entities_for_prompt()

    def query_kwargs(self):
        """
        By default there are no additional kwargs passed through to the query
        """
        return {}

    def get_entities_for_prompt(self):
        """
        Queries the API and returns the entities for the prompt based on
        `self.build_query()` and `self.query_kwargs`
        """
        query = self.build_query()
        entities = getattr(self.qalx_session, self.entity_type).find(
            query=query, **self.query_kwargs()
        )
        return entities["data"]

    def build_query(self):
        """
        Builds the query that will be used to query the api
        :return: A dict of the query, by default just the name will be queried
        """
        return {"name": self.name}

    @property
    def entity_type_plural(self):
        return f"{self.entity_type}s"

    def build_no_entities_message(self):
        """
        The message to be displayed if no entities are found matching the query
        """
        return f"No {self.entity_type_plural} found called `{self.name}`"

    @staticmethod
    def build_row(index, entity):  # pragma: no cover
        """
        A specific row on a table
        :param index: The index of this row
        :param entity: The entity instance
        :return: A list of data for the entity for a single row
        """
        raise Exception("Must be implemented by subclass")

    @staticmethod
    def build_headers():  # pragma: no cover
        """
        The headers for this table
        :return: A list of strings for the table
        """
        raise Exception("Must be implemented by subclass")

    def tabulate(self):
        """
        For the given `self.entities_for_prompt` will build a table using
        tabulate and display this to the user via `click.echo`
        """
        table = []

        # Massage the remaining entities into a nice format for presentation
        for index, entity in enumerate(self.entities_for_prompt, start=1):
            table.append(self.build_row(index, entity))

        # We then display the entities to the user in a list,
        # and potentially prompt them for an index for the specific one they
        # wish to interact with
        headers = self.build_headers()
        # Display a table of entities
        click.echo(tabulate(table, headers))
        return table

    def get_entity_or_display(self):
        """
        Will either return the entity or display a table of entities
        depending on the number of entities found and the value
        of `self.tabulate_single`.
        If no entities are found always return None
        """
        entities_for_prompt = self.entities_for_prompt
        if len(entities_for_prompt) == 1:
            # Only a single entity found matching the name and with active
            # workers.
            # Just return it without showing the user the table of entities
            if self.tabulate_single:
                self.tabulate()
            else:
                return entities_for_prompt[0]
        elif not len(entities_for_prompt):
            # No entities found.  Nothing to do!
            click.echo(self.build_no_entities_message())
            return
        else:
            # Many entities found matching the query.
            # Create a table to allow the user to pick which they want
            index = 0
            table = self.tabulate()
            if self.prompt_text:
                # Wait until they choose an option that is valid.
                # Only display this prompt if there is prompt text.
                # If there isn't prompt text then we probably just want to
                # show a table of entities (i.e. it's an info command)
                while index == 0 or index > len(table):
                    index = click.prompt(
                        f"Please choose a {self.entity_type} index"
                        f" to {self.prompt_text}",
                        type=int,
                    )
                # Get the entity from the index (-
                # 1 because the index the user chooses starts at 1)
                return self.entities_for_prompt[index - 1]


class BotTabulation(QalxCLITabulation):
    def __init__(self, *args, **kwargs):
        super(BotTabulation, self).__init__(entity_class=Bot, *args, **kwargs)

    @staticmethod
    def build_headers():
        return [
            "Index",
            "Name",
            "Status",
            "Platform",
            "Node",
            "No. Workers",
            "Created On",
            "Created By",
        ]

    @staticmethod
    def build_row(index, entity):
        created_on = parse(entity["info"]["created"]["on"]).strftime(
            "%d/%m/%Y %H:%M:%S"
        )
        row = [
            index,
            entity["name"],
            entity["status"],
            entity["host"].get("platform"),
            entity["host"].get("node"),
            len(entity["workers"]),
            created_on,
            entity["info"]["created"]["by"]["email"],
        ]
        return row


class TerminateBotTabulation(BotTabulation):
    prompt_text = "terminate"

    def build_query(self):
        query = super(TerminateBotTabulation, self).build_query()
        query["workers"] = {"$exists": True, "$not": {"$size": 0}}
        return query

    def query_kwargs(self):
        """
        Only return the workers field when querying for terminated bots
        as another query is required to check the status of each
        """
        query_kwargs = super(TerminateBotTabulation, self).query_kwargs()
        query_kwargs["fields"] = ["workers"]
        return query_kwargs

    def build_no_entities_message(self):
        message = super(
            TerminateBotTabulation, self
        ).build_no_entities_message()
        return f"{message} that have workers that are not already terminated"

    @staticmethod
    def _filterfalse_signal(_bot):
        """
        itertools.filterfalse is used to exclude bots if a specific signal
        IS FALSE.
        Returns the status of this bots terminate signal.  If this signal
        is True (i.e. the bot is terminated) then it WON'T get returned
        to the user
        """
        return QalxSignal(_bot).terminate

    def get_entities_for_prompt(self):
        """
        For the termination prompt, only show bots that exist with workers
        that aren't terminated.
        """
        bots = super(TerminateBotTabulation, self).get_entities_for_prompt()
        potential_bots = []
        # Because we don't unpack when doing a `find` we need to do
        # an extra reload query for each bot so we can get the signal data
        for bot in bots:
            potential_bots.append(self.qalx_session.bot.reload(bot))

        def _has_workers_with_specific_signal(_bot):
            # For each bot, we only return it if any of the
            # workers ARE NOT on a status of `self._filter_signal(x)`.
            # As a separate function to avoid nested lambdas
            return list(
                itertools.filterfalse(
                    lambda x: self._filterfalse_signal(x), _bot["workers"]
                )
            )

        # We then filter the bots to only be those that have any workers that
        # don't have a self._filterfalse signal.
        entities_for_prompt = list(
            filter(_has_workers_with_specific_signal, potential_bots)
        )
        return entities_for_prompt


class StopBotTabulation(TerminateBotTabulation):
    prompt_text = "stop"

    def build_no_entities_message(self):
        message = super(
            TerminateBotTabulation, self
        ).build_no_entities_message()
        return (
            f"{message} that have workers that are not already stopped "
            f"or terminated"
        )

    @staticmethod
    def _filterfalse_signal(_bot):
        """
        itertools.filterfalse is used to exclude bots if a specific signal
        IS FALSE.
        :return: If the bots stop signal is True (i.e. the bot is stopped)
        then the bot WON'T get returned to the user OR if the bots
        terminate signal is True (i.e. the bot is terminated)
         then the bot WON'T get returned to the user.
         Therefore, this will only return non terminated bots that are also
         not stopped
        """
        signal = QalxSignal(_bot)
        return signal.terminate is True or signal.stop is True


class ResumeBotTabulation(TerminateBotTabulation):
    prompt_text = "resume"

    def build_no_entities_message(self):
        message = super(
            TerminateBotTabulation, self
        ).build_no_entities_message()
        return f"{message} that have workers that can be resumed"

    @staticmethod
    def _filterfalse_signal(_bot):
        """
        itertools.filterfalse is used to exclude bots if a specific signal
        IS FALSE.
        :return: if the bots stop signal is False (i.e. the bot is not stopped)
        then the bot WON'T get returned to the user OR if the bots terminate
        signal is True (i.e. the bot is terminated) then the bot WON'T get
        returned to the user.
        Therefore, this will only return non terminated bots that are also
        stopped
        """
        signal = QalxSignal(_bot)
        return signal.terminate is True or signal.stop is False
