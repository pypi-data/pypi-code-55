import os
import mimetypes
import random
import string

BOUNDARY_CHARS = string.digits + string.ascii_letters


def encode(fields, files=None):
    '''
    Encode multipart/form-data
    '''
    boundary = ''.join(random.choice(BOUNDARY_CHARS) for i in range(30))
    lines = []

    for name, value in fields.items():
        if isinstance(value, list):
            for itm in value:
                lines.extend((
                    '--{0}'.format(boundary),
                    'Content-Disposition: form-data; name="{0}"'.format(escape_quote(name)),
                    '',
                    str(itm),
                ))
        else:
            lines.extend((
                '--{0}'.format(boundary),
                'Content-Disposition: form-data; name="{0}"'.format(escape_quote(name)),
                '',
                str(value),
            ))

    for fn in files:
        name = os.path.basename(fn)
        with open(fn, "rb") as content_file:
            content = content_file.read()
        mimetype = mimetypes.guess_type(fn)[0] or 'application/octet-stream'
        lines.extend((
            '--{0}'.format(boundary),
            'Content-Disposition: form-data; name="{0}"; filename="{1}"'.format(escape_quote(name), escape_quote(fn)),
            'Content-Type: {0}'.format(mimetype),
            '',
            content,
        ))

    lines.extend((
        '--{0}--'.format(boundary),
        '',
    ))
    body = '\r\n'.join(lines)

    headers = {
        'Content-Type': 'multipart/form-data; boundary={0}'.format(boundary),
        'Content-Length': str(len(body)),
    }

    return (body, headers)


def escape_quote(s):
    return s.replace('"', '\\"')
