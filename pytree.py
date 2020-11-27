#!/usr/bin/env python3

import fnmatch
import os
from sys import argv


COLORS = ((os.getenv("TREE_COLORS") or "") + ":" + (os.getenv("LS_COLORS") or "")).split(":")
COLORS = {pat: "=".join(col) for pat, *col in map(lambda s: s.split("="), COLORS)}


if len(argv) >= 2:
    if argv[1] != "--no-color":
        os.chdir(argv[1])
    elif len(argv) >= 3:
        os.chdir(argv[2])

color = True
if "--no-color" in argv:
    color = False

dirlist = os.listdir()


def colorof(name: str, isdir: bool) -> str:
    if isdir:
        return COLORS.get("di", "")
    else:
        for pat, col in COLORS.items():
            if fnmatch.fnmatch(name, pat):
                return col
        return ""


def printnode(depth: int, name: str, isdir: bool, color: bool):
    name_colored = f"\x1b[{colorof(name, isdir)}m{name}{'/' if isdir else ''}\x1b[m"
    if color:
        print("   "*depth + name_colored)
    else:
        print(f"{'   '*depth}{name}{'/' if isdir else ''}")


def process(path: str):
    pathl = path.split("/")
    if os.path.isdir(path):
        printnode(len(pathl) - 1, pathl[-1], True, color)
        try:
            for pos in os.listdir(path):
                process(path + "/" + pos)
        except PermissionError:
            print("   "*len(pathl) + "Permission Denied")
    else:
        printnode(len(pathl) - 1, pathl[-1], False, color)


for pos in dirlist:
    process(pos)

