"""
Loyiha kartochkalari uchun shaffof fonli mockup (UIC uslubida: qurilma o'ng pastda, kartochkadan chiqib turadi).

    compose_cover(desktop="desktop.png", phone="store-1.png")        # monitor + telefon
    compose_cover(desktop="desktop.png", posters=["s1.png", "s2.png"]) # monitor + posterlar
    compose_cover(tablet="store-1.png", desktop=...)                   # monitor + planshet
"""
from __future__ import annotations

import io

from PIL import Image, ImageDraw, ImageFilter

W, H = 1600, 1200
BEZEL = (17, 17, 20, 255)
FRAME_EDGE = (58, 58, 64, 255)


def _rounded_mask(size: tuple[int, int], radius: int) -> Image.Image:
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius=radius, fill=255)
    return m


def _fit(img: Image.Image, size: tuple[int, int]) -> Image.Image:
    """Rasmni o'lchamga yuqoridan qirqib moslash (cover, anchor top)."""
    img = img.convert("RGB")
    tw, th = size
    scale = max(tw / img.width, th / img.height)
    nw, nh = int(img.width * scale + 0.5), int(img.height * scale + 0.5)
    img = img.resize((nw, nh), Image.LANCZOS)
    left = (nw - tw) // 2
    return img.crop((left, 0, left + tw, th))


def _shadow(canvas: Image.Image, box: tuple[int, int, int, int], radius: int, blur: int = 40, opacity: int = 110, offset=(0, 30)):
    sh = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    x0, y0, x1, y1 = box
    ImageDraw.Draw(sh).rounded_rectangle(
        (x0 + offset[0], y0 + offset[1], x1 + offset[0], y1 + offset[1]), radius=radius, fill=(0, 0, 0, opacity),
    )
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    canvas.alpha_composite(sh)


def _device(canvas: Image.Image, screen: Image.Image, box, radius: int, bezel: int, notch: bool = False):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    _shadow(canvas, box, radius)
    frame = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(frame)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=radius, fill=BEZEL, outline=FRAME_EDGE, width=3)
    sw, sh = w - bezel * 2, h - bezel * 2
    scr = _fit(screen, (sw, sh)).convert("RGBA")
    frame.paste(scr, (bezel, bezel), _rounded_mask((sw, sh), max(4, radius - bezel)))
    if notch:
        nw = int(w * 0.3)
        d.rounded_rectangle(((w - nw) // 2, bezel + 10, (w + nw) // 2, bezel + 10 + int(w * 0.075)), radius=40, fill=BEZEL)
    canvas.alpha_composite(frame, (x0, y0))


def _monitor(canvas: Image.Image, screen: Image.Image, x: int, y: int, width: int):
    h = int(width * 0.64)
    # oyoq
    d = ImageDraw.Draw(canvas)
    neck_w = int(width * 0.14)
    cx = x + width // 2
    d.polygon(
        [(cx - neck_w // 2, y + h - 10), (cx + neck_w // 2, y + h - 10), (cx + neck_w // 2 + 18, y + h + 120), (cx - neck_w // 2 - 18, y + h + 120)],
        fill=(205, 206, 212, 255),
    )
    d.rounded_rectangle((cx - int(width * 0.2), y + h + 112, cx + int(width * 0.2), y + h + 136), radius=12, fill=(225, 226, 231, 255))
    _device(canvas, screen, (x, y, x + width, y + h), radius=26, bezel=18)


def _phone(canvas: Image.Image, screen: Image.Image, x: int, y: int, width: int):
    h = int(width * 2.08)
    _device(canvas, screen, (x, y, x + width, y + h), radius=int(width * 0.16), bezel=int(width * 0.04), notch=True)


def _tablet(canvas: Image.Image, screen: Image.Image, x: int, y: int, width: int):
    ratio = screen.height / screen.width if screen.height > screen.width else 1.33
    h = int(width * ratio)
    _device(canvas, screen, (x, y, x + width, y + h), radius=44, bezel=22)


def _poster(canvas: Image.Image, img: Image.Image, x: int, y: int, width: int, angle: float = 0):
    img = img.convert("RGB")
    h = int(width * img.height / img.width)
    p = img.resize((width, h), Image.LANCZOS).convert("RGBA")
    p.putalpha(_rounded_mask((width, h), 34))
    pad = 80
    layer = Image.new("RGBA", (width + pad * 2, h + pad * 2), (0, 0, 0, 0))
    _shadow(layer, (pad, pad, pad + width, pad + h), 34, blur=30, opacity=120, offset=(0, 24))
    layer.alpha_composite(p, (pad, pad))
    if angle:
        layer = layer.rotate(angle, resample=Image.BICUBIC, expand=True)
    canvas.alpha_composite(layer, (x - pad, y - pad))


def compose_cover(
    desktop: str | None = None,
    phone: str | None = None,
    tablet: str | None = None,
    posters: list[str] | None = None,
) -> bytes:
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    open_ = lambda p: Image.open(p)  # noqa: E731

    if desktop:
        _monitor(canvas, open_(desktop), x=430 if (phone or tablet or posters) else 330, y=360, width=1240)
    if phone:
        _phone(canvas, open_(phone), x=250, y=470, width=330)
    if tablet:
        _tablet(canvas, open_(tablet), x=200, y=480, width=520)
    if posters:
        if desktop:
            _poster(canvas, open_(posters[0]), x=230, y=470, width=360, angle=4)
        else:
            xs = [420, 820, 1220]
            angles = [6, 0, -6]
            ys = [430, 360, 430]
            for i, p in enumerate(posters[:3]):
                _poster(canvas, open_(p), x=xs[i], y=ys[i], width=380, angle=angles[i])

    buf = io.BytesIO()
    canvas.save(buf, "WEBP", quality=86, method=6)
    return buf.getvalue()


def to_webp(path: str, max_w: int, max_h: int = 4000, quality: int = 82) -> bytes:
    img = Image.open(path)
    img = img.convert("RGBA") if img.mode in ("RGBA", "LA", "P") else img.convert("RGB")
    img.thumbnail((max_w, max_h), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, "WEBP", quality=quality, method=6)
    return buf.getvalue()
