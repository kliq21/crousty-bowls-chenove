"""
Génère les tailles du panneau CHENOVE détouré (fond transparent).
Source : Chenove-removebg-preview.png (fourni par Victor)
Sortie : assets/img/lieu/panneau-chenove-nobg-{480,960,1600}.webp + .png fallback
"""
from pathlib import Path
from PIL import Image, ImageOps

SRC = Path(r"C:\Users\victo\Desktop\Chenove-removebg-preview.png")
DST = Path(r"C:\Users\victo\Documents\Kliq-Clients\Crousty-Bowls-Chenove\repo\assets\img\lieu")
BASE = "panneau-chenove-nobg"
SIZES = [480, 960, 1600]

img = Image.open(SRC)
img = ImageOps.exif_transpose(img)
if img.mode != "RGBA":
    img = img.convert("RGBA")

# Trim la bounding box du contenu non-transparent pour cadrer serré
bbox = img.getbbox()
if bbox:
    img = img.crop(bbox)

w, h = img.size
print(f"Source apres trim : {w}x{h}  ratio {w/h:.2f}:1  mode {img.mode}")

DST.mkdir(parents=True, exist_ok=True)

for size in SIZES:
    if size >= max(w, h):
        resized = img
    else:
        r = size / max(w, h)
        resized = img.resize((int(w*r), int(h*r)), Image.LANCZOS)
    out = DST / f"{BASE}-{size}.webp"
    resized.save(out, "WEBP", quality=88, method=6, lossless=False)
    print(f"  {out.name:44s} {resized.size[0]}x{resized.size[1]}  {out.stat().st_size//1024} Ko")

fallback = img
if max(w, h) > 1600:
    r = 1600 / max(w, h)
    fallback = img.resize((int(w*r), int(h*r)), Image.LANCZOS)
png_out = DST / f"{BASE}.png"
fallback.save(png_out, "PNG", optimize=True)
print(f"  {png_out.name:44s} {fallback.size[0]}x{fallback.size[1]}  {png_out.stat().st_size//1024} Ko")
