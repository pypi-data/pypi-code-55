from typing import List

from beets.importer import BaseImportTask
from beets.plugins import BeetsPlugin
from beets.ui import Subcommand

from beetsplug.tagmod.command.options import tagmod_command_parser
from beetsplug.tagmod.command.utilities import tagmod_command_function
from beetsplug.tagmod.configuration import (
    get_configured_modifications,
    set_default_configuration,
    should_run_automatically,
    verify_configuration,
)
from beetsplug.tagmod.logging import LoggingWrapper
from beetsplug.tagmod.modification import modify_media_item


class TagMod(BeetsPlugin):
    def __init__(self):
        super(TagMod, self).__init__()
        set_default_configuration(self.config)
        verify_configuration(self.config)
        LoggingWrapper.get_instance().set_internal_logger(self._log)

        if should_run_automatically(self.config):
            self.import_stages = [self.import_task]

    def import_task(self, _, task: BaseImportTask) -> None:
        LoggingWrapper.get_instance().debug(
            "Run tag modification import procedure"
        )
        modifications = get_configured_modifications(self.config)

        for media_item in task.imported_items():
            modify_media_item(media_item, modifications)
            media_item.store()

    def commands(self) -> List[Subcommand]:
        tagmod_command = Subcommand(
            "tagmod",
            parser=tagmod_command_parser,
            help="Modify tags via pattern",
        )
        tagmod_command.func = tagmod_command_function
        return [tagmod_command]
