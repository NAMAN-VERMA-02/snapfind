# Changelog

## 0.1.0 (2026-11-10)

First release.

- `snapfind index` OCRs screenshots into a local SQLite index. It finds Windows' real Screenshots folder (including OneDrive's `Screenshots 1`), works newest first, can resume after Ctrl+C, and skips OneDrive cloud-only files and files that are still being saved.
- `snapfind "query"` ranks results with FTS5 BM25 and a bundled MiniLM model (int8 ONNX), fused with Reciprocal Rank Fusion; `--mode keyword|semantic|hybrid`. Before searching, it indexes up to 20 new screenshots.
- Months in queries match dates in screenshots and the capture date ("december" finds `14/12/2026`).
- Cache: unchanged files are never re-read. Copies and renames reuse the stored text through a sha1 of their content. The same screenshot in two folders shows as one result.
- `snapfind serve`: a local web UI on 127.0.0.1 with a Host-header check and id-only image URLs.
- `snapfind watch`, `forget`, `reset`, `--exclude`.
- No network calls at runtime. A test proves this with sockets blocked, and CI also runs it inside a Linux network namespace.
- Eval set (100 labelled screenshots plus 100 hard negatives) with a runner and a manual CI workflow. Top-3: keyword 75, semantic 95, hybrid 89.

### Fixed during development
- Stopwords flooded the keyword list and hurt hybrid ranking on paraphrase queries (#6, fixed in #7).
- OCR skips the text-angle classifier, which is never needed for screenshots (#4).
