"""snapfind command line."""

import argparse

from snapfind import __version__


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="snapfind",
                                description="Search your screenshots by the text in them, offline.")
    p.add_argument("--version", action="version", version=f"snapfind {__version__}")
    return p


def main(argv: list[str] | None = None) -> int:
    build_parser().parse_args(argv)
    print("snapfind: indexing and search are coming in the next release.")
    return 0
