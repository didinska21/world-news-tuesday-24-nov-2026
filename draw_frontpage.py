#!/usr/bin/env python3
"""THE WORLD — Tuesday 24 November 2026. One day, one page.

Draws a 1024x1024 newspaper front page with PIL: a masthead, a UTC
timeline strip, six illustrated lead stories and 38 one-line briefs
covering 8 world regions. Every story happened, or was first
reported, on Tuesday 24 November 2026. Output: entry.png (JPEG).
"""

from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
MARGIN = 16
PAPER = (247, 242, 228)
CARD = (255, 254, 248)
INK = (26, 26, 30)
FAINT = (100, 95, 84)
ACCENT = (164, 32, 28)
CARD_EDGE = (198, 186, 158)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_BOLD = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_BOLD = "DejaVuSans-Bold.ttf"

# region code -> (full name, chip colour)
REGION_INFO = {
    "NA": ("NORTH AMERICA", (37, 99, 235)),
    "EU": ("EUROPE", (124, 58, 237)),
    "ME": ("MIDDLE EAST", (217, 119, 6)),
    "AF": ("AFRICA", (5, 150, 105)),
    "SA": ("SOUTH ASIA", (220, 38, 38)),
    "EA": ("EAST ASIA", (219, 39, 119)),
    "SEA": ("SOUTHEAST ASIA", (8, 145, 178)),
    "OC": ("OCEANIA", (101, 163, 13)),
}
REGION_ORDER = ["NA", "EU", "ME", "AF", "SA", "EA", "SEA", "OC"]

# The six lead stories: region, scene key, headline, summary.
LEAD_STORIES = [
    {
        "region": "EA", "scene": "markets",
        "head": "ASIA MARKETS ROCKET IN CHIP RALLY",
        "body": "Tokyo +4.5%, Seoul +7.5% and Taiwan +9.1% as Jensen "
                "Huang's return to Nvidia revives the AI trade.",
    },
    {
        "region": "SA", "scene": "quake",
        "head": "DAWN QUAKE SHAKES NEPAL",
        "body": "A magnitude 5.3 quake hits Koshi province; tremors "
                "are felt across India, Bhutan, Bangladesh and China.",
    },
    {
        "region": "EU", "scene": "strike",
        "head": "RUSSIAN STRIKE KILLS TWO IN ZAPORIZHZHIA",
        "body": "An overnight attack wounds 22 people, including two "
                "children, in the frontline Ukrainian city.",
    },
    {
        "region": "EA", "scene": "alert",
        "head": "SEOUL SOUNDS AIR ALERT OVER RUSSIAN JET",
        "body": "An evacuation warning sounds for Ulleung Island as a "
                "Russian aircraft enters Korean airspace.",
    },
    {
        "region": "SA", "scene": "flood",
        "head": "HIMALAYAN FLOOD LEAVES 100 MISSING",
        "body": "A wall of mud tears down an Indian mountain valley; "
                "at least four die as the army searches.",
    },
    {
        "region": "NA", "scene": "travel",
        "head": "AMERICA TAKES OFF FOR THANKSGIVING",
        "body": "The FAA braces for its busiest holiday in 16 years: "
                "81.5 million Americans on the move.",
    },
]

# The 38 briefs: (region code, one-line headline).
BRIEF_STORIES = [
    ("NA", "Mexico will prosecute cartel boss 'El Chapo Isidro' at home, defying a US extradition bid"),
    ("NA", "FAA lifts ground stop at Chicago O'Hare after an air-traffic staffing snarl"),
    ("NA", "US lawmakers close ranks against Nvidia chief's return, pressing tighter China chip curbs"),
    ("NA", "Comedian roasts Trump at Toronto's journalists' dinner"),
    ("EU", "Ukraine says Neptune missiles struck a Russian drone plant in Rostov-on-Don"),
    ("EU", "EU loans for Ukraine will cost 55 billion euros in interest alone, a Commission paper shows"),
    ("EU", "Norway's supreme court voids oil licences in a landmark climate ruling"),
    ("EU", "France confirms a deadly bird-flu outbreak at a poultry farm"),
    ("EU", "Georgia plans a full ban on surrogacy over trafficking concerns"),
    ("EU", "Moldova survey finds voters backing the road to Europe"),
    ("EU", "Inter fall in seven-goal San Siro thriller as Tresoldi hits a hat-trick"),
    ("ME", "Israel arrests 10 after days of violent settler attacks in the West Bank"),
    ("ME", "Saudi-led strike on Hodeidah telecom building kills 10, Houthi media say"),
    ("ME", "UAE president takes call from Syria's al-Sharaa on deeper cooperation"),
    ("ME", "Drone attack wounds four security men in Syria's Suwayda countryside"),
    ("ME", "Gulf bourses slip as Saudi-Houthi clashes rattle investors"),
    ("ME", "Erdogan plans a first visit to Libya in 15 years"),
    ("AF", "Nigeria: governor orders probe as eight-year-old dies in Abia school collapse"),
    ("AF", "At least 24 civilians killed in South Sudan's Warrap state"),
    ("AF", "Ethiopia's central bank holds a $140m foreign-exchange auction"),
    ("AF", "Museveni accepts an invitation to visit Somalia after talks with Mohamud"),
    ("AF", "Sahel states restart dialogue with the West Africa bloc"),
    ("AF", "Kenya secures 293,600 Saudi job openings for its workers"),
    ("SA", "Bangladesh begins vaccinating 50 million children against typhoid"),
    ("SA", "Former MP Prajwal Revanna is sentenced to life in prison for rape"),
    ("SA", "India holds third place in the Asia Power Index; Modi ranked second leader"),
    ("SA", "New Saryu-Kamala Express train links Ayodhya with Janakpur in Nepal"),
    ("EA", "SoftBank to invest $2bn in Intel"),
    ("EA", "Japan creates a new government body on foreign-resident concerns"),
    ("EA", "Japan's factory activity quickens as manufacturing PMI climbs to 53.7"),
    ("EA", "Seoul seeks priority Qatari LNG cargoes as Hormuz shipping normalises"),
    ("SEA", "Philippine Senate opens plenary debates on the 2027 national budget"),
    ("SEA", "S&P tips the Philippines to be SE Asia's slowest-growing economy in 2026"),
    ("SEA", "SE Asia's AI data-centre boom faces Nvidia supply curbs"),
    ("SEA", "Jollibee plans 30 UK restaurants in a franchise expansion"),
    ("OC", "Severe heatwave warning issued for Queensland's Cape York Peninsula"),
    ("OC", "Australia to treat AI as a first-order foreign-policy challenge"),
    ("OC", "Australia rotate squad for Rugby League World Cup final vs New Zealand"),
]

TIMELINE_TEXT = (
    "THE DAY AROUND THE WORLD (UTC) - 07:02 Kathmandu quake - "
    "07:52 Seoul air alert - Tokyo markets leap 4.5% - "
    "Zaporizhzhia struck overnight - US Thanksgiving rush peaks"
)

def load_font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


def wrap_words(draw, text, font, max_width):
    """Greedy word wrap against pixel width."""
    out = []
    for chunk in text.split("\n"):
        words = chunk.split()
        line = ""
        for word in words:
            trial = (line + " " + word).strip()
            if draw.textlength(trial, font=font) <= max_width:
                line = trial
            else:
                if line:
                    out.append(line)
                line = word
        if line:
            out.append(line)
    return out


def draw_paragraph(draw, x, y, text, font, max_width, fill=INK,
                   leading=1.22, center=False):
    for line in wrap_words(draw, text, font, max_width):
        if center:
            w = draw.textlength(line, font=font)
            draw.text((x + (max_width - w) / 2, y), line, font=font, fill=fill)
        else:
            draw.text((x, y), line, font=font, fill=fill)
        y += int(font.size * leading)
    return y


def paragraph_height(draw, text, font, max_width, leading=1.22):
    n = len(wrap_words(draw, text, font, max_width))
    return int(n * font.size * leading)


def region_chip(draw, x, y, code, font):
    _, colour = REGION_INFO[code]
    w = draw.textlength(code, font=font) + 12
    h = font.size + 6
    draw.rounded_rectangle([x, y, x + w, y + h], 3, fill=colour)
    draw.text((x + 6, y + 3), code, font=font, fill=(255, 255, 255))
    return w


# ---------------- lead scene illustrations ----------------
# Each scene paints inside the box (x0, y0, x1, y1).

def scene_markets(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(16, 24, 48))
    base = y1 - 14
    candles = [(0.06, 0.52, True), (0.20, 0.44, False), (0.34, 0.58, True),
               (0.48, 0.50, True), (0.62, 0.66, True), (0.76, 0.60, False),
               (0.88, 0.78, True)]
    cw = (x1 - x0) * 0.075
    for fx, top, up in candles:
        cx = x0 + (x1 - x0) * fx
        cy = y0 + (y1 - y0) * (1 - top)
        col = (34, 197, 94) if up else (239, 68, 68)
        draw.line([cx + cw / 2, cy - 9, cx + cw / 2, base], fill=col, width=2)
        draw.rectangle([cx, cy, cx + cw, base], fill=col)
    pts = [(x0 + (x1 - x0) * fx + cw / 2, y0 + (y1 - y0) * (1 - top) - 12)
           for fx, top, _ in candles]
    draw.line(pts, fill=(250, 204, 21), width=3)
    lx, ly = pts[-1]
    draw.polygon([(lx, ly), (lx - 13, ly + 2), (lx - 4, ly + 11)], fill=(250, 204, 21))


def scene_quake(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(253, 224, 171))
    draw.ellipse([x1 - 58, y0 + 8, x1 - 18, y0 + 48], fill=(245, 158, 11))
    horizon = y0 + (y1 - y0) * 0.58
    draw.polygon([(x0, horizon), (x0 + 70, y0 + 18), (x0 + 130, horizon)], fill=(120, 113, 108))
    draw.polygon([(x0 + 95, horizon), (x0 + 185, y0 + 8), (x0 + 265, horizon)], fill=(87, 83, 78))
    draw.rectangle([x0, horizon, x1, y1], fill=(168, 140, 96))
    crack = [(x0 + 30, horizon + 4), (x0 + 80, horizon + 18), (x0 + 70, horizon + 30),
              (x0 + 130, horizon + 40), (x0 + 190, horizon + 30), (x0 + 250, horizon + 44)]
    draw.line(crack, fill=(41, 37, 36), width=3)
    draw.line([(x0 + 80, horizon + 18), (x0 + 95, horizon + 34)], fill=(41, 37, 36), width=2)


def scene_strike(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(23, 27, 51))
    ground = y1 - 10
    for bx, bw, bh in [(0.03, 0.16, 0.52), (0.22, 0.13, 0.38), (0.62, 0.15, 0.46), (0.80, 0.17, 0.34)]:
        sx = x0 + (x1 - x0) * bx
        sw = (x1 - x0) * bw
        top = ground - (y1 - y0) * bh
        draw.rectangle([sx, top, sx + sw, ground], fill=(10, 12, 24))
        for wy in range(int(top) + 7, ground - 6, 13):
            draw.rectangle([sx + 5, wy, sx + 9, wy + 4], fill=(253, 224, 71))
    cx, cy = x0 + (x1 - x0) * 0.47, y0 + (y1 - y0) * 0.34
    star = []
    import math
    for i in range(16):
        r = 26 if i % 2 == 0 else 10
        a = math.pi * i / 8
        star.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(star, fill=(249, 115, 22))
    draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(254, 240, 138))
    for dx, dy, s in [(-38, -22, 15), (30, -28, 19), (2, -40, 13)]:
        draw.ellipse([cx + dx, cy + dy, cx + dx + s, cy + dy + s * 0.6], fill=(120, 124, 140))


def scene_alert(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(147, 197, 253))
    sea = y0 + (y1 - y0) * 0.68
    draw.rectangle([x0, sea, x1, y1], fill=(29, 78, 216))
    draw.polygon([(x0 + 30, sea), (x0 + 95, sea - 22), (x0 + 165, sea)], fill=(74, 124, 60))
    jx, jy = x0 + (x1 - x0) * 0.60, y0 + (y1 - y0) * 0.26
    draw.polygon([(jx, jy), (jx + 62, jy + 10), (jx + 20, jy + 16), (jx + 8, jy + 26),
                  (jx - 4, jy + 14), (jx - 16, jy + 16)], fill=(55, 65, 81))
    draw.polygon([(jx + 2, jy), (jx - 10, jy - 12), (jx + 12, jy - 2)], fill=(55, 65, 81))
    tx, ty = x1 - 52, y0 + 10
    draw.polygon([(tx + 17, ty), (tx, ty + 30), (tx + 34, ty + 30)], fill=(220, 38, 38))
    f = load_font(SANS_BOLD, 20)
    draw.text((tx + 13, ty + 9), "!", font=f, fill=(255, 255, 255))


def scene_flood(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(224, 242, 254))
    draw.polygon([(x0, y1), (x0, y0 + 16), (x0 + 105, y0 + 62), (x0 + 105, y1)], fill=(101, 128, 96))
    draw.polygon([(x1, y1), (x1, y0 + 10), (x0 + 205, y0 + 66), (x0 + 205, y1)], fill=(101, 128, 96))
    mud = [(x0 + 105, y0 + 60), (x0 + 150, y0 + 84), (x0 + 138, y0 + 108),
           (x0 + 175, y1), (x0 + 130, y1), (x0 + 128, y0 + 112), (x0 + 112, y0 + 88)]
    draw.polygon(mud, fill=(146, 96, 52))
    draw.line([(x0 + 122, y0 + 76), (x0 + 142, y0 + 118)], fill=(120, 76, 40), width=3)
    for hx, hy in [(x0 + 52, y1 - 40), (x0 + 238, y1 - 34)]:
        draw.rectangle([hx, hy, hx + 26, hy + 18], fill=(254, 243, 199))
        draw.polygon([(hx - 3, hy), (hx + 13, hy - 10), (hx + 29, hy)], fill=(146, 64, 14))


def scene_travel(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(186, 230, 253))
    draw.ellipse([x0 + 14, y0 + 8, x0 + 46, y0 + 40], fill=(250, 204, 21))
    for cx, cy, s in [(0.30, 0.20, 30), (0.78, 0.14, 24), (0.58, 0.34, 20)]:
        ex, ey = x0 + (x1 - x0) * cx, y0 + (y1 - y0) * cy
        draw.ellipse([ex, ey, ex + s, ey + s * 0.45], fill=(255, 255, 255))
        draw.ellipse([ex + s * 0.4, ey - 4, ex + s * 1.2, ey + s * 0.4], fill=(255, 255, 255))
    runway = y1 - 22
    draw.rectangle([x0, runway, x1, y1], fill=(75, 85, 99))
    for i in range(7):
        dx = x0 + 14 + i * 44
        draw.rectangle([dx, runway + 9, dx + 22, runway + 13], fill=(254, 240, 138))
    px, py = x0 + (x1 - x0) * 0.34, y0 + (y1 - y0) * 0.40
    draw.polygon([(px, py), (px + 96, py + 12), (px + 34, py + 20), (px + 16, py + 32),
                  (px - 2, py + 18), (px - 18, py + 20)], fill=(243, 244, 246), outline=(71, 85, 105))
    draw.polygon([(px + 6, py + 1), (px - 8, py - 14), (px + 20, py - 3)], fill=(220, 38, 38))
    for i in range(5):
        draw.rectangle([px + 26 + i * 13, py + 9, px + 33 + i * 13, py + 13], fill=(37, 99, 235))


SCENES = {
    "markets": scene_markets,
    "quake": scene_quake,
    "strike": scene_strike,
    "alert": scene_alert,
    "flood": scene_flood,
    "travel": scene_travel,
}

# ---------------- page composition ----------------

def build_fonts():
    return {
        "title": load_font(SERIF_BOLD, 52),
        "sub": load_font(SANS_BOLD, 14),
        "counts": load_font(SANS_BOLD, 15),
        "timeline": load_font(SANS_BOLD, 10),
        "lead_head": load_font(SANS_BOLD, 15),
        "lead_body": load_font(SANS, 11),
        "chip": load_font(SANS_BOLD, 10),
        "brief": load_font(SANS, 10),
        "brief_chip": load_font(SANS_BOLD, 9),
        "section": load_font(SERIF_BOLD, 17),
        "key": load_font(SANS_BOLD, 10),
        "footer": load_font(SANS, 10),
    }


def draw_masthead(draw, fonts):
    draw.rectangle([0, 0, PAGE, 5], fill=ACCENT)
    draw_paragraph(draw, 0, 12, "THE WORLD", fonts["title"], PAGE, center=True)
    draw.text((MARGIN, 76), "TUESDAY 24 NOVEMBER 2026", font=fonts["sub"], fill=INK)
    right = "ONE DAY - ONE PAGE"
    rw = draw.textlength(right, font=fonts["sub"])
    draw.text((PAGE - MARGIN - rw, 76), right, font=fonts["sub"], fill=INK)
    draw_paragraph(draw, 0, 98, "44 date-checked stories - 8 regions",
                   fonts["counts"], PAGE, fill=ACCENT, center=True)
    draw.line([MARGIN, 126, PAGE - MARGIN, 126], fill=INK, width=2)
    y = draw_paragraph(draw, MARGIN, 132, TIMELINE_TEXT, fonts["timeline"],
                       PAGE - 2 * MARGIN, fill=ACCENT, center=True)
    draw.line([MARGIN, y + 2, PAGE - MARGIN, y + 2], fill=INK, width=1)
    return y + 8


def draw_lead_panel(draw, x, y, w, h, story, fonts):
    draw.rectangle([x, y, x + w, y + h], fill=CARD, outline=CARD_EDGE, width=1)
    scene_box = (x + 6, y + 6, x + w - 6, y + 90)
    SCENES[story["scene"]](draw, scene_box)
    cy = y + 98
    cw = region_chip(draw, x + 8, cy, story["region"], fonts["chip"])
    name = REGION_INFO[story["region"]][0]
    draw.text((x + 14 + cw, cy + 2), name, font=fonts["chip"], fill=FAINT)
    hy = draw_paragraph(draw, x + 8, cy + 24, story["head"], fonts["lead_head"],
                        w - 16, leading=1.15)
    draw_paragraph(draw, x + 8, hy + 2, story["body"], fonts["lead_body"],
                   w - 16, fill=(52, 50, 46), leading=1.2)


def draw_briefs(draw, top, bottom, fonts):
    draw.text((MARGIN, top), "MORE OF THE DAY", font=fonts["section"], fill=INK)
    tag = "38 BRIEFS"
    tw = draw.textlength(tag, font=fonts["section"])
    draw.text((PAGE - MARGIN - tw, top), tag, font=fonts["section"], fill=ACCENT)
    draw.line([MARGIN, top + 26, PAGE - MARGIN, top + 26], fill=INK, width=2)
    col_w = (PAGE - 2 * MARGIN - 20) // 3
    col_x = [MARGIN + i * (col_w + 10) for i in range(3)]
    text_w = col_w - 40
    # Balance the three columns by measured height (order preserved),
    # so no column can run into the region key or the footer.
    heights = [paragraph_height(draw, hl, fonts["brief"], text_w, leading=1.15) + 3
               for _, hl in BRIEF_STORIES]
    target = sum(heights) / 3
    col = 0
    y = top + 36
    used = 0
    for (code, headline), h in zip(BRIEF_STORIES, heights):
        if col < 2 and used > 0 and used + h > target:
            col += 1
            y = top + 36
            used = 0
        x = col_x[col]
        region_chip(draw, x, y + 1, code, fonts["brief_chip"])
        draw_paragraph(draw, x + 40, y, headline, fonts["brief"], text_w, leading=1.15)
        y += h
        used += h
    return y


def draw_region_key(draw, y, fonts):
    counts = {code: 0 for code in REGION_ORDER}
    for story in LEAD_STORIES:
        counts[story["region"]] += 1
    for code, _ in BRIEF_STORIES:
        counts[code] += 1
    x = MARGIN
    draw.text((x, y + 2), "KEY", font=fonts["key"], fill=FAINT)
    x += 34
    for code in REGION_ORDER:
        cw = region_chip(draw, x, y, code, fonts["key"])
        label = str(counts[code])
        draw.text((x + cw + 3, y + 2), label, font=fonts["key"], fill=INK)
        x += cw + 3 + draw.textlength(label, font=fonts["key"]) + 13


def main():
    import os
    img = Image.new("RGB", (PAGE, PAGE), PAPER)
    draw = ImageDraw.Draw(img)
    fonts = build_fonts()

    y = draw_masthead(draw, fonts)

    # lead grid: 3 columns x 2 rows
    panel_w = (PAGE - 2 * MARGIN - 20) // 3
    panel_h = 198
    for i, story in enumerate(LEAD_STORIES):
        px = MARGIN + (i % 3) * (panel_w + 10)
        py = y + (i // 3) * (panel_h + 10)
        draw_lead_panel(draw, px, py, panel_w, panel_h, story, fonts)
    briefs_top = y + 2 * panel_h + 18

    draw_briefs(draw, briefs_top, 958, fonts)
    draw_region_key(draw, 966, fonts)
    draw_paragraph(
        draw, MARGIN, 992,
        "Every story on this page happened or was first reported on "
        "Tuesday 24 November 2026 (UTC). Pictures are drawn illustrations.",
        fonts["footer"], PAGE - 2 * MARGIN, fill=FAINT, center=True)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, format="JPEG", quality=88)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()


