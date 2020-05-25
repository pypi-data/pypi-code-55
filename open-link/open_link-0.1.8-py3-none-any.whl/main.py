
import click
import pyperclip
import subprocess
import shlex
from syslog import syslog

from click import Context
from pobject import I


@click.command()
@click.argument('link', required=False)
@click.option('--clipboard', 'clipboard_flag', is_flag=True)
@click.option('--selection', 'selection_flag', is_flag=True)
@click.option('--multi', is_flag=True)
@click.pass_context
def main(context: Context, link, clipboard_flag, selection_flag, multi):

    """
    Get text from selection or clipboard and open it in Google Chrome

    E.g URL: https://google.com

    E.g URL: https://stackoverflow.com
    """

    if link:
        _open_in_chrome(link)
        return True

    text_from_selection = _get_selection()

    if type(text_from_selection) == bytes:
        text_from_selection = text_from_selection.decode()

    text_from_clipboard = _get_clipboard()

    text_from_stdin = ''
    if not click.get_text_stream('stdin').isatty():
        text_from_stdin = click.get_text_stream('stdin').read().strip()

    text_from_selection_is_url = I(text_from_selection).is_url
    text_from_clipboard_is_url = I(text_from_clipboard).is_url

    if text_from_stdin:
        if I(text_from_stdin).is_url:
            _open_in_chrome(text_from_stdin)
        else:
            result = f'https://www.google.com/search?q={text_from_stdin}'
            _open_in_chrome(result)
    elif selection_flag:
        if text_from_selection_is_url:
            _open_in_chrome(text_from_selection)
        else:
            _print_message(f'Not valid URL: {text_from_selection}')
    elif clipboard_flag:
        if text_from_clipboard_is_url:
            _open_in_chrome(text_from_clipboard)
        else:
            _print_message(f'Not valid URL: {text_from_clipboard}')
    else:
        if I(text_from_selection).is_url:
            result = text_from_selection
        elif I(text_from_clipboard).is_url:
            result = text_from_clipboard
        else:
            if text_from_clipboard != '':
                result = f'https://www.google.com/search?q={text_from_clipboard}'
            elif text_from_selection != '':
                result = f'https://www.google.com/search?q={text_from_selection}'
            else:
                message = f'Not a valid input | selection: {text_from_selection} | clipboard: {text_from_clipboard}'
                _print_message(message)
                return False

        _open_in_chrome(result)


def _print_message(message):
    print(message)
    syslog(message)
    return True


def _open_in_chrome(url):
    subprocess.call(['google-chrome', '--new-window', url])
    return True


def _get_clipboard():
    return pyperclip.paste()


def _get_selection():
    return subprocess.check_output((shlex.split('xclip -out -selection')))

