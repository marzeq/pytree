#!/usr/bin/env python3

import fnmatch
import os
from sys import argv


COLORS = ((os.getenv("TREE_COLORS") or "") + ":" + (os.getenv("LS_COLORS") or "")).split(":")
COLORS = {pat: "=".join(col) for pat, *col in map(lambda s: s.split("="), COLORS)}


if len(argv) >= 2:
    os.chdir(argv[1])

dirlist = os.listdir()


def colorof(name: str, isdir: bool) -> str:
    if isdir:
        return COLORS.get("di", "")
    else:
        for pat, col in COLORS.items():
            if fnmatch.fnmatch(name, pat):
                return col
        return ""


def printnode(depth: int, name: str, isdir: bool):
    name_colored = f"\x1b[{colorof(name, isdir)}m{name}{'/' if isdir else ''}\x1b[m"
    print("   "*depth + name_colored)


def process(path: str):
    pathl = path.split("/")
    if os.path.isdir(path):
        printnode(len(pathl) - 1, pathl[-1], True)
        try:
            for pos in os.listdir(path):
                process(path + "/" + pos)
        except PermissionError:
            print("   "*len(pathl) + "Permission Denied")
    else:
        printnode(len(pathl) - 1, pathl[-1], False)


for pos in dirlist:
    process(pos)
