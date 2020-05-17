# -*- coding: utf-8 -*-

import pytest

from nlpcleaner import TextCleaner

def test_clear_blank_lines():
    txt = "first line\r\n\r\nsecond line"
    assert TextCleaner(txt).clear_blank_lines() == "first line second line"

def test_strip_all():
    txt = "this is a test\n"
    assert TextCleaner(txt).strip_all() == "this is a test"

def test_lower_all():
    txt = "THIS IS A TEST"
    assert TextCleaner(txt).lower_all() == "this is a test"

def test_remove_numbers():
    txt = "numbers 1 2 3 4 5 6 7 8 9 42"
    assert TextCleaner(txt).remove_numbers() == "numbers"

def test_remove_symbols():
    txt = "this is a t風est `~!@#$%^&*()_|+\-=?;:'\",.<>{}[]/"
    assert TextCleaner(txt).remove_symbols() == "this is a t風est"

def test_remove_urls():
    txt = "this is a test https://www.test.it http://www.test.it ftp://test.it"
    assert TextCleaner(txt).remove_urls() == "this is a test"

def test_strip_html_tags():
    txt = "<script>alert('test')</script><p>I'm currently working on a flash project using external interface and I'm able to get this <a href=\"http://codepen.io/rginnow/pen/mwFpC\" rel=\"nofollow\">interface to display</a>. However when I try to type something in the input field, it doesn't allow me to click on the field or on the buttons. So I did some digging around and found out that maybe this is what's causing it.</p><pre><code>  .panel {    background: #000;    padding: 10px;    width: 45%;    height: 200px;    position: absolute;    top: 10px;    z-index: -1;  }</code></pre><p>I tried changing <code>z-index</code> to <code>1</code> and it allowed me to type but at the same time, it seems to mess up the interface. Does anyone have a fix for this?</p><p>One more thing, whenever I click on a option like <code>change password</code> the panel opens up, but when I click on it again, it doesn't close but instead slides right back up.</p><p>I'm no expert when it comes to CSS so I'm hoping someone can help me out with this.</p>"
    assert TextCleaner(txt).strip_html_tags() == "alert('test') I'm currently working on a flash project using external interface and I'm able to get this interface to display . However when I try to type something in the input field, it doesn't allow me to click on the field or on the buttons. So I did some digging around and found out that maybe this is what's causing it. .panel { background: #000; padding: 10px; width: 45%; height: 200px; position: absolute; top: 10px; z-index: -1; } I tried changing z-index to 1 and it allowed me to type but at the same time, it seems to mess up the interface. Does anyone have a fix for this? One more thing, whenever I click on a option like change password the panel opens up, but when I click on it again, it doesn't close but instead slides right back up. I'm no expert when it comes to CSS so I'm hoping someone can help me out with this."

def test_remove_script():
    txt = "<script>alert('test')</script><p>test</p>"
    assert TextCleaner(txt).remove_script() == "<p>test</p>"

def test_remove_stopwords_guessing_language():
    txt = "this is a test"
    assert TextCleaner(txt).remove_stopwords() == "test"

def test_remove_stopwords_with_passed_language():
    txt = "this is a test"
    assert TextCleaner(txt, 'en').remove_stopwords() == "test"

def test_remove_stopwords_with_not_supported_passed_language():
    txt = "this is a test"
    assert TextCleaner(txt, 'lang_not_supported').remove_stopwords() == "this is a test"

def test_remove_stopwords_with_wrong_passed_language():
    txt = "this is a test"
    assert TextCleaner(txt, 'it').remove_stopwords() == "this is test"

def test_remove_stopwords_punjabi_language_supported():
    txt = "ਖੂਹ ਵਿਚ ਚੰਦਰਮਾ"
    assert TextCleaner(txt).remove_stopwords() == "ਖੂਹ ਵਿਚ ਚੰਦਰਮਾ"

def test_stemming():
    txt = "many dogs enjoy tug and chew toys and playing 'hide and seek' with you outdoors"
    assert TextCleaner(txt).stemming() == "mani dog enjoy tug and chew toy and play hide and seek with you outdoor"

def test_lemming():
    txt = "many dogs enjoy tug and chew toys and playing 'hide and seek' with you outdoors"
    assert TextCleaner(txt).lemming() == "many dog enjoy tug and chew toy and playing 'hide and seek' with you outdoors"
