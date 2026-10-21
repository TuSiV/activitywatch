#!/usr/bin/env python3
"""Apply the reviewed web UI overlay to initialized server submodules.

Submodule pointers remain upstream-owned. Hash checks prevent overwriting a
changed upstream file or local edit. All targets are validated before any write.
Use --webui PATH to develop/build just one checkout; --check verifies the overlay
is already applied. Repeated application is safe.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
OVERLAY = ROOT / 'ui-overrides'


def digest(path: Path) -> str | None:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def apply(targets: list[Path], check: bool = False) -> int:
    manifest = json.loads((OVERLAY / 'manifest.json').read_text())
    pending = []
    for target in targets:
        if not (target / 'package.json').is_file():
            raise ValueError(f'Web UI not initialized: {target}')
        for name, hashes in manifest.items():
            relative = Path(name)
            if relative.is_absolute() or '..' in relative.parts:
                raise ValueError(f'Invalid overlay path: {name}')
            source, dest = OVERLAY / relative, target / relative
            if digest(source) != hashes['replacement']:
                raise ValueError(f'Overlay checksum mismatch: {name}')
            current = digest(dest)
            if current == hashes['replacement']:
                continue
            if current != hashes['original']:
                raise ValueError(f'Upstream/local file changed: {dest}; review the overlay before building')
            if check:
                raise ValueError(f'Overlay not applied: {dest}')
            pending.append((source, dest))
    for source, dest in pending:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(source.read_bytes())
    return len(pending)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--webui', type=Path, action='append', help='explicit web UI checkout (repeatable)')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    targets = args.webui or [p for p in (
        ROOT / 'aw-server/aw-webui', ROOT / 'aw-server-rust/aw-webui',
        ROOT / 'aw-tauri/aw-server/aw-webui',
        ROOT / 'aw-tauri/src-tauri/aw-server/aw-webui',
    ) if (p / 'package.json').is_file()]
    if not targets:
        parser.error('No initialized web UI found; run git submodule update --init --recursive')
    try:
        count = apply(targets, args.check)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f'Workspace theme verified in {len(targets)} checkout(s); {count} file(s) updated')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
