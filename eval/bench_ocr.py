"""Compare RapidOCR settings for speed (s/image) and word recall on the synthetic eval images.

    python eval/bench_ocr.py IMAGE... [--real]

With --real only timings are printed (for private screenshots: no text is shown or saved).
"""

import argparse
import re
import statistics
import sys
import time
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

CONFIGS = {
    "v6-small (default)": {},
    "v6-small, no cls": {"Global.use_cls": False},
    "v6-small, no cls, det 1280": {"Global.use_cls": False, "Global.max_side_len": 1280},
}
if V4 := __import__("os").environ.get("V4_DIR"):  # PP-OCRv4 mobile models, for comparison only
    from rapidocr import ModelType, OCRVersion

    CONFIGS["v4-mobile, no cls"] = {
        "Global.use_cls": False,
        "Det.ocr_version": OCRVersion.PPOCRV4, "Det.model_type": ModelType.MOBILE,
        "Det.model_path": f"{V4}/ch_PP-OCRv4_det_infer.onnx",
        "Rec.ocr_version": OCRVersion.PPOCRV4, "Rec.model_type": ModelType.MOBILE,
        "Rec.model_path": f"{V4}/ch_PP-OCRv4_rec_infer.onnx"}


def ground_truth() -> dict[str, set[str]]:
    from make_dataset import pad_tall, variants
    from screens import S
    from templates import RENDER

    gt = {}
    for spec in S:
        for v in variants(spec):
            html = RENDER[v["t"]](pad_tall(v) if v.get("hard") == "tall" else v)
            text = re.sub(r"<[^>]+>", " ", html)
            gt[v["id"]] = set(re.findall(r"[a-z0-9]{3,}", text.lower()))
    return gt


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("images", nargs="+")
    ap.add_argument("--real", action="store_true")
    ap.add_argument("--configs", nargs="*", default=list(CONFIGS))
    args = ap.parse_args()
    from rapidocr import RapidOCR

    gt = {} if args.real else ground_truth()
    imgs = [(Path(p).stem, np.asarray(Image.open(p).convert("RGB"))[:, :, ::-1].copy())
            for p in args.images]
    for name in args.configs:
        t = time.perf_counter()
        eng = RapidOCR(params={"Global.log_level": "error", **CONFIGS[name]})
        load = time.perf_counter() - t
        times, recalls = [], []
        for stem, img in imgs:
            t = time.perf_counter()
            out = eng(img)
            times.append(time.perf_counter() - t)
            if stem in gt:
                words = set(re.findall(r"[a-z0-9]{3,}", " ".join(out.txts or ()).lower()))
                recalls.append(len(gt[stem] & words) / max(1, len(gt[stem])))
        rec = f"  word recall {statistics.mean(recalls):.3f}" if recalls else ""
        print(f"{name:32} load {load:5.1f}s  {statistics.mean(times):5.2f} s/img "
              f"(median {statistics.median(times):.2f}, n={len(times)}){rec}", flush=True)


if __name__ == "__main__":
    main()
