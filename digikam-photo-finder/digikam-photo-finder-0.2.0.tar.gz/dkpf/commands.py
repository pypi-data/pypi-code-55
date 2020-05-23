import os
import subprocess

from cleo import Command

from dkpf.config import config
from dkpf.database import DigikamDB


class ConfigCommand(Command):
    """
    Display the active configuration.

    config
        {--e|--edit=? : Open the configuration file in your editor}
    """

    def handle(self):
        edit = self.option("edit")
        if not edit:
            print(config.dump())
            return

        if edit != "null":
            editor = edit
        elif "VISUAL" in os.environ:
            editor = os.environ["VISUAL"]
        elif "EDITOR" in os.environ:
            editor = os.environ["EDITOR"]
        else:
            print("Unable to determine editor; please specify a binary")

        if editor:
            config.path.parent.mkdir(parents=True, exist_ok=True)
            subprocess.Popen([editor, config.path]).wait()


class FindCommand(Command):
    """
    Find the file paths of all photos matching specified tags.

    find
        {tags* : Return images with all of the specified tags}
        {--d|--database= : Path to the digikam database}
    """

    def handle(self):
        database_path = self.option("database")
        if not database_path:
            database_path = config.database["path"]

        db = DigikamDB(database_path)
        tags = self.argument("tags") or []
        paths = db.get_paths(tags)

        if config.root:
            paths = [os.path.join(config.root, p) for p in paths]
        print("\n".join(paths))
