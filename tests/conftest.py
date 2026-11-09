import os
import time

import pytest
from PIL import Image, ImageDraw, ImageFont

from snapfind import db


def make_shot(path, lines, size=(1100, 700), font_size=30):
    """A plain screenshot-like PNG with the given lines of text, old enough to be indexed."""
    img = Image.new("RGB", size, "white")
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default(size=font_size)
    for i, line in enumerate(lines):
        draw.text((50, 50 + i * int(font_size * 1.8)), line, fill=(20, 20, 20), font=font)
    img.save(path)
    age(path)
    return str(path)


def age(path, seconds=3600):
    t = time.time() - seconds
    os.utime(path, (t, t))


@pytest.fixture
def con(tmp_path):
    c = db.connect(tmp_path / "index.db")
    yield c
    c.close()
