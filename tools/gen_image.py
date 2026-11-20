#!/usr/bin/env python3
"""Draw the front page for Friday 20 November 2026 and save entry.png.

A newspaper front page: masthead, dateline, the Trump-Xi-Putin summit as
the lead story with the three flags, four grid stories, an ALSO TODAY
strip and a footer. Pillow drawing only: no network, no timestamps, no
randomness, so every run writes the same bytes.
"""

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
INK = (24, 24, 24)
PAPER = (247, 243, 234)
MUTED = (96, 91, 80)
RED = (178, 34, 34)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


F_TITLE = font("DejaVuSerif-Bold.ttf", 64)
F_DATE = font("DejaVuSans-Bold.ttf", 21)
F_HEAD = font("DejaVuSerif-Bold.ttf", 33)
F_KICK = font("DejaVuSans-Bold.ttf", 16)
F_GRID_HEAD = font("DejaVuSerif-Bold.ttf", 22)
F_BODY = font("DejaVuSerif.ttf", 19)
F_GRID_BODY = font("DejaVuSans.ttf", 16)
F_LABEL = font("DejaVuSans-Bold.ttf", 15)
F_STRIP = font("DejaVuSans.ttf", 16)
F_STRIP_LABEL = font("DejaVuSans-Bold.ttf", 16)
F_FOOT = font("DejaVuSans.ttf", 13)


def wrap(draw, text, fnt, width):
    """Greedy word wrap measured with the real font, so nothing overflows."""
    lines = []
    cur = ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill=INK, leading=None):
    """Draw wrapped lines top-left at (x, y); return the y below the last."""
    if leading is None:
        leading = int(fnt.size * 1.32)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def star(cx, cy, r_outer, r_inner):
    pts = []
    for i in range(10):
        r = r_outer if i % 2 == 0 else r_inner
        a = math.radians(-90 + i * 36)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def flag_us(d, x, y, w, h):
    stripe = h / 13
    for i in range(13):
        if i % 2 == 0:
            d.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe],
                        fill=(178, 34, 34))
    cw, ch = w * 0.40, stripe * 7
    d.rectangle([x, y, x + cw, y + ch], fill=(28, 48, 96))
    for r in range(5):
        for c in range(6):
            sx = x + 9 + c * (cw - 18) / 5
            sy = y + 8 + r * (ch - 14) / 4
            d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255))
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def flag_cn(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    d.polygon(star(x + w * 0.17, y + h * 0.30, h * 0.21, h * 0.085),
              fill=(255, 222, 0))
    for sx, sy in [(0.36, 0.14), (0.44, 0.27), (0.44, 0.43), (0.36, 0.53)]:
        d.polygon(star(x + w * sx, y + h * sy, h * 0.075, h * 0.03),
                  fill=(255, 222, 0))
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def flag_ru(d, x, y, w, h):
    for i, col in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        d.rectangle([x, y + i * h / 3, x + w, y + (i + 1) * h / 3], fill=col)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 36                      # side margin
    cw = W - 2 * mx              # content width

    # Masthead.
    title = "THE WORLD TODAY"
    d.text(((W - d.textlength(title, font=F_TITLE)) / 2, 26), title,
           font=F_TITLE, fill=INK)
    d.line([(mx, 112), (W - mx, 112)], fill=INK, width=3)
    d.line([(mx, 118), (W - mx, 118)], fill=INK, width=1)

    # Dateline.
    date = "FRIDAY, 20 NOVEMBER 2026  •  THE DAY'S WORLD NEWS IN ONE PAGE"
    d.text(((W - d.textlength(date, font=F_DATE)) / 2, 130), date,
           font=F_DATE, fill=MUTED)

    # Lead headline.
    lead_head = ("TRUMP, XI AND PUTIN HOLD FIRST-EVER "
                 "THREE-WAY SUMMIT")
    y = 168
    y = draw_lines(d, wrap(d, lead_head, F_HEAD, cw), mx, y, F_HEAD,
                   leading=42)

    # The three flags, labelled.
    fy = y + 12
    fw, fh = 288, 96
    gap = (cw - 3 * fw) / 2
    for i, (draw_flag, label) in enumerate([
            (flag_us, "UNITED STATES"),
            (flag_cn, "CHINA"),
            (flag_ru, "RUSSIA")]):
        fx = mx + i * (fw + gap)
        draw_flag(d, fx, fy, fw, fh)
        lw = d.textlength(label, font=F_LABEL)
        d.text((fx + (fw - lw) / 2, fy + fh + 8), label,
               font=F_LABEL, fill=INK)

    # Lead body.
    lead_body = (
        "SHENZHEN \u2014 The leaders of the United States, China and "
        "Russia met together for the first time on Thursday: 90 minutes "
        "behind closed doors at the Kylin Villa. Their joint \u201cpeace "
        "declaration\u201d reaffirmed that \u201ca nuclear war cannot be "
        "won and must never be fought\u201d and promised a dialogue on "
        "nuclear risks \u2014 but said nothing about Ukraine or Iran and "
        "set no arms-control deal. Trump called it \u201cbigger than "
        "Yalta\u201d.")
    y = draw_lines(d, wrap(d, lead_body, F_BODY, cw), mx, fy + fh + 34,
                   F_BODY, leading=26)

    # Layout guard: the lead must end before the grid divider at y=566.
    # Fail loudly instead of silently overlapping the grid.
    if y > 560:
        raise ValueError(f"lead overflows the lead area: ends at y={y}")

    # Divider above the grid.
    d.line([(mx, 566), (W - mx, 566)], fill=INK, width=2)

    stories = [
        ("WORLD COURT", "ICJ: Myanmar guilty of genocide",
         "The World Court ruled 9\u20136 that Myanmar committed genocide "
         "against the Rohingya \u2014 the first such finding against a "
         "state."),
        ("IRAN WAR", "Senate rejects curb on Iran war",
         "The US Senate voted 51\u201348 against a war-powers resolution "
         "as the war passed $48bn in cost; Houthis struck four Saudi "
         "targets and a tanker hit a mine near Hormuz."),
        ("UKRAINE", "Missiles strike Kyiv bridges",
         "Russia hit Kyiv with ballistic missiles as Britain pledged "
         "1,000+ drones in a \u00a3260m package; Europe expects to join "
         "new peace talks soon."),
        ("MARKETS", "Anthropic soars on Nasdaq debut",
         "The AI firm behind Claude became the first frontier AI company "
         "to go public, its shares jumping on their first day of trading "
         "as ANT."),
    ]
    col_w = (cw - 24) / 2
    row_y = [582, 730]
    for i, (kicker, head, body) in enumerate(stories):
        x = mx + (i % 2) * (col_w + 24)
        y = row_y[i // 2]
        d.text((x, y), kicker, font=F_KICK, fill=RED)
        y += 24
        y = draw_lines(d, wrap(d, head, F_GRID_HEAD, col_w), x, y,
                       F_GRID_HEAD, leading=27)
        draw_lines(d, wrap(d, body, F_GRID_BODY, col_w), x, y + 4,
                   F_GRID_BODY, leading=21)
    # Grid separators.
    d.line([(W / 2, 582), (W / 2, 866)], fill=MUTED, width=1)
    d.line([(mx, 720), (W - mx, 720)], fill=MUTED, width=1)

    # ALSO TODAY strip.
    d.line([(mx, 884), (W - mx, 884)], fill=INK, width=2)
    strip = ("Taiwan stocks plunge 2,200 points \u2022 COP31 drops fossil "
             "fuels from draft deal \u2022 Trump pardons baseball star "
             "Pete Rose \u2022 Cyclone Akvan hits Odisha \u2022 Harris "
             "meets Macron in Paris")
    label = "ALSO TODAY  "
    lw = d.textlength(label, font=F_STRIP_LABEL)
    d.text((mx, 900), label, font=F_STRIP_LABEL, fill=RED)
    draw_lines(d, wrap(d, strip, F_STRIP, cw - lw), mx + lw, 900,
               F_STRIP, leading=21)

    # Footer.
    d.line([(mx, 962), (W - mx, 962)], fill=INK, width=1)
    foot = "THE WORLD TODAY  \u2022  Friday 20 November 2026  \u2022  make.fun \u00b7 news-image-20261120"
    d.text(((W - d.textlength(foot, font=F_FOOT)) / 2, 972), foot,
           font=F_FOOT, fill=MUTED)

    out = Path(__file__).resolve().parent.parent / "entry.png"
    img.save(out, format="PNG")
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
