from typing import List, Tuple
from urllib.parse import urljoin

from bs4 import BeautifulSoup


def get_title_and_author_of_book(soup) -> Tuple[str, str]:
    """Gets the title and author of the book."""
    title_tag = soup.select_one('h1')
    title_and_author = title_tag.text.split('::')
    title, author = [book_attr.strip() for book_attr in title_and_author]
    return title, author


def get_image_url(soup: BeautifulSoup, book_url: str) -> str:
    """Gets full path to image."""
    image_src = soup.select_one('.bookimage img')['src']
    return urljoin(book_url, image_src)


def get_page_id(book_url: str) -> int:
    """Gets page if from a book url."""
    return int(book_url.split('/')[-2][1:])


def get_texts_of_comments(soup: BeautifulSoup) -> List[str]:
    """Gets texts of the page's comments."""
    return [
        tag.text
        for tag in soup.select('.texts .black')
    ]


def get_genres_of_book(soup: BeautifulSoup):
    """Gets genres of book."""
    return [
        tag.text
        for tag in soup.select('span.d_book a')
    ]
