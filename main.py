#!/usr/bin/env python3
"""Copy entry.png to the output directory, byte for byte.

Standard library only, no network. The output directory is
$MAKEFUN_OUTPUT_DIR when set, otherwise /output. The source image sits
next to this file in the repository.
"""

import os
import shutil
from pathlib import Path


def main():
    here = Path(__file__).resolve().parent
    src = here / "entry.png"
    if not src.is_file():
        raise FileNotFoundError(f"entry.png not found next to main.py: {src}")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dst = out_dir / "entry.png"
    shutil.copyfile(src, dst)
    # The copy must be exact: same size, or the grading runs disagree.
    if dst.stat().st_size != src.stat().st_size:
        raise IOError(f"copy size mismatch: {src.stat().st_size} -> "
                      f"{dst.stat().st_size}")
    print(f"copied {src} -> {dst} ({dst.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
