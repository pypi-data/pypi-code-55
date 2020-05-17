import io
import platform


def stream_configure(encoding, stream):
    if platform.python_version_tuple() >= ('3', '7'):
        stream.reconfigure(encoding=encoding)
    else:
        stream = io.TextIOWrapper(stream.buffer, encoding=encoding)
    
    return stream
