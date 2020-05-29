# from __future__ import absolute_import
import neologdn
import re
import emoji


def preprocessing(text):
    text = neologdn.normalize(text)
    text = re.sub(r'\n', "", text)
    text = re.sub(r'\r', "", text)
    text = re.sub(r'\s', "", text)
    text = re.sub(r"(https?|ftp)(:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+$,%#]+)", "" , text)
    text = re.sub(r"#(\w+)", "" , text)
    text = re.sub(r"@([A-Za-z0-9_]+) ", "" , text)
    text = ''.join(c for c in text if c not in emoji.UNICODE_EMOJI)
    text = text.strip()

    return text
