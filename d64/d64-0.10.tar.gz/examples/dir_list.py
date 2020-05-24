import sys

from pathlib import Path

from d64 import DiskImage

with DiskImage(Path(sys.argv[1])) as image:
    for line in image.directory():
        print(line)
