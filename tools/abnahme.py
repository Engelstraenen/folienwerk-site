#!/usr/bin/env python3
"""Abnahme-Bilder: je Storyboard-Panel (3x3) das Panel + Seite Laptop + Seite Handy -> abnahme/<n>-*.jpg"""
import asyncio, os
from playwright.async_api import async_playwright
from PIL import Image
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SB = os.path.join(BASE, 'konzepte/v3/1-musterfaecher.png'); OUT = os.path.join(BASE, 'abnahme/')
URL = 'http://localhost:4482/'
# (Abschnitt, Anteil der Scrollstrecke im Abschnitt)
CH = [("duo", .02), ("duo", .84), ("wissen", .55), ("handwerk", .5), ("referenzen", .0), ("alles", .62), ("konfigurator", .25), ("karriere", .7), ("angebot", .3)]
os.makedirs(OUT, exist_ok=True)
sb = Image.open(SB).convert('RGB'); W, H = sb.size; pw, ph = W / 3, H / 3
for i in range(9):
    r, c = divmod(i, 3); sb.crop((int(c * pw), int(r * ph), int((c + 1) * pw), int((r + 1) * ph))).save(f'{OUT}{i+1}-storyboard.jpg', quality=90)
JS = "([id,f])=>{const s=document.getElementById(id);const h=Math.max(0,s.offsetHeight-innerHeight);scrollTo(0,s.offsetTop+h*f)}"
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for tag, w, h, mob in (("desktop", 1600, 900, False), ("handy", 390, 844, True)):
            pg = await b.new_page(viewport={"width": w, "height": h}, device_scale_factor=2 if mob else 1, is_mobile=mob, has_touch=mob)
            await pg.goto(URL); await pg.wait_for_timeout(2500)
            for i, (sid, f) in enumerate(CH):
                await pg.evaluate(JS, [sid, f]); await pg.wait_for_timeout(1600)
                await pg.evaluate(JS, [sid, f]); await pg.wait_for_timeout(900)
                await pg.screenshot(path=f'{OUT}{i+1}-{tag}.jpg', type='jpeg', quality=82)
        await b.close()
asyncio.run(main())
print('ok')
