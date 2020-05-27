import os
from pathlib import Path

import click
import polib  # fades
from google.cloud import translate_v2 as translate  # fades google-cloud-translate == 2.0.1


CREDENTIALS_PATH = Path("credentials.json")
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(CREDENTIALS_PATH.resolve())


@click.command()
@click.argument('input_filename', type=click.Path(exists=True))
@click.option('--dst-lang', default='es', help="Destination Language. Default: 'es'")
@click.option('--fuzzy/--no-fuzzy', default=True, help="Mark as fuzzy translation")
@click.option('--output-filename', type=click.Path(), help="Output Filename Path.")
@click.option('--n', type=int, help="Number of strings to translate. Handy for testing this utility.")
def translation(input_filename, dst_lang, fuzzy, output_filename, n):
    _, w = os.popen("stty size", "r").read().split()
    tty_width = int(w)

    output_filename = output_filename if output_filename else input_filename

    translate_client = translate.Client()

    po = polib.pofile(input_filename)

    click.secho(f"\nTranslated {len(po.translated_entries())}/{len(po)} ({po.percent_translated()}%) of {Path(input_filename).resolve()}\n\n", fg='blue', bold=True)

    for i, entry in enumerate(po.untranslated_entries()):
        click.secho(f"{entry.msgid}", fg='yellow')
        result = translate_client.translate(
            entry.msgid,
            target_language=dst_lang,
            )
        entry.msgstr = result['translatedText']
        click.secho("-"*tty_width, fg='white')
        click.secho(f"{entry.msgstr}", fg='green')
        
        if fuzzy:
            entry.flags.append('fuzzy')
        
        click.secho("="*tty_width, fg='white')
        if n and i == n - 1:
            break
    click.secho(f"\n\nSaving to {Path(output_filename).resolve()}\n", fg='blue', bold=True)
    po.save(output_filename)


if __name__ == "__main__":
    translation()