from typing import List
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def get_soup(url: str) -> BeautifulSoup:
    """Gets BeautifulSoup object."""
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'lxml')


def get_books_url_from_page(soup: BeautifulSoup, page_url: str) -> List[str]:
    """Gets all links from a single category page."""
    return [
        urljoin(page_url, tag['href'])
        for tag in soup.select('.bookimage a')
    ]


def get_books_url_from_category(
    start_page_id: int, end_page_id: int, category_url: str,
) -> List[str]:
    """Gets all links from all pages in the category."""
    books_url = []
    for page_id in range(start_page_id, end_page_id):
        page_url = f'{category_url}/{page_id}/'
        soup = get_soup(page_url)
        books_url_from_page = get_books_url_from_page(soup, page_url)
        if not books_url_from_page:
            break
        books_url.extend(books_url_from_page)
    return books_url
