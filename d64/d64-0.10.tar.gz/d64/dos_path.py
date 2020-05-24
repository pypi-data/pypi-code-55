from .exceptions import DiskFullError
from .file import File, RelativeFile


class DOSPath(object):
    """Encapsulate a path within an image."""
    def __init__(self, image, entry=None, name=None):
        self.image = image
        self.entry = entry
        self._name = name

    def __str__(self):
        return self.name.decode()

    def exists(self):
        """Return `True` if path exists."""
        return self.entry is not None

    def unlink(self):
        """Delete directory entry for this path."""
        if self.entry is None:
            raise FileNotFoundError("File not found: "+str(self.name))

        self.entry.file_type = 0
        block = self.entry.first_block()

        while block:
            self.image.free_block(block)
            block = block.next_block()

    def rename(self, other):
        """Rename this directory entry, replacing another entry if it exists."""
        if self.entry is None:
            raise FileNotFoundError("File not found: "+str(self.name))

        if isinstance(other, str) or isinstance(other, bytes):
            other = self.image.path(other)

        if other.entry:
            other.unlink()

        self.entry.name = other.name
        return self

    replace = rename

    @property
    def name(self):
        if self.entry:
            return self.entry.name
        return self._name

    @property
    def size_blocks(self):
        """Return file size in blocks."""
        if self.entry:
            return self.entry.size
        raise FileNotFoundError("File not found: "+str(self.name))

    @property
    def size_bytes(self):
        """Return file size in bytes."""
        if self.entry is None:
            raise FileNotFoundError("File not found: "+str(self.name))

        size = 0
        block = self.entry.first_block()
        while block:
            size += block.data_size
            block = block.next_block()

        return size

    def open(self, mode='r', ftype=None, record_len=None):
        """Return new file object."""
        if mode not in ('r', 'w'):
            raise ValueError("Invalid mode, "+mode)

        if mode == 'r':
            if self.entry is None:
                raise FileNotFoundError("File not found: "+str(self.name))
        else:
            # open file for write
            if not self.image.writeable:
                raise PermissionError("Image is read-only")

            if self.entry:
                # truncate an existing file
                self.entry.free_blocks()
            else:
                # no existing entry, create a new one
                if ftype is None:
                    raise ValueError("File type missing for new file")
                ftype = ftype.upper()
                if ftype == 'REL' and record_len is None:
                    raise ValueError("Record length missing for new relative file")
                entry = self.image.get_free_entry()
                if entry is None:
                    raise DiskFullError()

                entry.file_type = ftype
                entry.name = self._name
                entry.record_len = record_len if ftype == 'REL' else 0
                self.entry = entry
                self._name = None

            self.entry.reset()

        if self.entry.file_type == 'REL':
            return RelativeFile(self.entry, mode)

        return File(self.entry, mode)

    @staticmethod
    def wildcard_match(fname, ftype, wildcard):
        """Return True if file matches a DOS wildcard."""

        if isinstance(wildcard, str):
            wildcard = wildcard.encode()

        if b'=' in wildcard:
            # file type
            if wildcard[-1] == ord('='):
                raise ValueError("Invalid wildcard, "+str(wildcard))
            wildcard, wftype = wildcard.split(b'=', 1)
            if ord(ftype[0]) != wftype[0]:
                return False

        for w, f in zip(wildcard, fname):
            if w == ord('?'):
                # matches any character
                continue
            if w == ord('*'):
                # matches rest of file name
                return True
            if w != f:
                return False

        if len(fname)+1 == len(wildcard) and wildcard.endswith(b'*'):
            # zero length match
            return True
        return len(fname) == len(wildcard)
