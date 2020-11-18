#!/usr/bin/env python3
#!/usr/bin/env python

import os
from sys import argv

if len(argv) >= 2:
    os.chdir(argv[1])

dirlist = os.listdir()

def process(path: str):
    pathl = path.split("/")
    if os.path.isdir(path):
        print("   "*(len(pathl)-1) + pathl[len(pathl)-1] + "/")
        try:
            for pos in os.listdir(path):
                process(path + "/" + pos)
        except PermissionError:
            print("   "*len(pathl) + "Permission Denied")
    else:
        print("   "*(len(pathl)-1) + pathl[len(pathl)-1])


for pos in dirlist:
    process(pos)
