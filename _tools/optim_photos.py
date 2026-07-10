"""
Optimisation photos Crousty Bowls — v3 (vraies photos gérante, 2026-07-10).
Source : C:\\Users\\victo\\Desktop\\photo crousty bowl
Mapping validé par Victor : basé sur les noms donnés + identification visuelle.
"""
from pathlib import Path
from PIL import Image, ImageOps

SRC = Path(r"C:\Users\victo\Desktop\photo crousty bowl")
DST = Path(r"C:\Users\victo\Documents\Kliq-Clients\Crousty-Bowls-Chenove\repo\assets\img")

MAPPING = {
    # LIEU / EXTÉRIEUR
    "Deventure.jpg":   ("lieu", "facade"),
    "Chenove.jpg":     ("lieu", "panneau-chenove"),

    # SALLE (privatisation)
    "Salle.jpg":       ("salle", "salle-01"),
    "IMG_1292.jpg":    ("salle", "salle-02"),
    "IMG_1294.jpg":    ("salle", "salle-03"),

    # YAKISOBA (nouilles)
    "Nouille.jpg":     ("yakisoba", "yakisoba-signature"),
    "nouille2.jpg":    ("yakisoba", "yakisoba-flyer"),
    "Nouille3.jpg":    ("yakisoba", "yakisoba-topdown"),
    "IMG_1295.jpg":    ("yakisoba", "yakisoba-flyer-2"),
    "IMG_1296.jpg":    ("yakisoba", "yakisoba-topdown-2"),
    "IMG_1298.jpg":    ("yakisoba", "yakisoba-3quart"),
    "IMG_1309.jpg":    ("yakisoba", "yakisoba-closeup"),
    "tastu2.jpg":      ("yakisoba", "yakisoba-topdown-3"),

    # POUTINE
    "Poutine.jpg":     ("poutine", "poutine-gratinee-topdown"),
    "IMG_1306.jpg":    ("poutine", "poutine-gratinee-large"),
    "IMG_1308.jpg":    ("poutine", "poutine-gratinee-side"),
    "IMG_1303.jpg":    ("poutine", "poutine-sriracha-closeup"),
    "IMG_1307.jpg":    ("poutine", "poutine-sriracha-side"),

    # CROUSTY (bowl signature — utilisé en hero)
    "Tasty.jpg":       ("crousty", "crousty-signature"),

    # BOISSONS
    "jus.jpg":         ("boissons", "matcha-duo"),

    # EXTRAS (non utilisés pour l'instant mais générés)
    "IMG_1291.jpg":    ("lieu", "frigo-boissons"),
    "IMG_1304.jpg":    ("plats", "mix-flyers"),
}

SIZES = [480, 960, 1600]
WEBP_QUALITY = 82
JPG_QUALITY = 84


def process(src_path: Path, folder: str, base: str):
    out_dir = DST / folder
    out_dir.mkdir(parents=True, exist_ok=True)

    img = Image.open(src_path)
    img = ImageOps.exif_transpose(img).convert("RGB")
    w, h = img.size

    for size in SIZES:
        if size >= max(w, h):
            resized, actual = img, f"{w}x{h}"
        else:
            r = size / max(w, h)
            resized = img.resize((int(w * r), int(h * r)), Image.LANCZOS)
            actual = f"{resized.width}x{resized.height}"

        webp_out = out_dir / f"{base}-{size}.webp"
        resized.save(webp_out, "WEBP", quality=WEBP_QUALITY, method=6)
        print(f"  {webp_out.name:38s} {actual:>10s}  {webp_out.stat().st_size // 1024:>4d} Ko")

    fallback = img
    if max(w, h) > 1600:
        r = 1600 / max(w, h)
        fallback = img.resize((int(w * r), int(h * r)), Image.LANCZOS)
    jpg_out = out_dir / f"{base}.jpg"
    fallback.save(jpg_out, "JPEG", quality=JPG_QUALITY, optimize=True, progressive=True)
    print(f"  {jpg_out.name:38s}             {jpg_out.stat().st_size // 1024:>4d} Ko")


def main():
    print(f"Source : {SRC}")
    print(f"Destination : {DST}\n")
    for src_name, (folder, base) in MAPPING.items():
        src = SRC / src_name
        if not src.exists():
            print(f"MANQUE : {src_name}")
            continue
        print(f"> {src_name} -> {folder}/{base}")
        process(src, folder, base)
        print()


if __name__ == "__main__":
    main()
