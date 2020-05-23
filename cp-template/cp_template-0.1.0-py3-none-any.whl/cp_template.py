import os
import sys

from coleo import Argument, auto_cli
from pystache import Renderer
from pystache.context import KeyNotFoundError


render = Renderer(missing_tags="strict")


def transform(path, text, env):
    try:
        return render.render(text, env)
    except KeyNotFoundError as err:
        print(
            f"Key '{err.args[0]}' required for file '{path}' was not found",
            file=sys.stderr,
        )
        sys.exit(1)


def run():
    """Copy a template file or directory."""

    # [positional]
    # Path to the file or directory to copy
    path: Argument

    # [positional: *]
    # key=value pairs to substitute
    env: Argument
    env_dict = dict(k.split("=") for k in env)

    full_path = os.path.abspath(path)

    if not os.path.exists(full_path):
        print(f"Error: {full_path} does not exist", file=sys.stderr)
        sys.exit(1)

    base = os.path.dirname(full_path)
    if not base.endswith("/"):
        base += "/"
    base_length = len(base)

    new_base = "."

    gen = {}

    data = list(os.walk(full_path, topdown=True))
    if os.path.isdir(full_path):
        first_entry = (base, [os.path.basename(full_path)], [])
    else:
        first_entry = (base, [], [os.path.basename(full_path)])
    data.insert(0, first_entry)
    for dirname, dirs, files in data:
        for d in dirs:
            full = os.path.join(dirname, d)
            relative = full[base_length:]
            new_relative = transform(full, relative, env_dict)
            gen[os.path.join(new_base, new_relative)] = None

        for f in files:
            full = os.path.join(dirname, f)
            relative = full[base_length:]
            new_relative = transform(relative, relative, env_dict)
            gen[os.path.join(new_base, new_relative)] = transform(
                full, open(full).read(), env_dict
            )

    for filename, contents in gen.items():
        if contents is None:
            print(f"Generating directory: {filename}")
            os.makedirs(filename)
        else:
            print(f"Generating file: {filename}")
            open(filename, "w").write(contents)


def main():
    auto_cli(run, [])
