from datetime import datetime
from PIL import Image


def img_date(fn):
    "returns the image date from image (if available)\nfrom Orthallelous"
    std_fmt = '%Y:%m:%d %H:%M:%S.%f'
    # for subsecond prec, see doi.org/10.3189/2013JoG12J126 , sect. 2.2, 2.3
    tags = [(36867, 37521),  # (DateTimeOriginal, SubsecTimeOriginal)
            (36868, 37522),  # (DateTimeDigitized, SubsecTimeDigitized)
            (306, 37520), ]  # (DateTime, SubsecTime)
    fp = Image.open(fn)
    exif = fp._getexif()
    fp.close()
    if not exif:
        return None

    for t in tags:
        dat = exif.get(t[0])
        sub = exif.get(t[1], 0)

        # PIL.PILLOW_VERSION >= 3.0 returns a tuple
        dat = dat[0] if type(dat) == tuple else dat
        sub = sub[0] if type(sub) == tuple else sub
        if dat != None:
            break

    if dat == None:
        return None
    full = '{}.{}'.format(dat, sub)
    T = datetime.strptime(full, std_fmt)
    #T = time.mktime(time.strptime(dat, '%Y:%m:%d %H:%M:%S')) + float('0.%s' % sub)
    return T
