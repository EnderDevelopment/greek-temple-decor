#!/usr/bin/env python3
"""
Texture generator for the Greek Temple Decorations Bedrock addon.

Generates the white/cream marble textures (with carved relief shading) used by
the custom blocks and the Zeus statue. Run:  python tools/generate_textures.py

Outputs PNG files directly into GreekTemple_RP/textures/blocks/.
Requires: Pillow  (pip install Pillow)
"""
import os
from PIL import Image, ImageDraw

OUT = os.path.join(os.path.dirname(__file__), "..", "GreekTemple_RP", "textures", "blocks")
os.makedirs(OUT, exist_ok=True)

# ---------- Marble base ----------
BASE = (233, 230, 224)      # warm white/cream marble
SHADE = (196, 190, 182)     # cool shadow grey (carved recess)
HIGHLIGHT = (248, 246, 242) # sculpted highlight
CREAM = (225, 216, 198)     # cream accent

SIZE = 64  # texture resolution


def marble_base(size=SIZE):
    """Return a base image textured with subtle marble veining."""
    img = Image.new("RGB", (size, size), BASE)
    px = img.load()
    for y in range(size):
        for x in range(size):
            r, g, b = px[x, y]
            # gentle noise + horizontal-ish veins
            import random
            random.seed((x * 31 + y * 17) & 0xFFFFFFFF)
            n = random.randint(-6, 6)
            vein = 0
            if random.randint(0, 12) == 0:
                vein = random.randint(-22, -8)
            px[x, y] = (r + n + vein, g + n + vein, b + n + vein)
    return img


def carve(draw, shape, fill=SHADE, outline=HIGHLIGHT):
    """Draw a carved shape with an offset shadow so it reads as a deep relief."""
    draw.polygon(shape, fill=fill)
    # highlight edge (top-left) to suggest caught light
    hl = [(x - 1, y - 1) for x, y in shape]
    draw.polygon(hl, outline=outline)


def save(img, name):
    img.save(os.path.join(OUT, name + ".png"))
    print("wrote", name + ".png")


# ---------- Zeus marble (large sculpting surface) ----------
def zeus_marble():
    img = marble_base(128)
    save(img, "zeus_marble")


# ---------- Greek meander (Greek key) ----------
def meander():
    img = marble_base()
    d = ImageDraw.Draw(img)
    s = SIZE
    # continuous Greek-key frets along the middle band
    band = 16
    y0 = s // 2 - band // 2
    i = 0
    step = 16
    while i * step < s:
        x = i * step
        carve(d, [(x + 2, y0), (x + step - 2, y0),
                  (x + step - 2, y0 + band // 2), (x + step // 2, y0 + band // 2),
                  (x + step // 2, y0 + band - 2), (x + 2, y0 + band - 2), (x + 2, y0)])
        # hook linking into neighbouring fret
        if i % 2 == 0:
            carve(d, [(x + step - 2, y0 + band // 2), (x + step + 10, y0 + band // 2),
                      (x + step + 10, y0 + band - 2), (x + step - 2, y0 + band - 2)])
        i += 1
    # top and bottom guide lines
    d.rectangle([0, y0 - 3, s, y0 - 2], fill=SHADE)
    d.rectangle([0, y0 + band + 2, s, y0 + band + 3], fill=SHADE)
    save(img, "marble_meander")


# ---------- Greek warrior (shield + spear) ----------
def warrior():
    img = marble_base()
    d = ImageDraw.Draw(img)
    s = SIZE
    cx, cy = s // 2, s // 2
    # round shield
    d.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], fill=BASE,
              outline=SHADE, width=3)
    d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], outline=SHADE, width=2)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=SHADE)
    # spear (vertical) behind the shield
    d.rectangle([cx - 27, cy - 2, cx - 20, cy + 2], fill=SHADE)
    d.polygon([(cx - 29, cy - 8), (cx - 18, cy - 8), (cx - 23.5, cy - 20)], fill=SHADE)
    # helmet crest
    carve(d, [(cx + 6, cy - 22), (cx + 26, cy - 6), (cx + 22, cy - 2), (cx + 8, cy - 12)])
    # statue plinth
    d.rectangle([cx - 28, cy + 22, cx + 28, cy + 25], fill=SHADE)
    save(img, "marble_warrior")


# ---------- Citizens in ceremonial procession ----------
def procession():
    img = marble_base()
    d = ImageDraw.Draw(img)
    s = SIZE
    base_y = s - 10
    # three simplified robed figures in a row
    for i, bx in enumerate([12, 32, 52]):
        # robed body (trapezoid)
        d.polygon([(bx - 7, base_y), (bx + 7, base_y),
                   (bx + 4, base_y - 26), (bx - 4, base_y - 26)], fill=SHADE)
        # head
        d.ellipse([bx - 4, base_y - 36, bx + 4, base_y - 28], fill=SHADE)
        # ceremonial staff / offering held forward
        if i != 1:
            d.rectangle([bx + 4, base_y - 24, bx + 6, base_y - 6], fill=SHADE)
        else:
            d.rectangle([bx - 6, base_y - 24, bx - 4, base_y - 6], fill=SHADE)
    # ground line frieze
    d.rectangle([0, base_y, s, base_y + 2], fill=SHADE)
    save(img, "marble_procession")


# ---------- Horses and chariot relief ----------
def chariot():
    img = marble_base()
    d = ImageDraw.Draw(img)
    s = SIZE
    gx = s // 2 - 4
    gy = s // 2 + 2
    # chariot box
    d.polygon([(gx - 20, gy + 8), (gx + 12, gy + 8),
               (gx + 8, gy - 6), (gx - 22, gy - 4)], fill=SHADE)
    # wheel (carved circle)
    d.ellipse([gx + 16, gy - 16, gx + 28, gy - 4], outline=SHADE, width=3)
    # horse body (galloping)
    carve(d, [(gx - 26, gy - 10), (gx - 4, gy - 16), (gx - 2, gy - 4),
              (gx - 24, gy - 2)])
    # horse neck + head
    carve(d, [(gx - 4, gy - 16), (gx + 4, gy - 26), (gx + 10, gy - 24),
              (gx + 2, gy - 12)])
    # legs
    for lx in [gx - 22, gx - 16, gx - 10, gx - 4]:
        d.rectangle([lx, gy, lx + 2, gy + 10], fill=SHADE)
    # driver
    d.ellipse([gx - 18, gy - 20, gx - 8, gy - 10], fill=SHADE)
    save(img, "marble_chariot")


# ---------- Acanthus leaf ornament ----------
def acanthus():
    img = marble_base()
    d = ImageDraw.Draw(img)
    s = SIZE
    cx, cy = s // 2, s // 2 + 6
    # a stylised acanthus leaf: a fan of curling fronds
    for ang in range(-60, 60, 15):
        import math
        rad = math.radians(ang)
        # frond from the base curling outward
        pts = []
        for t in range(0, 22):
            L = 4 + t * 1.4
            px = cx + math.sin(rad) * L + t * 0.6
            py = cy - math.cos(rad) * L
            pts.append((px, py))
        d.line(pts, fill=SHADE, width=3)
    # central vein
    d.line([(cx, cy), (cx, cy - 26)], fill=SHADE, width=3)
    # leaf base cup
    d.arc([cx - 14, cy - 4, cx + 14, cy + 14], 180, 360, fill=SHADE, width=3)
    save(img, "marble_acanthus")


# ---------- Floral and vine patterns ----------
def floral():
    img = marble_base()
    d = ImageDraw.Draw(img)
    s = SIZE
    cx, cy = s // 2, s // 2
    # winding vine
    import math
    vine_pts = []
    for t in range(0, s, 4):
        y = cy + math.sin(t / 6.0) * 12
        vine_pts.append((t, y))
    d.line(vine_pts, fill=SHADE, width=3)
    # blossoms along the vine
    for x in range(6, s, 16):
        y = cy + math.sin(x / 6.0) * 12
        pet = 4
        d.ellipse([x - pet, y - pet, x + pet, y + pet], outline=SHADE, width=2)
        d.ellipse([x - 1, y - 1, x + 1, y + 1], fill=SHADE)
        # leaves
        d.line([(x - pet, y - pet), (x - pet - 5, y - pet - 5)], fill=SHADE, width=2)
        d.line([(x + pet, y - pet), (x + pet + 5, y - pet - 5)], fill=SHADE, width=2)
    save(img, "marble_floral")


if __name__ == "__main__":
    zeus_marble()
    meander()
    warrior()
    procession()
    chariot()
    acanthus()
    floral()
    print("All marble textures generated in", OUT)
