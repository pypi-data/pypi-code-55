from rich import print as rp


def bold(text: str, color: str = 'cyan') -> str:
    return f"[bold {color}]{text}[/bold {color}]"


def bred(text: str) -> str:
    return f"[bold red]{text}[/bold red]"


def bcyan(text):
    return f"[bold cyan]{text}[/bold cyan]"


def bblue(text):
    return f"[bold slate_blue3]{text}[/bold slate_blue3]"


def byellow(text):
    return f"[bold bright_yellow]{text}[/bold bright_yellow]"


def bgreen(text):
    return f"[bold spring_green4]{text}[/bold spring_green4]"


def underline(text):
    return f"[u]{text}[/u]"


def warn(text) -> str:
    return bred(text)


def clear(text) -> str:
    return bgreen(text)
