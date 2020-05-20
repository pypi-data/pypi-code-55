import click
import pyperclip


@click.command()
@click.argument("file-path", type=click.Path(exists=True, resolve_path=True))
@click.option("-c", "--clipboard", "clipboard_flag", is_flag=True, default=False)
def cli(file_path, clipboard_flag):
    print(file_path)

    if clipboard_flag:
        pyperclip.copy(file_path)
        print("[Result copied to clipboard]")

    return True


if __name__ == "__main__":
    cli()
