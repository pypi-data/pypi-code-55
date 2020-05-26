from urllib.parse import parse_qs, urlencode, urlsplit, urlunsplit

from django.utils.encoding import force_text


def simple_urljoin(*args):
    """
        Joins url parts like 'https://', 'google.com/', '/search/' to https://google.com/search/

        Treats parts ending on double slash as url beginning and ignores all parts before them.
        Other parts are treated as path and joined with single slash.

        Preserves single trailing and leading slash.
    """
    sep = '/'
    protocol_sep = '://'
    res = ''

    for idx, piece in enumerate(args):
        is_first = idx == 0
        is_last = idx == len(args) - 1

        add_leading_slash = add_trailing_slash = False

        piece = force_text(piece)

        if is_first and piece.startswith(sep):
            add_leading_slash = True

        if is_last and piece.endswith(sep):
            add_trailing_slash = True

        if not is_last:
            add_trailing_slash = True

        if piece.endswith(protocol_sep):
            piece = piece.lstrip('/')
            add_trailing_slash = False
        else:
            piece = piece.strip('/')

        if add_leading_slash:
            piece = sep + piece

        if add_trailing_slash:
            piece += sep

        if protocol_sep in piece:
            res = piece
        else:
            res += piece

    return res


def add_query(url: str, **params: str):
    scheme, netloc, path, query_string, fragment = urlsplit(url)
    query_params = parse_qs(query_string)

    query_params.update(params)
    new_query_string = urlencode(query_params, doseq=True)

    return urlunsplit((scheme, netloc, path, new_query_string, fragment))
