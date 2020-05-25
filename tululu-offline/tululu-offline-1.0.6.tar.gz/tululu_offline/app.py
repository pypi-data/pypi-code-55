import json
import os
import shutil
from pathlib import Path
from typing import Dict, List, Optional

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from tululu_offline.book import (
    get_genres_of_book,
    get_image_url,
    get_page_id,
    get_texts_of_comments,
    get_title_and_author_of_book,
)
from tululu_offline.download_files import download_image, download_txt
from tululu_offline.get_args import get_args
from tululu_offline.parse_tululu_category import get_books_url_from_category
from tululu_offline.render_website import render_website


def save_result_of_parsing(
    json_path: Optional[str],
    dest_folder: str,
    books_attributes: List[Dict[str, str]],
) -> None:
    """Saves the result of the parser to a json file."""
    if not json_path:
        os.makedirs(dest_folder, exist_ok=True)

    path_to_result_file = json_path if json_path else f'{dest_folder}/books.json'
    with open(path_to_result_file, 'w') as file_object:
        json.dump(books_attributes, file_object, ensure_ascii=False)


def main() -> None:  # noqa: WPS210
    """Entry point."""
    books_attributes = []
    args = get_args()
    dest_folder = args.dest_folder

    books_url_from_category = get_books_url_from_category(
        args.start_page,
        args.end_page,
        args.category_url,
    )

    image_folder_path = 'images'
    static_files_folder_path = 'static'

    if os.path.exists(image_folder_path):
        shutil.rmtree(image_folder_path)
    if os.path.exists(static_files_folder_path):
        shutil.rmtree(static_files_folder_path)

    shutil.copytree(str(Path('tululu_offline/template/images').resolve()), image_folder_path)
    shutil.copytree(str(Path('tululu_offline/template/static').resolve()), static_files_folder_path)

    for book_url in tqdm(books_url_from_category):
        response = requests.get(book_url, allow_redirects=False)
        response.raise_for_status()

        if response.status_code != 200:  # noqa: WPS432
            continue

        soup = BeautifulSoup(response.text, 'lxml')
        page_id = get_page_id(book_url)
        book_title, book_author = get_title_and_author_of_book(soup)
        download_txt_url = f'http://tululu.org/txt.php?id={page_id}'
        book_path = download_txt_url if args.skip_txt else download_txt(
            url=download_txt_url,
            filename=book_title,
            dest_folder=dest_folder,
        )

        if not book_path:
            continue

        image_url = get_image_url(soup, book_url)
        image_path = image_url if args.skip_imgs else download_image(
            url=image_url,
            filename=image_url.split('/')[-1],
            dest_folder=dest_folder,
        )

        book_attributes = {
            'title': book_title,
            'author': book_author,
            'img_src': image_path,
            'book_path': book_path,
            'comments': get_texts_of_comments(soup),
            'genres': get_genres_of_book(soup),
        }

        books_attributes.append(book_attributes)

    save_result_of_parsing(args.json_path, dest_folder, books_attributes)
    render_website()


if __name__ == '__main__':
    main()
