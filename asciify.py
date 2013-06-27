try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    import Image
    import ImageDraw
    import ImageFont

import os
import random
import urllib
import StringIO

from bisect import bisect

MAX_SIZE = 350, 350
COLOR_WHITE = (255, 255, 255)
FILL = 'black'
OUTLINE = 'black'

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

    # awesome variable names.
    _la_image_from_la_url = urllib.urlopen(url).read()
    _la_buff_for_la_image = StringIO.StringIO()

    _la_buff_for_la_image.write(_la_image_from_la_url)
    _la_buff_for_la_image.seek(0)

    return _la_buff_for_la_image


def to_ascii(url):

    # open image and resize
    # experiment with aspect ratios according to font
    # a monospaced font works best
    _la_image = _url_to_img(url)

    try:
        im = Image.open(_la_image)
    except Exception, e:
        print e
        raise UnsupportedFormatException("Your file must be a valid .png image")

    im = im.resize(MAX_SIZE, Image.BILINEAR)
    im = im.convert("L")  # convert to mono

    w, h = im.size

    # now, work our way over the pixels
    # build up str
    out = ""
    for y in range(0, h):
        for x in range(0, w):
            lum = 255-im.getpixel((x, y))
            row = bisect(ZONEBOUNDS, lum)
            possibles = GREYSCALE[row]
            out = out + possibles[random.randint(0, len(possibles)-1)]
        out = out+"\n"
    return out, w, h


def to_image(url):

    img_content, w, h = to_ascii(url)

    img = Image.new('RGB', (w, h), COLOR_WHITE)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(os.getcwd() + '/font/anon.ttf', 2)

    cur_line = 0
    for line in img_content.split('\n'):
        draw.text((0, cur_line), line, font=font, fill=FILL)
        cur_line += 1
    del draw

    img.thumbnail(MAX_SIZE, Image.ANTIALIAS)
    img.save('output.png')


if __name__ == '__main__':
    url = 'http://images.wikia.com/donkeykong/images/archive/1/17/20110926232526!BananaDKCR.png'
    #url = 'http://upload.wikimedia.org/wikipedia/commons/8/87/Avatar_poe84it.png'
    to_image(url)
