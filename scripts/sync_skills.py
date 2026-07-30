#!/usr/bin/env python3
"""Sync skills from this repo into ~/.claude/skills.

The repo is the source of truth; ~/.claude/skills is a working copy. Every
replaced directory is backed up first, so this is always reversible.

Dry-run by default. Nothing is written without --apply.

    python3 scripts/sync_skills.py              # show what would change
    python3 scripts/sync_skills.py --apply      # do it, backing up first
    python3 scripts/sync_skills.py --apply --only context-graph

Python 3 standard library only. No network.
"""

import argparse
import datetime as dt
import filecmp
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, ".claude", "skills")
DEST = os.path.expanduser("~/.claude/skills")


def tree(path):
    out = {}
    for dirpath, dirnames, filenames in os.walk(path):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for name in filenames:
            full = os.path.join(dirpath, name)
            out[os.path.relpath(full, path)] = full
    return out


def compare(src_dir, dest_dir):
    """Return (added, changed, removed) relative paths."""
    src, dest = tree(src_dir), tree(dest_dir) if os.path.isdir(dest_dir) else {}
    added = sorted(set(src) - set(dest))
    removed = sorted(set(dest) - set(src))
    changed = sorted(
        rel for rel in set(src) & set(dest)
        if not filecmp.cmp(src[rel], dest[rel], shallow=False))
    return added, changed, removed


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--apply", action="store_true", help="write changes (default: dry run)")
    parser.add_argument("--only", action="append", help="limit to named skill(s)")
    parser.add_argument("--dest", default=DEST)
    args = parser.parse_args(argv)

    if not os.path.isdir(SRC):
        print("ERROR no skills directory at %s" % SRC)
        return 1

    names = sorted(d for d in os.listdir(SRC) if os.path.isdir(os.path.join(SRC, d)))
    if args.only:
        wanted = set(args.only)
        missing = wanted - set(names)
        if missing:
            print("ERROR unknown skill(s): %s" % ", ".join(sorted(missing)))
            return 1
        names = [n for n in names if n in wanted]

    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_root = os.path.join(args.dest, ".backup-%s" % stamp)
    pending, backed_up = [], False

    for name in names:
        src_dir = os.path.join(SRC, name)
        dest_dir = os.path.join(args.dest, name)
        added, changed, removed = compare(src_dir, dest_dir)
        if not (added or changed or removed):
            print("  ok       %s" % name)
            continue
        pending.append(name)
        state = "new" if not os.path.isdir(dest_dir) else "update"
        print("  %-8s %s  (+%d ~%d -%d)" % (state, name, len(added), len(changed), len(removed)))
        for rel in changed:
            print("             ~ %s" % rel)
        for rel in removed:
            print("             - %s (in ~/.claude only; will be removed)" % rel)

    if not pending:
        print("\nNothing to sync -- %d skills already match." % len(names))
        return 0

    if not args.apply:
        print("\n%d skill(s) would change. Re-run with --apply to write." % len(pending))
        print("Nothing has been modified.")
        return 0

    os.makedirs(args.dest, exist_ok=True)
    for name in pending:
        src_dir = os.path.join(SRC, name)
        dest_dir = os.path.join(args.dest, name)
        if os.path.isdir(dest_dir):
            os.makedirs(backup_root, exist_ok=True)
            shutil.copytree(dest_dir, os.path.join(backup_root, name))
            backed_up = True
            shutil.rmtree(dest_dir)
        shutil.copytree(src_dir, dest_dir)
        print("  synced   %s" % name)

    print("\nSynced %d skill(s)." % len(pending))
    if backed_up:
        print("Previous versions backed up to %s" % backup_root)
        print("To undo: remove the synced directories and copy them back from there.")
    print("\nNote: ~/.claude/skills/manifest.json is left untouched, so claude.ai sync")
    print("keeps its skillId mappings. Skills authored here that claude.ai has never")
    print("seen will not appear on mobile until they are added there too.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
