"""
Crop du panneau CHENOVE : vire le mur blanc au-dessus et le bas pour ne garder que le panneau + un peu de rainures noires autour.
Régénère ensuite les 3 tailles WebP + JPG dans assets/img/lieu/panneau-chenove.*
"""
from pathlib import Path
from PIL import Image, ImageOps

SRC = Path(r"C:\Users\victo\Desktop\photo crousty bowl\Chenove.jpg")
DST = Path(r"C:\Users\victo\Documents\Kliq-Clients\Crousty-Bowls-Chenove\repo\assets\img\lieu")
BASE = "panneau-chenove"
SIZES = [480, 960, 1600]

img = Image.open(SRC)
img = ImageOps.exif_transpose(img).convert("RGB")
w, h = img.size
print(f"Source : {w}x{h}")

# Crop centré sur le panneau : haut à 26%, bas à 72%, largeur pleine avec 2% de marge lat.
left   = int(w * 0.02)
right  = int(w * 0.98)
top    = int(h * 0.26)
bottom = int(h * 0.72)
cropped = img.crop((left, top, right, bottom))
cw, ch = cropped.size
print(f"Crop   : {cw}x{ch}  ratio {cw/ch:.2f}:1")

DST.mkdir(parents=True, exist_ok=True)

for size in SIZES:
    if size >= max(cw, ch):
        resized = cropped
    else:
        r = size / max(cw, ch)
        resized = cropped.resize((int(cw*r), int(ch*r)), Image.LANCZOS)
    out = DST / f"{BASE}-{size}.webp"
    resized.save(out, "WEBP", quality=82, method=6)
    print(f"  {out.name:36s} {resized.size[0]}x{resized.size[1]}  {out.stat().st_size//1024} Ko")

fallback = cropped
if max(cw, ch) > 1600:
    r = 1600 / max(cw, ch)
    fallback = cropped.resize((int(cw*r), int(ch*r)), Image.LANCZOS)
jpg = DST / f"{BASE}.jpg"
fallback.save(jpg, "JPEG", quality=84, optimize=True, progressive=True)
print(f"  {jpg.name:36s} {fallback.size[0]}x{fallback.size[1]}  {jpg.stat().st_size//1024} Ko")
