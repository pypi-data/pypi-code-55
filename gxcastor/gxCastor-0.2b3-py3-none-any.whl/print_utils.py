import rich


def bold(text: str, color: str = 'cyan') -> str:
    return f"[bold {color}]{text}[/bold {color}]"


if __name__ == '__main__':
    rich.print(bold("Hello"))
