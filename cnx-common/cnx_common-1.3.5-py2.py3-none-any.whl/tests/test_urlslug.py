# -*- coding: utf-8 -*-
"""
# Copyright (c) 2019, Rice University
# This software is subject to the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
"""
import re

import pytest

from cnxcommon.urlslug import generate_slug

class TestSlugGenerator:
    def test_it_removes_html_tags(self):
        title = "<span class=\"os-number\"></span><span>sometext</span>"
        expected = "sometext"
        actual = generate_slug(title)

        assert expected == actual

    def test_it_removes_special_chars(self):
        title = "@#$*(&sometext!!!"

        expected = "sometext"
        actual = generate_slug(title)

        assert re.match(r'^\W+$', actual) is None
        assert expected == actual

    def test_it_replaces_special_chars_btwn_text_with_dashes(self):
        title = "@#$*(&some!!!text!!!"

        expected = "some-text"
        actual = generate_slug(title)

        assert re.match(r'^\W+$', actual) is None
        assert expected == actual

    def test_it_replaces_spaces_with_dashes(self):
        title = "some text and     a    bunch      of     spaces    "
        expected = "some-text-and-a-bunch-of-spaces"
        actual = generate_slug(title)

        assert expected == actual

    def test_it_makes_all_lowercase(self):
        title = "SomeTEXT"
        expected = "sometext"
        actual = generate_slug(title)

        assert expected == actual

    def test_it_replaces_unicode_chars_w_their_ascii_equivalent(self):
        title = "podręcznikfizykadlaszkółwyższych"
        expected = "podrecznikfizykadlaszkolwyzszych"
        actual = generate_slug(title)

        assert expected == actual

    def test_it_can_identify_chapter_and_section_numbers(self):
        title = "12.4 sometext"
        expected = "12-4-sometext"
        actual = generate_slug(title)

        assert expected == actual

    def test_with_only_chapter_number_not_section(self):
        title = "1 introduction"
        expected = "1-introduction"
        actual = generate_slug(title)

        assert expected == actual

    def test_using_generate_slug(self):
        title = "12.4 sometext"
        expected = "12-4-sometext"
        actual = generate_slug(title)

        assert expected == actual

    def test_it_removes_trailing_slashes(self):
        title = "-12.4 some-text--"
        expected = "12-4-some-text"
        actual = generate_slug(title)

        assert expected == actual

    def test_it_removes_html_encoded_chars(self):
        title = "12.4 sometext&amp;moretext"
        expected = "12-4-sometext-moretext"
        actual = generate_slug(title)

        assert expected == actual

    def test_it_can_find_chapter_number_when_not_in_section_title(self):
        """If the chapter number isn't present in the section title,
        it can find it in the chapter title instead.
        """
        book_title = "college-physics"
        chapter_title = '<span class="os-number">1</span> Introduction: The Nature of Science and Physics'
        section_title = "problems-and-exercises"
        expected = "1-problems-and-exercises"
        actual = generate_slug(book_title, chapter_title, section_title)

        assert expected == actual

    def test_when_chapter_number_not_present_in_section_nor_chapter_titles(self):
        """What happens when (or if) a chapter number is not present in the chapter
        title nor the section title.
        """
        book_title = "college-physics"
        chapter_title = "Introduction: The Nature of Science and Physics"
        section_title = "problems-and-exercises"
        expected = "problems-and-exercises"
        actual = generate_slug(book_title, chapter_title, section_title)

        assert expected == actual

    def test_slug_generator_acceptance_test(self):
        """High-level test using the Acceptance Criteria described in:
        https://github.com/openstax/cnx/issues/348
        """
        books = [
            (
                'College Physics',
                '<span class="os-number">12</span><span class="os-divider"> </span><span class="os-text">Fluid Dynamics and Its Biological and Medical Applications</span>',
                '<span class="os-number">12.4</span><span class="os-divider"> </span><span class="os-text">Viscosity and Laminar Flow; Poiseuille\'s Law< /span >',
            ), (
                'College Physics',
                '<span class="os-number">1</span><span class="os-divider"> </span><span class="os-text">Introduction: The Nature of Science and Physics</span>',
                '<span class="os-text">Problems &amp; Exercises</span>',
            ), (
                'Biology 2e',
                '<span class="os-number">1</span><span class="os-divider"> </span><span class="os-text">The Study of Life</span>',
                '<span class="os-number">1.1</span><span class="os-divider"> </span><span class="os-text">The Science of Biology</span>',
            ), (
                'Biology 2e',
                '<span class="os-text">Preface</span>',
            ), (
                'Biology 2e',
            ), (
                'A Study of How a Region Can Lever Participation',
                '<span class="os-text">21st Century Economic Development</span>',
            ), (
                'A Study of How a Region Can Lever Participation',
                '<span class="os-text">21st Century Economic Development</span>',
                '<span class="os-text">Introduction</span>',
            ), (
                'Astronomy',
                '<span class=\"os-number\">2</span><span class=\"os-divider\"> </span><span class=\"os-text\">Observing the Sky: The Birth of Astronomy</span>',
                '<span class=\"os-text\">Exercises</span>',
                '<span class=\"os-text\">Review Questions</span>',
            ), (
                'Astronomy',
                '<span class=\"os-number\">2</span><span class=\"os-divider\"> </span><span class=\"os-text\">Observing the Sky: The Birth of Astronomy</span>',
                '<span class=\"os-number\">2.1</span><span class=\"os-divider\"> </span><span class=\"os-text\">The Sky Above</span>',
                '<span class=\"os-text\">Exercises</span>',
                '<span class=\"os-text\">Review Questions</span>',
            )
        ]

        expectations = [
            '12-4-viscosity-and-laminar-flow-poiseuilles-law',
            '1-problems-exercises',
            '1-1-the-science-of-biology',
            'preface',
            'biology-2e',
            '21st-century-economic-development',
            'introduction',
            '2-review-questions',
            '2-1-review-questions',
        ]

        for index, book in enumerate(books):
            assert expectations[index] == generate_slug(*book)

    # https://github.com/openstax/cnx/issues/389
    def test_removes_apostrophes(self):
        titles = (
            'University Physics Volume 2',
            '<span class="os-text">Unit 2. Electricity and Magnetism</span>',
            '<span class="os-number">9</span><span class="os-divider"> </span><span class="os-text">Current and Resistance</span>',
            '<span class="os-number">9.4</span><span class="os-divider"> </span><span class="os-text">Ohm\'s Law</span>',
        )

        slug = generate_slug(*titles)

        expected = '9-4-ohms-law'
        assert expected == slug

    def test_handling_bytes(self):
        titles = (
            b'College Physics',
            u'<span class="os-number">5</span><span class="os-divider"> </span><span class="os-text">'
            u'Further Applications of Newton’s Laws: Friction, Drag, and Elasticity</span>'.encode('utf-8'),
            u'<span class="os-text">Introduction: Further Applications of Newton’s Laws</span>'.encode('utf-8')
        )

        slug = generate_slug(*titles)
        assert slug == '5-introduction-further-applications-of-newtons-laws'

    def test_handling_unicode(self):
        titles = (
            u'College Physics',
            u'<span class="os-number">5</span><span class="os-divider"> </span><span class="os-text">'
            u'Further Applications of Newton’s Laws: Friction, Drag, and Elasticity</span>',
            u'<span class="os-text">Introduction: Further Applications of Newton’s Laws</span>',
        )

        slug = generate_slug(*titles)
        assert slug == '5-introduction-further-applications-of-newtons-laws'

    def test_discard_part_of_slug(self):
        """Acceptance test for the criteria described in:
        https://github.com/openstax/cnx/issues/972
        """
        book_title = "college-physics"
        chapter_title = '<span class="os-part-text">Chapter</span><span class="os-divider"> </span><span class="os-number">4</span><span class="os-divider"> </span><span class="os-text">Kinematics in 7 Dimensions</span>'
        expected = "4-kinematics-in-7-dimensions"
        actual = generate_slug(book_title, chapter_title)

        assert expected == actual

    def test_discard_part_of_slug_nested(self):
        """Acceptance test for the criteria described in:
        https://github.com/openstax/cnx/issues/972
        """
        book_title = "college-physics"
        chapter_title = '<span class="os-number"><span class="os-part-text">Chapter </span>2</span><span class="os-divider"> </span><span data-type="" itemprop="" class="os-text">Motion in One Dimension</span>'
        section_title = '<span class="os-text">Key Terms</span>'
        expected = "2-key-terms"
        actual = generate_slug(book_title, chapter_title, section_title)

        assert expected == actual

    def test_polish_book_slug(self):
        """Test written based upon failure observed with Polish Physics
        (col23946) per: https://github.com/openstax/cnx/issues/1000
        """
        book_title = 'Fizyka dla szkół wyższych. Tom 1'
        other_titles = (
            u'<span class="os-number">Cz\u0119\u015b\u0107 1</span><span class="os-divider"> </span><span data-type="" itemprop="" class="os-text">Cz\u0119\u015b\u0107 1. Mechanika</span>',
            u'<span class="os-number">Rozdzia\u0142 1</span><span class="os-divider"> </span><span data-type="" itemprop="" class="os-text">Jednostki i miary</span>',
            u'<span data-type="" itemprop="" class="os-text">Wst\u0119p</span>'
        )
        expected = "rozdzial-1-wstep"
        actual = generate_slug(book_title, *other_titles)

        assert expected == actual
