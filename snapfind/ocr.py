"""Text from an image with RapidOCR. Its ONNX models ship inside the rapidocr wheel."""

import math
import re

_engine = None
_CAMEL = re.compile(r"\b\w*[a-z][A-Z]\w*\b")


def _get():
    global _engine
    if _engine is None:
        from rapidocr import RapidOCR

        # Screenshots are upright, so the text-angle classifier only costs time
        # (eval/bench_ocr.py: about 14% faster, same word recall on the eval images).
        _engine = RapidOCR(params={"Global.log_level": "error", "Global.use_cls": False})
    return _engine


def slice_tops(w: int, h: int) -> list[int]:
    """Top edges of evenly spaced slices, each 2*w tall, overlapping by at least 10%, the last
    one ending at the bottom. RapidOCR shrinks the long side to 2000 px, which would make the
    text in a tall scroll capture unreadable."""
    span = 2 * w
    if h <= span:
        return [0]
    n = math.ceil((h - span) / (0.9 * span)) + 1
    return [round(i * (h - span) / (n - 1)) for i in range(n)]


def read_text(path: str) -> str:
    import numpy as np
    from PIL import Image

    with Image.open(path) as im:
        img = im.convert("RGB")
    w, h = img.size
    lines: list[str] = []
    for top in slice_tops(w, h):
        part = np.asarray(img.crop((0, top, w, min(h, top + 2 * w))))[:, :, ::-1]  # to BGR
        lines += _get()(np.ascontiguousarray(part)).txts or ()
    return "\n".join(lines)


def split_joined(text: str) -> str:
    """OCR often glues neighbouring UI labels: 'E-TicketPNR'. Return 'Ticket PNR' style splits
    to index next to the original, so both 'ticketpnr' and 'ticket' match."""
    return " ".join(re.sub(r"(?<=[a-z])(?=[A-Z])", " ", w) for w in _CAMEL.findall(text))
