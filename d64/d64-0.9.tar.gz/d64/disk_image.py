import shutil
import tempfile

from pathlib import Path

from .d64_image import D64Image


class DiskImage(object):
    raw_modes = {'r': 'rb', 'w': 'r+b'}

    def __init__(self, filepath, mode='r'):
        self.filepath = filepath
        self.mode = self.raw_modes.get(mode, 'rb')

    def __enter__(self):
        if self.mode == 'r+b':
            self.org_filepath = self.filepath
            tempf = tempfile.NamedTemporaryFile(prefix='d64-', dir=self.filepath.parent,
                                                delete=False)
            # copy existing file to temporary
            with self.org_filepath.open('rb') as inh:
                shutil.copyfileobj(inh, tempf)
            tempf.close()
            self.filepath = Path(tempf.name)

        self.image = D64Image(self.filepath)
        self.image.open(self.mode)
        return self.image

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.image.close()

        if self.mode == 'r+b':
            if exc_type is None:
                # update original with modified file
                self.filepath.replace(self.org_filepath)
            else:
                self.filepath.unlink()
