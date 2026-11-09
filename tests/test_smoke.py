import subprocess
import sys

import snapfind


def test_version_flag():
    out = subprocess.run([sys.executable, "-m", "snapfind", "--version"], capture_output=True,
                         text=True)
    assert out.stdout.strip() == f"snapfind {snapfind.__version__}"
