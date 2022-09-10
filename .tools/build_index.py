#!/usr/bin/env python3
import hashlib
import json
import os
import sys


index = {}

ROOT = "."


def hash_file(f):
    h = hashlib.sha256()
    while True:
        buf = f.read(8196)
        if not buf:
            break
        h.update(buf)
    return h.hexdigest()


for (dirpath, dirnames, filenames) in os.walk(ROOT):
    if dirpath == ROOT:
        dirnames[:] = [dirname for dirname in dirnames if dirname[0] != "."]
        continue
    path = os.path.normpath(os.path.relpath(dirpath, ROOT)).split(os.path.sep)
    e = index
    for part in path:
        e = e.setdefault(part, {})
    for filename in filenames:
        with open(os.path.join(*[*path, filename]), "rb") as f:
            e[filename] = hash_file(f)


json.dump(index, sys.stdout, indent=1)
