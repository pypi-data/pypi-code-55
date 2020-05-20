#!/usr/bin/env python

"""Tests for `h2m` package."""

import pytest

from click.testing import CliRunner

from h2m import h2m

def test_h2m_md():
    # h2m.feed('<h1>h1</h1>')
    # assert h2m.md() == '# h1'
    # h2m.feed('''''')
    # assert h2m.md() == ''''''
    h2m.feed('''<p>Lorem</p>
    <p>ipsum</p>
    <p>sit</p>''')
    assert h2m.md() == '''Lorem

ipsum

sit'''
    h2m.feed('''<em>em element</em>''')
    assert h2m.md() == '''_em element_'''

    h2m.feed('''<i>i element</i>''')
    assert h2m.md() == '''_i element_'''

    h2m.feed('''<strong>strong element</strong>''')
    assert h2m.md() == '''**strong element**'''

    h2m.feed('''<b>b element</b>''')
    assert h2m.md() == '''**b element**'''

    h2m.feed('''<code>code element</code>''')
    assert h2m.md() == '''`code element`'''

    h2m.feed('''<h1>Level One Heading</h1>''')
    assert h2m.md() == '''# Level One Heading'''

    h2m.feed('''<h2>Level Two Heading</h2>''')
    assert h2m.md() == '''## Level Two Heading'''

    h2m.feed('''<h3>Level Three Heading</h3>''')
    assert h2m.md() == '''### Level Three Heading'''

    h2m.feed('''<h4>Level Four Heading with <code>child</code></h4>''')
    assert h2m.md() == '''#### Level Four Heading with `child`'''

    h2m.feed('''<img src="http://example.com/logo.png" />''')
    assert h2m.md() == '''![](http://example.com/logo.png)'''

    h2m.feed('''<img src="logo.png" alt="img with alt" />''')
    assert h2m.md() == '''![img with alt](logo.png)'''

    h2m.feed('''<a href="http://example.com">An anchor</a>''')
    assert h2m.md() == '''[An anchor](http://example.com)'''

    h2m.feed('''<a href="http://example.com" title="Title for
    
    link">An anchor</a>''')
    assert h2m.md() == '''[An anchor](http://example.com)'''

    h2m.feed('''    <ol>
      <li>Ordered list item 1</li>
      <li>Ordered list item 2</li>
      <li>Ordered list item 3</li>
    </ol>''')
    assert h2m.md() == '''1. Ordered list item 1
2. Ordered list item 2
3. Ordered list item 3'''

    h2m.feed('''    <p>A paragraph.</p>
    <ol>
      <li>Ordered list item 1</li>
      <li>Ordered list item 2</li>
      <li>Ordered list item 3</li>
    </ol>
    <p>Another paragraph.</p>
    <ul>
      <li>Unordered list item 1</li>
      <li>Unordered list item 2</li>
      <li>Unordered list item 3</li>
    </ul>''')
    assert h2m.md() == '''A paragraph.

1. Ordered list item 1
2. Ordered list item 2
3. Ordered list item 3

Another paragraph.

- Unordered list item 1
- Unordered list item 2
- Unordered list item 3'''

#     h2m.feed('''    <blockquote>
#       <p>This is the first level of quoting.</p>
#       <blockquote>
#         <p>This is a paragraph in a nested blockquote.</p>
#       </blockquote>
#       <p>Back to the first level.</p>
#     </blockquote>''')
#     assert h2m.md() == '''
# > 
# > This is the first level of quoting.
# > 
# > > This is a paragraph in a nested blockquote.
# > 
# >
# > Back to the first level.
# > 
# '''

    # h2m.feed('''''')
    # assert h2m.md() == ''''''

    # h2m.feed('''''')
    # assert h2m.md() == ''''''

    # h2m.feed('''''')
    # assert h2m.md() == ''''''