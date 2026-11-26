#!/usr/bin/env python3
"""Rohbilder (media/roh/*.png) -> nachgeschärfte WebP in site/assets/img/.
- Varianten K1–K5 / S1–S7 werden per ECC (affin) deckungsgleich auf K0 / S0 ausgerichtet (für den Wischer).
- Schärfen: Unsharp-Mask radius 1.6, 70 %, Schwelle 2 (Masterfile V2.65); Laplace-Varianz vorher/nachher wird ausgegeben.
- Cache: unveränderte Quellen werden übersprungen.
Start: python3 tools/assets_v3.py [ID ...]"""
import json, os, sys
import cv2, numpy as np
from PIL import Image, ImageFilter

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW, OUT = os.path.join(BASE, "media/roh"), os.path.join(BASE, "site/assets/img")
CACHE = os.path.join(BASE, "media/.assets_cache.json")
# ID -> (Dateiname, Breiten)
SPEC = {}
for i in range(6): SPEC[f"K{i}"] = (f"k{i}", [2560, 1600])
for i in range(8): SPEC[f"S{i}"] = (f"s{i}", [2400])
SPEC.update({"M1": ("m1", [2560, 1600]), "R0": ("r0", [2560]), "J1": ("j1", [2560]),
             "R1": ("r1", [1920]), "R2": ("r2", [1920]), "R3": ("r3", [1920]),
             "A1": ("a1", [1200]), "A2": ("a2", [1200]), "A3": ("a3", [1200]), "A4": ("a4", [1200]),
             "AB1": ("ab1", [1920]), "AB2": ("ab2", [1920]), "AB3": ("ab3", [1920]), "P1": ("p1", [1920]), "F1": ("f1", [1920])})
FLIP = {"M1"}  # Motiv nach rechts, Text steht links
ALIGN = {**{f"K{i}": "K0" for i in range(1, 6)}, **{f"S{i}": "S0" for i in range(1, 8)}}

def lap(im):
    g = cv2.cvtColor(np.asarray(im.convert("RGB")), cv2.COLOR_RGB2GRAY)
    return cv2.Laplacian(g, cv2.CV_64F).var()

def align(src, ref):
    """affine ECC auf verkleinerten Graubildern, dann auf volle Größe anwenden"""
    a = np.asarray(ref.convert("RGB")); b = np.asarray(src.convert("RGB").resize(ref.size, Image.LANCZOS))
    s = 960 / a.shape[1]
    ga = cv2.cvtColor(cv2.resize(a, None, fx=s, fy=s), cv2.COLOR_RGB2GRAY).astype(np.float32)
    gb = cv2.cvtColor(cv2.resize(b, None, fx=s, fy=s), cv2.COLOR_RGB2GRAY).astype(np.float32)
    w = np.eye(2, 3, dtype=np.float32)
    try:
        cc, w = cv2.findTransformECC(ga, gb, w, cv2.MOTION_AFFINE, (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-6), None, 5)
    except cv2.error:
        return Image.fromarray(b), None
    w[:, 2] /= s
    out = cv2.warpAffine(b, w, (a.shape[1], a.shape[0]), flags=cv2.INTER_LANCZOS4 + cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REFLECT)
    return Image.fromarray(out), (float(cc), float(w[0, 2]), float(w[1, 2]))

def main():
    want = set(sys.argv[1:])
    cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    for k, (name, widths) in SPEC.items():
        p = os.path.join(RAW, k + ".png")
        if not os.path.exists(p) or (want and k not in want): continue
        st = os.stat(p); key = f"{st.st_mtime}-{st.st_size}-{widths}"
        if cache.get(k) == key and not want: continue
        im = Image.open(p).convert("RGB")
        if k in FLIP: im = im.transpose(Image.FLIP_LEFT_RIGHT)
        info = ""
        if k in ALIGN and os.path.exists(os.path.join(RAW, ALIGN[k] + ".png")):
            im, r = align(im, Image.open(os.path.join(RAW, ALIGN[k] + ".png")).convert("RGB"))
            info = f" ECC cc={r[0]:.3f} dx={r[1]:.1f} dy={r[2]:.1f}" if r else " ECC fehlgeschlagen"
        l0 = lap(im)
        sh = im.filter(ImageFilter.UnsharpMask(radius=1.6, percent=70, threshold=2))
        for i, w in enumerate(widths):
            t = sh if sh.width <= w else sh.resize((w, round(sh.height * w / sh.width)), Image.LANCZOS)
            fn = name + ("" if i == 0 else f"-{w}") + ".webp"
            t.save(os.path.join(OUT, fn), "WEBP", quality=84, method=6)
        print(f"{k}: {im.size[0]}x{im.size[1]} Schärfe {l0:.0f} -> {lap(sh):.0f}{info}")
        cache[k] = key
    json.dump(cache, open(CACHE, "w"))

main()
