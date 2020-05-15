import click


def fix_short_title_underline(path_to_rst_file: str) -> None:
    """
    Fixes too short underlines of titles of *.rst files
    example:
    COOKIETEMPLE
    ======
    ->
    COOKIETEMPLE
    ============

    :param path_to_rst_file: Path to the *.rst file (usually index.rst)
    """
    click.echo(click.style('Fixing too short underlines of *.rst titles', fg='blue'))
    try:
        with open(path_to_rst_file) as f:
            content = f.readlines()
            # Fix the underlined title by replacing the short underline with the correct length
            len_header = len(content[0])
            content[1] = len_header * '='
            # Write everything back
            with open(path_to_rst_file, 'w') as file:
                file.writelines(content)
    except FileNotFoundError:
        click.echo(click.style(f'Unable to find rst file: {path_to_rst_file}', fg='yellow'))
