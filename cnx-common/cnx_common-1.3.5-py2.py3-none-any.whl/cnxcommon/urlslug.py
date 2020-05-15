# -*- coding: utf-8 -*-
import re

from slugify import slugify

from . import utils


QUOTE_PATTERN = re.compile(r'[\']+')
REMOVE_PART_PATTERN = re.compile(r'<span class="os-part-text">([^<]+)</span>')


@utils.ensure_unicode
def generate_slug(book_title, *other_titles):
    """Generates a slug for a book title or a section title.

    GIVEN just the book title
    book_title = "College Physics"
    RETURNS
     "college-physics"

    GIVEN
    book_title = "College Physics"
    other_title = "1.1 The Science of Biology"
    RETURNS
     "1-1-the-science-of-biology"

     GIVEN
     book_title = "College Physics"
     other_title[0] = "1 Introduction: The Nature of Science and Physics"
     other_title[1] = "Problems &amp; Exercises"
     RETURNS
     "1-problems-exercises"

     NOTE that the chapter title is only used to determine the chapter number
     in case it is missing from the section title - like for "Introduction" sections.
    """
    if len(other_titles) == 0:
        book_title = slugify(remove_html_tags(book_title))
        return book_title

    section_title = other_titles[-1]
    if isinstance(section_title, bytes):
        section_title = section_title.decode('utf-8')
    # Remove any quotes from the textp
    section_title = QUOTE_PATTERN.sub('', section_title)

    result = slugify(remove_html_tags(section_title))
    if not get_os_number(section_title):
        # find the chapter number
        for title in reversed(other_titles[:-1]):
            number = get_os_number(title)
            if number:
                result = u'{}-{}'.format(number, result)
                break

    return slugify(result)


@utils.ensure_unicode
def remove_html_tags(title):
    tmp_title = REMOVE_PART_PATTERN.sub('', title)
    return re.sub(r"<.*?>", "", tmp_title)


@utils.ensure_unicode
def get_os_number(title):
    tmp_title = REMOVE_PART_PATTERN.sub('', title)
    m = re.search('<span class="os-number">([^<]+)</span>', tmp_title)
    if m:
        return m.group(1)
