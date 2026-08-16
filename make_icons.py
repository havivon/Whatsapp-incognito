#!/usr/bin/env python3
"""
יצירת אייקוני ה-PWA: ריבוע מעוגל כהה עם בועת צ'אט ירוקה.
הרנדור נעשה בפי 2 מהגודל הסופי ואז מוקטן ב-LANCZOS לקצוות חלקים.

    pip install Pillow && python3 make_icons.py
"""

from PIL import Image, ImageChops, ImageDraw, ImageFilter

BG = (11, 15, 20, 255)        # #0b0f14
GREEN = (37, 211, 102, 255)   # #25D366
DOT = (11, 15, 20, 255)

SS = 2  # supersampling


def rounded_square(size, radius_ratio=0.22):
    """רקע כהה עם פינות מעוגלות."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, size - 1, size - 1],
                        radius=int(size * radius_ratio), fill=BG)
    return img


def green_glow(size):
    """זוהר ירוק עדין בפינה העליונה."""
    glow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(glow)
    r = size * 0.55
    cx, cy = size * 0.74, size * 0.14
    steps = 26
    for i in range(steps, 0, -1):
        rr = r * i / steps
        a = int(30 * (1 - i / steps) ** 1.6)
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
                  fill=(37, 211, 102, a))
    return glow.filter(ImageFilter.GaussianBlur(size * 0.06))


def chat_bubble(size, box):
    """
    בועת צ'אט ירוקה עם זנב משמאל-למטה ושלוש נקודות כהות.
    box = (x0, y0, x1, y1) — התיבה שבתוכה מציירים.
    """
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    x0, y0, x1, y1 = box
    w = x1 - x0
    h = y1 - y0

    body_h = h * 0.80
    by1 = y0 + body_h
    radius = body_h * 0.30

    d.rounded_rectangle([x0, y0, x1, by1], radius=radius, fill=GREEN)

    # זנב משמאל-למטה
    tail_x = x0 + w * 0.20
    d.polygon([
        (tail_x, by1 - radius * 0.35),
        (tail_x + w * 0.20, by1 - radius * 0.10),
        (x0 + w * 0.035, y1),
    ], fill=GREEN)

    # שלוש נקודות
    cy = y0 + body_h * 0.50
    dot_r = w * 0.072
    for k in (-1, 0, 1):
        cx = x0 + w * 0.5 + k * w * 0.235
        d.ellipse([cx - dot_r, cy - dot_r, cx + dot_r, cy + dot_r], fill=DOT)

    return layer


def build(size, inset=0.72, radius_ratio=0.22):
    """בונה אייקון מלא. inset = כמה מהמסגרת תופס הציור."""
    s = size * SS
    img = rounded_square(s, radius_ratio)

    # הזוהר נחתך לפי צורת הרקע כדי שלא יבלוט מחוץ לפינות המעוגלות
    glow = green_glow(s)
    glow.putalpha(ImageChops.multiply(glow.getchannel("A"), img.getchannel("A")))
    img = Image.alpha_composite(img, glow)

    bw = s * inset
    bh = bw * 0.92
    x0 = (s - bw) / 2
    y0 = (s - bh) / 2 + s * 0.015
    img = Image.alpha_composite(img, chat_bubble(s, (x0, y0, x0 + bw, y0 + bh)))

    return img.resize((size, size), Image.LANCZOS)


def main():
    build(192).save("icon-192.png")
    build(512).save("icon-512.png")
    build(180).save("apple-touch-icon.png")
    # maskable: הציור בתוך 56% מהמסגרת, רקע מלא בלי פינות מעוגלות
    build(512, inset=0.56, radius_ratio=0.0).save("icon-maskable-512.png")
    print("נוצרו: icon-192.png, icon-512.png, icon-maskable-512.png, apple-touch-icon.png")


if __name__ == "__main__":
    main()
