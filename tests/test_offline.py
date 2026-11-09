"""snapfind must never touch the network. A fresh process makes every socket call raise, then
imports snapfind. In CI this also runs inside a Linux network namespace with no interfaces
(SNAPFIND_EXPECT_NO_NET=1)."""

import subprocess
import sys
import textwrap

SCRIPT = textwrap.dedent(r"""
    import os, socket, sys

    if os.environ.get("SNAPFIND_EXPECT_NO_NET"):
        try:
            socket.create_connection(("1.1.1.1", 443), timeout=3).close()
            sys.exit("sandbox has network access")
        except OSError:
            pass

    def blocked(*a, **k):
        raise OSError("network access attempted: " + repr(a[:2]))

    socket.socket.connect = socket.socket.connect_ex = blocked
    socket.create_connection = socket.getaddrinfo = blocked

    import snapfind
    from snapfind.cli import main
    main([])
    print("OFFLINE OK")
""")


def test_import_with_network_blocked():
    out = subprocess.run([sys.executable, "-c", SCRIPT], capture_output=True, text=True,
                         timeout=300)
    assert out.returncode == 0, out.stdout + out.stderr
    assert "OFFLINE OK" in out.stdout
