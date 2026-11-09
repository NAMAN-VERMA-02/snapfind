"""Sentence vectors from the bundled MiniLM (int8 ONNX), loaded from disk, never the network."""

from pathlib import Path

import numpy as np

MODEL_DIR = Path(__file__).parent / "model"
DIM = 384
_session = _tokenizer = None


def _load():
    global _session, _tokenizer
    if _session is None:
        import onnxruntime as ort
        from tokenizers import Tokenizer

        tok = Tokenizer.from_file(str(MODEL_DIR / "tokenizer.json"))
        tok.enable_truncation(256)
        tok.enable_padding()
        _tokenizer = tok
        _session = ort.InferenceSession(str(MODEL_DIR / "model_quantized.onnx"),
                                        providers=["CPUExecutionProvider"])
    return _session, _tokenizer


def embed(texts: list[str]) -> np.ndarray:
    """L2-normalised mean-pooled vectors, shape (len(texts), 384), float32."""
    session, tok = _load()
    enc = tok.encode_batch(texts)
    ids = np.array([e.ids for e in enc], dtype=np.int64)
    mask = np.array([e.attention_mask for e in enc], dtype=np.int64)
    hidden = session.run(None, {"input_ids": ids, "attention_mask": mask,
                                "token_type_ids": np.zeros_like(ids)})[0]
    m = mask[..., None].astype(np.float32)
    v = (hidden * m).sum(1) / np.clip(m.sum(1), 1e-9, None)
    return (v / np.clip(np.linalg.norm(v, axis=1, keepdims=True), 1e-12, None)).astype(np.float32)


def chunks(text: str, size: int = 64, stride: int = 48) -> list[str]:
    """Overlapping word windows, so text deep in a long chat still gets its own vector."""
    words = text.split()
    if not words:
        return []
    starts = range(0, max(1, len(words) - size + stride), stride)
    return [" ".join(words[i:i + size]) for i in starts]
