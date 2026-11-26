#!/usr/bin/env python3
"""Dreamina-Downloads (~/Downloads/dreamina-…-<ID>. ….png) nach media/roh/<ID>.png einsortieren (neueste je ID)."""
import glob, os, re, shutil
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fs = sorted(glob.glob(os.path.expanduser("~/Downloads/dreamina-*.png")), key=os.path.getmtime)
seen = {}
for f in fs:
    m = re.match(r"dreamina-\d{4}-\d\d-\d\d-\d+-([A-Z]+\d)\. ", os.path.basename(f))
    # nur eigene IDs (SCHICHTWECHSEL), nie Downloads anderer Sitzungen anfassen
    if m and re.fullmatch(r"(K[0-5]|S[0-7]|M1|R[0-3]|J1|A[1-4]|AB[1-3]|P1|F1)", m.group(1)): seen[m.group(1)] = f
for k, f in seen.items():
    shutil.move(f, os.path.join(BASE, "media/roh", k + ".png")); print(k)
