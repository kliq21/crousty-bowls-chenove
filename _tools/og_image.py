"""Génère og-image.jpg 1200x630 pour le vrai site — palette dark #0A0A0F + tomato."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

SRC = Path(r"C:\Users\victo\Desktop\photo crousty bowl\IMG_1308.jpg")
OUT = Path(r"C:\Users\victo\Documents\Kliq-Clients\Crousty-Bowls-Chenove\repo\og.jpg")

W, H = 1200, 630
INK = (10, 10, 15)
TOMATO = (230, 57, 70)
WHITE = (255, 255, 255)

canvas = Image.new("RGB", (W, H), INK)

img = ImageOps.exif_transpose(Image.open(SRC)).convert("RGB")
sw, sh = img.size
target_ratio = H / H
photo_w, photo_h = 600, 630
r = photo_w / sw
new_h = int(sh * r)
img = img.resize((photo_w, new_h), Image.LANCZOS)
if new_h > photo_h:
    top = (new_h - photo_h) // 2
    img = img.crop((0, top, photo_w, top + photo_h))
canvas.paste(img, (600, 0))

overlay = Image.new("RGBA", (photo_w, photo_h), (0, 0, 0, 0))
draw_ov = ImageDraw.Draw(overlay)
for x in range(photo_w):
    alpha = int(220 * ((photo_w - x) / photo_w) ** 2.5)
    draw_ov.line([(x, 0), (x, photo_h)], fill=(10, 10, 15, alpha))
canvas.paste(overlay, (600, 0), overlay)

draw = ImageDraw.Draw(canvas)

def font(size, name):
    for base in [r"C:\Windows\Fonts", r"C:\WINDOWS\Fonts"]:
        p = Path(base) / name
        if p.exists():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()

f_eyebrow = font(22, "arialbd.ttf")
f_poster1 = font(150, "impact.ttf")
f_poster2 = font(150, "impact.ttf")
f_sub = font(24, "arial.ttf")
f_tag = font(18, "arialbd.ttf")

x = 60
draw.line([(x, 100), (x + 60, 100)], fill=TOMATO, width=3)
draw.text((x + 76, 88), "CHENÔVE · 21300", font=f_eyebrow, fill=(255, 255, 255, 255))

y = 140
draw.text((x, y), "CROUSTY", font=f_poster1, fill=WHITE)
y += 145
draw.text((x, y), "BOWLS", font=f_poster2, fill=TOMATO)

y += 175
draw.text((x, y), "Le bowl croustillant à Chenôve.", font=f_sub, fill=(255, 255, 255, 220))
y += 34
draw.text((x, y), "Halal · Livraison Dijon · Ouvert 7j/7", font=f_sub, fill=(180, 180, 190))

tag_y = 555
for i, tag in enumerate(["BOWLS", "POUTINES", "YAKISOBA", "SUSHIS"]):
    tx = x + i * 130
    draw.rectangle([(tx, tag_y), (tx + 110, tag_y + 30)], outline=TOMATO, width=2)
    tw = draw.textlength(tag, font=f_tag)
    draw.text((tx + (110 - tw) / 2, tag_y + 6), tag, font=f_tag, fill=TOMATO)

canvas.save(OUT, "JPEG", quality=88, optimize=True, progressive=True)
print(f"OK {OUT} ({OUT.stat().st_size // 1024} Ko, {W}x{H})")
