import json
import math
import os
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked

from tululu_offline.get_args import get_args


def render_website() -> None:  # noqa: WPS210
    """Renders the template.html in index.html and saves a new file."""
    args = get_args()
    json_path = args.json_path
    dest_folder = args.dest_folder
    number_of_books_per_page = args.number_of_books_per_page

    path_to_file_with_books = json_path if json_path else f'{dest_folder}/books.json'
    with open(path_to_file_with_books, 'r') as file_object:
        books_json = file_object.read()
    books_list = json.loads(books_json)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml']),
        extensions=['jinja2.ext.loopcontrols'],
    )

    template = env.get_template('tululu_offline/template/index.html')

    pages_folder_path = 'pages'
    os.makedirs(pages_folder_path, exist_ok=True)

    count_of_books = len(books_list)
    number_of_pages = math.ceil(count_of_books / number_of_books_per_page)
    chunks = list(chunked(books_list, number_of_books_per_page))

    old_rendered_pages = set(Path('pages').glob('*.html'))
    new_rendered_pages = set()

    for current_page_number, chunk in enumerate(chunks, 1):
        rendered_page = template.render(
            books=chunk,
            current_page=current_page_number,
            number_of_pages=int(number_of_pages),
        )

        path_to_index_file = f'{pages_folder_path}/index{current_page_number}.html'
        with open(path_to_index_file, 'w', encoding='utf8') as index_file:
            index_file.write(rendered_page)
        new_rendered_pages.add(Path(path_to_index_file))

    outdated_pages = old_rendered_pages - new_rendered_pages

    for outdated_page in outdated_pages:
        Path.unlink(Path(outdated_page))


def main() -> None:  # noqa: WPS210
    """Entry point."""
    render_website()
    server = Server()
    server.watch('tululu_offline/template/index.html', render_website)
    server.serve(root='.')


if __name__ == '__main__':
    main()
