import subprocess


def j(item=None):
    console_output = subprocess.run(
        ["odbcinst", "-j"], stdout=subprocess.PIPE
    ).stdout.decode("utf-8")
    items = {}
    lines = console_output.split("\n")
    # first line is "special"
    line = lines.pop(0)
    key, value = line.split(" ")
    items[key] = value
    for line in lines:
        if line:
            key, value = line.split(": ")
            items[key.replace(".", "")] = value
    if item is None:
        return items
    else:
        return items[item]
