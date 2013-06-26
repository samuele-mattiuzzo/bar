try:
    from PIL import Image
except ImportError:
    import Image

import random
import urllib
import cStringIO

from bisect import bisect

# greyscale.. the following strings represent
# 7 tonal ranges, from lighter to darker.
# for a given pixel tonal level, choose a character
# at random from that range.
GREYSCALE = [
    " ",
    " ",
    ".,-",
    "_ivc=!/|\\~",
    "gjez2]/(YL)t[+T7Vf",
    "mdK4ZGbNDXY5P*Q",
    "W8KMA",
    "#%$"
]

# using the bisect class to put luminosity values
# in various ranges.
ZONEBOUNDS = [36, 72, 108, 144, 180, 216, 252]


class UnsupportedFormatException(Exception):
    pass


def _url_to_img(url):
    return cStringIO.StringIO(urllib.urlopen(url).read())


def to_ascii(url):

    # open image and resize
    # experiment with aspect ratios according to font
    # a monospaced font works best
    _la_image = _url_to_img(url)

    try:
        im = Image.open(_la_image)
    except:
        raise UnsupportedFormatException("Your file must be a valid .png image")

    im = im.resize((160, 75), Image.BILINEAR)
    im = im.convert("L")  # convert to mono

    # now, work our way over the pixels
    # build up str
    out = ""
    for y in range(0, im.size[1]):
        for x in range(0, im.size[0]):
            lum = 255-im.getpixel((x, y))
            row = bisect(ZONEBOUNDS, lum)
            possibles = GREYSCALE[row]
            out = out + possibles[random.randint(0, len(possibles)-1)]
        out = out+"\n"
    return out

if __name__=='__main__':
    print to_ascii('http://upload.wikimedia.org/wikipedia/commons/8/87/Avatar_poe84it.png')
