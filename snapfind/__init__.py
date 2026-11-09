"""snapfind: search your screenshots by the text in them, fully offline."""

import os

# Backstop: nothing in snapfind uses the HF hub, but if a dependency ever does, keep it offline.
os.environ.setdefault("HF_HUB_OFFLINE", "1")

__version__ = "0.1.0"
