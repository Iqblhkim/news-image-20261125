#!/usr/bin/env python3
"""news-image-20261125: newspaper front page, Wed 25 Nov 2026.
Pure Python 3.13 stdlib only. Hand-written PNG encoder + 5x7 pixel font.
Reads MAKEFUN_OUTPUT_DIR, writes entry.png (1024x1024). Deterministic.
"""
import os
import struct
import zlib

W, H = 1024, 1024
PAPER = (251, 248, 239)
INK = (16, 16, 16)
RED = (176, 32, 26)
NAVY = (16, 32, 64)
BLUE = (28, 68, 116)
TEAL = (12, 94, 88)
GOLD = (178, 128, 24)
GREEN = (46, 110, 58)
GREY = (98, 96, 90)
SKY = (214, 230, 240)
TAN = (222, 205, 165)
GRID = (180, 200, 215)
WHITE = (255, 255, 255)
NIGHT = (18, 28, 58)
GOLDL = (240, 200, 80)

# ---------------- 5x7 pixel font ----------------
# Each glyph: 7 rows of 5 chars, '#' = ink.
def _g(rows):
    return tuple(rows)

FONT = {
 'A': _g(["01110","10001","10001","11111","10001","10001","10001"]),
 'B': _g(["11110","10001","10001","11110","10001","10001","11110"]),
 'C': _g(["01110","10001","10000","10000","10000","10001","01110"]),
 'D': _g(["11110","10001","10001","10001","10001","10001","11110"]),
 'E': _g(["11111","10000","10000","11110","10000","10000","11111"]),
 'F': _g(["11111","10000","10000","11110","10000","10000","10000"]),
 'G': _g(["01110","10001","10000","10111","10001","10001","01111"]),
 'H': _g(["10001","10001","10001","11111","10001","10001","10001"]),
 'I': _g(["01110","00100","00100","00100","00100","00100","01110"]),
 'J': _g(["00111","00010","00010","00010","00010","10010","01100"]),
 'K': _g(["10001","10010","10100","11000","10100","10010","10001"]),
 'L': _g(["10000","10000","10000","10000","10000","10000","11111"]),
 'M': _g(["10001","11011","10101","10101","10001","10001","10001"]),
 'N': _g(["10001","11001","10101","10011","10001","10001","10001"]),
 'O': _g(["01110","10001","10001","10001","10001","10001","01110"]),
 'P': _g(["11110","10001","10001","11110","10000","10000","10000"]),
 'Q': _g(["01110","10001","10001","10001","10101","10010","01101"]),
 'R': _g(["11110","10001","10001","11110","10100","10010","10001"]),
 'S': _g(["01111","10000","10000","01110","00001","00001","11110"]),
 'T': _g(["11111","00100","00100","00100","00100","00100","00100"]),
 'U': _g(["10001","10001","10001","10001","10001","10001","01110"]),
 'V': _g(["10001","10001","10001","10001","10001","01010","00100"]),
 'W': _g(["10001","10001","10001","10101","10101","11011","10001"]),
 'X': _g(["10001","10001","01010","00100","01010","10001","10001"]),
 'Y': _g(["10001","10001","01010","00100","00100","00100","00100"]),
 'Z': _g(["11111","00001","00010","00100","01000","10000","11111"]),
 '0': _g(["01110","10001","10011","10101","11001","10001","01110"]),
 '1': _g(["00100","01100","00100","00100","00100","00100","01110"]),
 '2': _g(["01110","10001","00001","00110","01000","10000","11111"]),
 '3': _g(["11110","00001","00001","01110","00001","00001","11110"]),
 '4': _g(["00010","00110","01010","10010","11111","00010","00010"]),
 '5': _g(["11111","10000","11110","00001","00001","10001","01110"]),
 '6': _g(["01110","10000","10000","11110","10001","10001","01110"]),
 '7': _g(["11111","00001","00010","00100","01000","01000","01000"]),
 '8': _g(["01110","10001","10001","01110","10001","10001","01110"]),
 '9': _g(["01110","10001","10001","01111","00001","00001","01110"]),
 ' ': _g(["00000","00000","00000","00000","00000","00000","00000"]),
 '.': _g(["00000","00000","00000","00000","00000","00000","01100"]),
 ',': _g(["00000","00000","00000","00000","00100","00100","01000"]),
 ':': _g(["00000","00100","00000","00000","00000","00100","00000"]),
 ';': _g(["00000","00100","00000","00000","00100","00100","01000"]),
 '-': _g(["00000","00000","00000","01110","00000","00000","00000"]),
 "'": _g(["00100","00100","00000","00000","00000","00000","00000"]),
 '(': _g(["00010","00100","01000","01000","01000","00100","00010"]),
 ')': _g(["01000","00100","00010","00010","00010","00100","01000"]),
 '%': _g(["11001","11010","00010","00100","01000","01011","10011"]),
 '$': _g(["00100","01111","10100","01110","00101","11110","00100"]),
 '/': _g(["00001","00010","00010","00100","01000","01000","10000"]),
 '&': _g(["01100","10010","10100","01000","10101","10010","01101"]),
 '!': _g(["00100","00100","00100","00100","00100","00000","00100"]),
 '?': _g(["01110","10001","00001","00110","00100","00000","00100"]),
 '+': _g(["00000","00100","00100","11111","00100","00100","00000"]),
 '=': _g(["00000","00000","11111","00000","11111","00000","00000"]),
 '"': _g(["01010","01010","00000","00000","00000","00000","00000"]),
 '\u00b7': _g(["00000","00000","00000","01100","00000","00000","00000"]),
 '\u2014': _g(["00000","00000","00000","11111","00000","00000","00000"]),
 '\u2019': _g(["00100","00100","00000","00000","00000","00000","00000"]),
}
# Map lowercase / curly forms to the same glyphs (rendered as capitals).
for _c in "abcdefghijklmnopqrstuvwxyz":
    FONT[_c] = FONT[_c.upper()]

# ---------------- canvas ----------------
class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bg * (w * h))

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(c)

    def rect(self, x, y, w, h, c):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            for xx in range(x0, x1):
                i = base + (xx - x0) * 3
                self.px[i:i + 3] = bytes(c)

    def hline(self, x, y, w, c, th=1):
        self.rect(x, y, w, th, c)

    def vline(self, x, y, h, c, th=1):
        self.rect(x, y, th, h, c)

    def line(self, x0, y0, x1, y1, c, th=1):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            self.rect(x0, y0, th, th, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy; x0 += sx
            if e2 < dx:
                err += dx; y0 += sy

    def circle(self, cx, cy, r, c):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                    self.set(xx, yy, c)

    def ring(self, cx, cy, r, c, th=2):
        # outline-only circle (for broadcast waves): no filled disc
        for yy in range(cy - r - 1, cy + r + 2):
            for xx in range(cx - r - 1, cx + r + 2):
                d = ((xx - cx) ** 2 + (yy - cy) ** 2) ** 0.5
                if abs(d - r) <= th / 2:
                    self.set(xx, yy, c)

    def poly(self, pts, c):
        # scanline fill
        ys = [p[1] for p in pts]
        for y in range(min(ys), max(ys) + 1):
            xs = []
            n = len(pts)
            for i in range(n):
                x0, y0 = pts[i]; x1, y1 = pts[(i + 1) % n]
                if (y0 <= y < y1) or (y1 <= y < y0):
                    xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
            xs.sort()
            for k in range(0, len(xs) - 1, 2):
                self.rect(int(xs[k]), y, max(1, int(xs[k + 1]) - int(xs[k])), 1, c)

    def text(self, s, x, y, c, scale=1, bold=False, adv=None):
        """Draw text; returns width. adv = advance per char (default 6*scale)."""
        a = adv if adv is not None else 6 * scale
        cx = x
        for ch in s:
            g = FONT.get(ch, FONT[' '])
            for r in range(7):
                row = g[r]
                for col in range(5):
                    if row[col] == '1':
                        self.rect(cx + col * scale, y + r * scale, scale, scale, c)
                        if bold:
                            self.rect(cx + col * scale + 1, y + r * scale, scale, scale, c)
            cx += a
        return cx - x

    def text_w(self, s, scale=1, adv=None):
        a = adv if adv is not None else 6 * scale
        return len(s) * a - (a - 5 * scale)

    def wrap(self, s, max_w, scale=1, adv=None):
        a = adv if adv is not None else 6 * scale
        cw = max_w // a
        lines, cur = [], ""
        for word in s.split(" "):
            trial = (cur + " " + word).strip()
            if len(trial) <= cw or not cur:
                cur = trial
            else:
                lines.append(cur); cur = word
        if cur:
            lines.append(cur)
        return lines

    def para(self, s, x, y, max_w, c, scale=1, lh=None, bold=False, adv=None):
        lh = lh if lh is not None else 7 * scale + 2
        lines = self.wrap(s, max_w, scale, adv)
        for i, ln in enumerate(lines):
            self.text(ln, x, y + i * lh, c, scale, bold=bold, adv=adv)
        return y + len(lines) * lh

    def centred(self, s, cx, y, c, scale=1, bold=False):
        w = self.text_w(s, scale)
        self.text(s, cx - w // 2, y, c, scale, bold=bold)
        return w


def png_bytes(cv):
    raw = bytearray()
    for y in range(cv.h):
        raw.append(0)
        raw.extend(cv.px[y * cv.w * 3:(y + 1) * cv.w * 3])
    def chunk(t, data):
        c = struct.pack(">I", len(data)) + t + data
        return c + struct.pack(">I", zlib.crc32(t + data) & 0xffffffff)
    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + chunk(b"IEND", b""))

# ---------------- data (from spec, verbatim) ----------------
NUMBERS = [
    ("$237.5bn", "Venezuela's total public debt, reported today"),
    ("700,000", "Russian troops killed in the war, analysis finds"),
    ("74,746", "Gaza death toll, health officials say"),
    ("266m", "people face acute food insecurity, WFP says"),
    ("48", "Patriot interceptors awaiting US sign-off"),
    ("11", "wounded in Houthi strike on Riyadh tower"),
]
REGIONS = [("EUROPE 8", BLUE), ("MIDDLE EAST 5", RED), ("AMERICAS 12", TEAL),
           ("ASIA-PACIFIC 9", GOLD), ("AFRICA 1", GREEN), ("WORLD 1", GREY)]
LEADS = [
    ("1 \u00b7 KYIV REGION, UKRAINE \u2014 WAR",
     "Russian drones hit Kyiv again; two killed in Odesa",
     "Debris sets a 16-storey Kyiv block ablaze, injuring two; in Odesa "
     "a strike kills two and injures three, a child among them."),
    ("2 \u00b7 WASHINGTON \u2014 UKRAINE",
     "Zelenskyy: US 'aligning with Russia' as Patriots stall",
     "Kyiv says 48 Patriot interceptors await US sign-off; Zelenskyy "
     "warns the delays help Moscow force surrender of the Donbas."),
    ("3 \u00b7 RIYADH \u2014 YEMEN",
     "Houthis hit Riyadh's tallest tower; 11 wounded",
     "A drone strike wounds 11 at the capital's tallest tower as Houthi "
     "forces push to within 60 km of Aden."),
]
TILES = [
    ("4 \u00b7 NEW DELHI \u2014 POLITICS", "BJP, Akali Dal reunite for Punjab 2027",
     "Six years after splitting over farm laws, the allies will contest all 117 seats together."),
    ("5 \u00b7 BENGHAZI, LIBYA \u2014 FALLOUT", "Russia cries 'terrorism' after ship strikes",
     "Moscow warns of severe consequences after Ukraine's drone hits in the Baltic and off Libya."),
    ("6 \u00b7 WASHINGTON \u2014 HONOUR", "Trump gives Giuliani Medal of Freedom",
     "The president awards the highest civilian honour to the former New York mayor."),
    ("7 \u00b7 NEW YORK \u2014 COURTS", "Huawei guilty of stealing trade secrets",
     "A US jury convicts Huawei of trade-secret theft but acquits it of racketeering."),
    ("8 \u00b7 WASHINGTON \u2014 CYBER", "CIA, spy chief's office hit by breach",
     "A breach touches unclassified material at the CIA and the director of national intelligence."),
    ("9 \u00b7 GULF OF HORMUZ \u2014 SEA", "Iran says tankers hit by mines",
     "The Revolutionary Guard navy claims three oil tankers were hit by naval mines in the strait."),
    ("10 \u00b7 BRUSSELS \u2014 SANCTIONS", "EU announces new Russia sanctions",
     "Brussels unveils further restrictive measures as the war grinds on and Kyiv seeks more aid."),
    ("11 \u00b7 NEW YORK \u2014 MARKETS", "Nvidia slides 7% as AI rally cools",
     "The Nasdaq falls 2.3% a day after its best rally since April; chip stocks lead the pullback."),
    ("12 \u00b7 MUMBAI \u2014 MARKETS", "Markets shut for Guru Nanak Jayanti",
     "Bourses closed on Tuesday; trading resumes today with Gift Nifty pointing to a gap-up open."),
    ("13 \u00b7 LONDON \u2014 CRICKET", "England level T20 series in Australia",
     "England chase 185 to beat Australia by eight wickets in the second T20 international."),
    ("14 \u00b7 TEHRAN \u2014 ENERGY", "Iran braces for winter gas shortages",
     "War damage to gas plants deepens the energy crisis as Tehran rations electricity."),
    ("15 \u00b7 KABUL \u2014 MEDIA", "Radio returns for Afghan girls",
     "RFE/RL resumes shortwave broadcasts with lessons for girls barred from school by the Taliban."),
]
ALSO = [
    (16, "STOCKHOLM", "Parliament to vote on Kristersson as PM"),
    (17, "PARIS", "Sarkozy corruption case sent to trial"),
    (18, "CHICAGO", "Radar outage delays O'Hare flights"),
    (19, "FORT HOOD", "Shooter Hasan seeks stay of execution"),
    (20, "JERUSALEM", "US envoy unsure Israel aid ends this year"),
    (21, "CHENNAI", "Karthigai Deepam lit despite court order"),
    (22, "NEW DELHI", "Ban calls over Netflix Pakistan series"),
    (23, "NEW DELHI", "Opposition seeks winter session date"),
    (24, "MUMBAI", "Tata Sons eyes Shapoorji liquidity plan"),
    (25, "KOCHI", "Kerala seeks pure petrol for E20 tests"),
    (26, "GAZA", "Oxfam: pollution risks cover 99% of Gaza"),
    (27, "BERLIN", "Most Germans back halting arms to Kyiv"),
    (28, "WARSAW", "NATO to send early-warning jets to Poland"),
    (29, "MANCHESTER", "United fume over Yoro red card"),
    (30, "AUSTIN", "Dell lifts forecasts on AI server boom"),
    (31, "WASHINGTON", "Bill seeks to track Russian hybrid attacks"),
    (32, "CARACAS", "Venezuela reports $237.5bn public debt"),
    (33, "NEW DELHI", "India women face China in hockey"),
    (34, "ROME", "WFP: 266m face acute food insecurity"),
    (35, "WASHINGTON", "Trump tariff decision expected today"),
    (36, "WASHINGTON", "Trump spares turkeys Freedom, Feathers"),
]
PINS = [(30, 50, 1), (-77, 39, 2), (47, 25, 3), (77, 29, 4), (20, 32, 5),
        (56, 26, 9), (73, 19, 12), (0, 51, 13), (51, 36, 14), (69, 34, 15),
        (18, 59, 16), (-88, 42, 18), (80, 13, 21), (13, 52, 27),
        (-67, 10, 32), (12, 42, 34)]

# ---------------- scenes ----------------
def scene_lead(cv, idx, x, y, w, h):
    if idx == 0:  # Kyiv night skyline, searchlight, moon
        cv.rect(x, y, w, h, NIGHT)
        cv.circle(x + w - 40, y + 22, 13, (240, 236, 200))
        cv.circle(x + w - 44, y + 18, 11, (250, 248, 220))
        for i in range(40):
            sx = x + (i * 37) % w; sy = y + (i * 53) % 40
            cv.rect(sx, sy, 2, 2, WHITE)
        cv.poly([(x + 60, y + h), (x + 150, y + 8), (x + 175, y + 8), (x + 210, y + h)], (90, 100, 140))
        base = y + h
        heights = [62, 80, 55, 88, 70, 95, 60, 78]
        bw = w // 8
        for i, bh in enumerate(heights):
            bx = x + i * bw
            cv.rect(bx + 2, base - bh, bw - 4, bh, (8, 12, 28))
            for wy in range(base - bh + 8, base - 6, 14):
                for wx in range(bx + 6, bx + bw - 6, 10):
                    if (wx + wy) % 3 == 0:
                        cv.rect(wx, wy, 3, 4, GOLDL)
        cv.rect(x + 30, base - 100, 26, 12, (200, 60, 30))  # fire glow block
        cv.rect(x + 34, base - 96, 18, 6, (255, 170, 40))
        cv.line(x + 43, base - 100, x + 43, base - 118, (255, 120, 40), 2)
    elif idx == 1:  # Patriot launchers, night sky
        cv.rect(x, y, w, h, (14, 22, 48))
        for i in range(30):
            cv.rect(x + (i * 41) % w, y + (i * 29) % 34, 2, 2, WHITE)
        cv.circle(x + 34, y + 20, 10, (240, 236, 200))
        gy = y + h - 18
        cv.rect(x, y + h - 18, w, 18, (30, 38, 30))
        for k, lx in enumerate((x + 30, x + 130, x + 225)):
            cv.rect(lx, gy - 12, 46, 12, (50, 58, 52))
            cv.circle(lx + 10, gy, 6, INK); cv.circle(lx + 36, gy, 6, INK)
            ang = -28 - k * 6
            import math
            ex = lx + 23 + int(52 * math.cos(math.radians(ang)))
            ey = gy - 12 + int(52 * math.sin(math.radians(ang)))
            cv.line(lx + 23, gy - 12, ex, ey, (120, 130, 125), 5)
            cv.line(lx + 23, gy - 12, ex, ey, (200, 205, 200), 2)
    else:  # Riyadh tower, pale sky, drone
        cv.rect(x, y, w, h, (232, 222, 198))
        cv.circle(x + w - 45, y + 24, 14, (250, 220, 120))
        cv.rect(x + 110, y + 8, 74, h - 8, (70, 90, 120))
        cv.rect(x + 118, y + 16, 58, 6, (180, 200, 220))
        for wy in range(y + 30, y + h - 10, 14):
            cv.rect(x + 118, wy, 58, 5, (180, 200, 220))
        cv.poly([(x + 128, y + 8), (x + 147, y - 6), (x + 166, y + 8)], (50, 65, 90))
        cv.rect(x + 20, y + h - 34, 60, 34, (120, 110, 95))
        cv.rect(x + 220, y + h - 26, 56, 26, (120, 110, 95))
        # small drone
        dx, dy = x + 235, y + 30
        cv.rect(dx, dy, 16, 5, INK)
        cv.rect(dx - 6, dy - 2, 8, 2, INK); cv.rect(dx + 14, dy - 2, 8, 2, INK)
        cv.line(dx + 4, dy + 6, dx + 4, dy + 16, RED, 2)

def scene_tile(cv, n, x, y, w, h):
    bg = [(235, 228, 205), (220, 232, 238), (238, 226, 210), (228, 232, 220),
          (222, 226, 236), (236, 228, 222), (226, 236, 228), (232, 228, 214),
          (220, 230, 226), (238, 232, 220), (228, 226, 232), (224, 234, 230)]
    cv.rect(x, y, w, h, bg[(n - 4) % len(bg)])
    cx, cy = x + w // 2, y + h // 2
    if n == 4:  # ballot box
        cv.rect(cx - 45, cy - 6, 90, 34, (90, 60, 40))
        cv.poly([(cx - 50, cy - 6), (cx - 40, cy - 22), (cx + 40, cy - 22), (cx + 50, cy - 6)], (120, 80, 50))
        cv.rect(cx - 8, cy - 32, 16, 12, WHITE)
        cv.rect(cx - 20, cy + 8, 40, 10, WHITE)
    elif n == 5:  # warship at night
        cv.rect(x, y, w, h, NIGHT)
        cv.rect(x, y + h - 22, w, 22, (20, 60, 90))
        cv.poly([(cx - 70, cy + 12), (cx - 55, cy - 8), (cx + 55, cy - 8), (cx + 75, cy + 12)], (90, 100, 110))
        cv.rect(cx - 18, cy - 24, 36, 16, (110, 120, 130))
        cv.line(cx, cy - 24, cx, cy - 36, (150, 160, 170), 2)
        cv.circle(cx + 52, cy - 20, 3, RED)
    elif n == 6:  # medal
        cv.poly([(cx - 22, y + 6), (cx - 8, y + 6), (cx, cy - 2), (cx + 8, y + 6), (cx + 22, y + 6), (cx + 12, cy - 2)], (176, 32, 26))
        cv.rect(cx - 14, cy - 4, 28, 6, (176, 32, 26))
        cv.circle(cx, cy + 12, 16, GOLDL)
        cv.circle(cx, cy + 12, 11, (200, 160, 40))
        cv.text("1", cx - 3, cy + 4, (120, 90, 10), 1)
    elif n == 7:  # gavel
        cv.rect(cx - 45, cy - 14, 55, 12, (110, 75, 40))
        cv.rect(cx - 50, cy - 18, 10, 20, (80, 55, 30))
        cv.rect(cx + 12, cy - 18, 10, 20, (80, 55, 30))
        cv.line(cx + 5, cy - 2, cx + 38, cy + 22, (90, 60, 30), 4)
        cv.rect(cx + 22, cy + 18, 44, 6, (140, 100, 55))
    elif n == 8:  # server room
        cv.rect(x, y, w, h, (16, 20, 34))
        for i in range(4):
            bx = x + 18 + i * 52
            cv.rect(bx, y + 8, 40, h - 16, (30, 44, 66))
            for r in range(3):
                cv.rect(bx + 6, y + 14 + r * 14, 18, 4, (80, 200, 120) if r != 1 else RED)
                cv.circle(bx + 32, y + 16 + r * 14, 2, GOLDL)
        cv.line(x + 20, y + 12, x + w - 20, y + h - 12, (90, 160, 220), 1)
    elif n == 9:  # sea, ships, mines
        cv.rect(x, y, w, h - 18, (200, 225, 235))
        cv.rect(x, y + h - 18, w, 18, (30, 90, 130))
        for sx in (cx - 70, cx + 10):
            cv.rect(sx, cy - 6, 52, 10, (60, 70, 80))
            cv.rect(sx + 12, cy - 20, 26, 14, (90, 100, 110))
        for mx in (cx - 20, cx + 62):
            cv.circle(mx, cy + 8, 6, INK)
            for dx, dy in ((-8, 0), (8, 0), (0, -8), (0, 8)):
                cv.line(mx, cy + 8, mx + dx, cy + 8 + dy, INK, 1)
    elif n == 10:  # EU flags / stars
        cv.rect(x, y, w, h, BLUE)
        for i in range(3):
            bx = x + 22 + i * 72
            cv.rect(bx, y + 10, 56, h - 20, (28, 68, 116))
            cv.rect(bx, y + 10, 56, h - 20, (20, 50, 95))
            for k in range(8):
                import math
                a = k * 3.14159 / 4
                cv.circle(int(bx + 28 + 12 * math.cos(a)), int(y + h // 2 + 12 * math.sin(a)), 2, GOLDL)
    elif n == 11:  # falling chart
        cv.rect(x, y, w, h, WHITE)
        pts = [(x + 16, y + 14), (x + 60, y + 12), (x + 100, y + 26), (x + 150, y + 22), (x + 200, y + 44)]
        for a, b in zip(pts, pts[1:]):
            cv.line(a[0], a[1], b[0], b[1], RED, 3)
        cv.line(x + 12, y + h - 12, x + w - 12, y + h - 12, INK, 1)
        cv.line(x + 12, y + 8, x + 12, y + h - 12, INK, 1)
    elif n == 12:  # temple / market
        cv.rect(cx - 55, cy + 2, 110, h // 2 - 4, (190, 140, 70))
        cv.poly([(cx - 62, cy + 2), (cx, cy - 26), (cx + 62, cy + 2)], (150, 90, 40))
        cv.rect(cx - 8, cy + 12, 16, h // 2 - 14, (90, 50, 20))
        cv.circle(cx, cy - 30, 4, GOLDL)
        for i in range(3):
            cv.rect(x + 14 + i * 70, y + h - 14, 44, 8, (120, 80, 40))
    elif n == 13:  # cricket bat and ball
        cv.line(cx - 30, cy - 24, cx + 30, cy + 20, (170, 130, 70), 8)
        cv.rect(cx + 28, cy + 14, 10, 16, (120, 85, 40))
        cv.circle(cx - 62, cy - 18, 9, RED)
        cv.rect(x, y + h - 10, w, 10, (90, 140, 70))
        cv.rect(x + 30, y + h - 16, 60, 6, (220, 210, 180))
    elif n == 14:  # gas plant
        cv.rect(cx - 70, cy - 6, 46, h // 2, (100, 105, 115))
        cv.rect(cx - 16, cy - 18, 34, h // 2 + 12, (130, 135, 145))
        cv.rect(cx + 26, cy + 2, 50, h // 2 - 8, (90, 95, 105))
        cv.line(cx - 70, cy - 6, cx - 78, cy - 28, (70, 75, 85), 3)
        cv.line(cx + 20, cy - 18, cx + 12, cy - 28, (70, 75, 85), 3)
        cv.circle(cx + 60, cy - 20, 5, GOLDL)
    else:  # 15 radio tower
        cv.poly([(cx - 22, y + h - 6), (cx - 4, y + 8), (cx + 4, y + 8), (cx + 22, y + h - 6)], (60, 70, 80))
        cv.line(cx, y + 8, cx, y - 2, RED, 2)
        cv.circle(cx, y + 6, 3, RED)
        for r in (10, 17, 24):
            cv.ring(cx, y + 10, r, RED, th=2)

# ---------------- map ----------------
LAND = [
    [(-168, 66), (-140, 70), (-120, 71), (-100, 68), (-85, 66), (-80, 62), (-75, 58), (-65, 60), (-60, 55), (-65, 50), (-70, 44), (-75, 38), (-80, 32), (-81, 26), (-90, 21), (-95, 17), (-87, 13), (-83, 9), (-79, 9), (-85, 14), (-92, 15), (-97, 16), (-105, 20), (-110, 24), (-115, 30), (-125, 40), (-125, 49), (-135, 58), (-155, 58), (-165, 60)],
    [(-80, 10), (-70, 12), (-62, 9), (-52, 5), (-44, -3), (-35, -8), (-40, -15), (-48, -25), (-55, -32), (-65, -40), (-70, -30), (-73, -20), (-78, -10), (-81, -3), (-80, 5)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (4, 53), (8, 57), (12, 55), (18, 56), (21, 59), (25, 60), (30, 62), (28, 65), (32, 70), (40, 68), (44, 64), (40, 58), (32, 52), (28, 46), (23, 40), (19, 42), (14, 45), (8, 44), (3, 42), (-2, 37)],
    [(-17, 15), (-16, 25), (-10, 31), (-5, 35), (5, 37), (11, 34), (20, 32), (30, 31), (33, 27), (38, 20), (43, 12), (51, 11), (48, 2), (42, -5), (40, -15), (36, -22), (32, -29), (26, -34), (19, -35), (16, -28), (13, -18), (12, -8), (9, 0), (9, 4), (0, 5), (-8, 5), (-13, 8), (-17, 12)],
    [(38, 70), (55, 69), (70, 72), (85, 74), (100, 76), (115, 73), (130, 71), (145, 72), (160, 70), (170, 66), (162, 60), (155, 55), (142, 50), (135, 43), (128, 38), (122, 32), (115, 25), (108, 20), (105, 10), (100, 8), (95, 15), (90, 22), (85, 20), (80, 15), (77, 8), (73, 20), (66, 25), (60, 25), (55, 27), (50, 29), (48, 30), (44, 36), (40, 42), (36, 44), (32, 50), (30, 55), (32, 62), (38, 66)],
    [(113, -22), (122, -14), (132, -12), (142, -11), (148, -20), (153, -27), (150, -37), (142, -39), (135, -35), (128, -32), (120, -34), (114, -30), (113, -25)],
]

def draw_map(cv, x, y, w, h):
    cv.rect(x, y, w, h, SKY)
    def px(lon, lat):
        return (x + int((lon + 180) / 360 * w), y + int((90 - lat) / 180 * h))
    for lon in range(-180, 181, 30):
        gx, _ = px(lon, 0)
        cv.vline(gx, y, h, GRID, 1)
    for lat in range(-60, 91, 30):
        _, gy = px(0, lat)
        cv.hline(x, gy, w, GRID, 1)
    for poly_ll in LAND:
        cv.poly([px(lon, lat) for lon, lat in poly_ll], TAN)
    cv.rect(x, y, w, 1, INK); cv.rect(x, y + h - 1, w, 1, INK)
    cv.rect(x, y, 1, h, INK); cv.rect(x + w - 1, y, 1, h, INK)
    for lon, lat, num in PINS:
        px_, py_ = px(lon, lat)
        cv.circle(px_, py_, 8, RED)
        s = str(num)
        cv.text(s, px_ - (3 if len(s) == 1 else 6), py_ - 3, WHITE, 1, bold=True)

# ---------------- build ----------------
def build():
    cv = Canvas(W, H, PAPER)
    M = 28
    CW = W - 2 * M
    y = 0
    # 1 top strip
    cv.rect(0, 0, W, 24, NAVY)
    cv.centred("THE WORLD IN ONE DAY \u00b7 36 STORIES \u00b7 6 REGIONS \u00b7 EVERY ONE DATED WEDNESDAY 25 NOVEMBER 2026",
               W // 2, 8, WHITE, 1, bold=True)
    y = 28
    # 2 masthead
    cv.centred("WEDNESDAY 25 NOVEMBER 2026", W // 2, y + 2, INK, 5, bold=True)
    cv.hline(M, y + 40, CW, INK, 2)
    y = 72
    # 3 subhead
    cv.centred("KYIV HIT AGAIN AS ODESA BURIES ITS DEAD \u00b7 ZELENSKYY SAYS US IS ALIGNING WITH RUSSIA \u00b7 HOUTHIS STRIKE RIYADH TOWER",
               W // 2, y, RED, 1, bold=True)
    y = 86
    # 4 numbers
    colw = CW // 6
    for i, (num, cap) in enumerate(NUMBERS):
        cx0 = M + i * colw
        cv.centred(num, cx0 + colw // 2, y, RED, 3, bold=True)
        cv.para(cap, cx0 + 6, y + 24, colw - 12, INK, 1, lh=9)
        if i:
            cv.vline(cx0, y, 50, (200, 195, 180), 1)
    cv.hline(M, y + 54, CW, INK, 1)
    y = 144
    # 5 region bar
    seg = CW // 6
    for i, (label, col) in enumerate(REGIONS):
        cv.rect(M + i * seg, y, seg - 2, 22, col)
        cv.centred(label, M + i * seg + (seg - 2) // 2, y + 7, WHITE, 1, bold=True)
    y = 170
    # 6 leads
    lw = (CW - 16) // 3
    for i, (kick, head, body) in enumerate(LEADS):
        x0 = M + i * (lw + 8)
        scene_lead(cv, i, x0, y, lw, 86)
        yy = y + 90
        cv.text(kick, x0, yy, RED, 1, bold=True); yy += 11
        yy = cv.para(head, x0, yy, lw, INK, 2, lh=15, bold=True)
        cv.para(body, x0, yy + 2, lw, INK, 1, lh=8)
        if i:
            cv.vline(x0 - 4, y, 168, (200, 195, 180), 1)
    y = 342
    # 7 tiles, 3 rows x 4
    tw = (CW - 24) // 4
    for row in range(3):
        for col in range(4):
            idx = row * 4 + col
            kick, head, body = TILES[idx]
            x0 = M + col * (tw + 8)
            y0 = y + row * 104
            scene_tile(cv, idx + 4, x0, y0, tw, 44)
            yy = y0 + 48
            cv.text(kick, x0, yy, RED, 1, bold=True); yy += 10
            yy = cv.para(head, x0, yy, tw, INK, 1, lh=9, bold=True)
            cv.para(body, x0, yy + 1, tw, INK, 1, lh=9)
    y = 658
    # 8 map
    cv.text("WHERE IT HAPPENED", M, y, INK, 1, bold=True)
    cv.text("PINS = STORY NUMBERS", M + 190, y, RED, 1, bold=True)
    cv.hline(M, y + 10, CW, INK, 1)
    draw_map(cv, M, y + 14, CW, 180)
    y = 858
    # 9 ALSO
    cv.text("ALSO ON WEDNESDAY 25 NOVEMBER \u2014 21 MORE STORIES", M, y, RED, 1, bold=True)
    cv.hline(M, y + 10, CW, RED, 1)
    aw = CW // 3
    for i, (num, city, head) in enumerate(ALSO):
        col, r = divmod(i, 7)
        x0 = M + col * aw
        yy = y + 14 + r * 10
        cv.text("%d %s \u2014 %s" % (num, city, head), x0, yy, INK, 1, adv=5)
    y = 950
    # 10 DATE CHECK
    cv.rect(M, y, CW, 50, PAPER)
    for xx in range(M, M + CW):
        cv.set(xx, y, RED); cv.set(xx, y + 49, RED)
    for yy2 in range(y, y + 50):
        cv.set(M, yy2, RED); cv.set(M + CW - 1, yy2, RED)
    cv.text("DATE CHECK", M + 8, y + 5, RED, 1, bold=True)
    cv.para("Left out because they happened on earlier days: COP31 collapse "
            "(Sun 22 Nov) \u00b7 Merkury sunk (Sun 22 Nov) \u00b7 Serang fire breaks out "
            "(Sat 21 Nov) \u00b7 Nvidia's 31.5% surge (Mon 23 Nov) \u00b7 Sensex -1,484 "
            "(Mon 23 Nov) \u00b7 Nepal Rs 15,000cr package (Sun 22 Nov) \u00b7 GTA 6 "
            "launch (Thu 19 Nov) \u00b7 Trump-Xi-Putin summit (Thu 19 Nov)",
            M + 8, y + 16, CW - 16, INK, 1, lh=9)
    y = 1006
    # 11 footer
    cv.centred("Sources: Reuters \u00b7 AP \u00b7 AFP \u00b7 BBC \u00b7 The Guardian \u00b7 CNN \u00b7 WSJ \u00b7 "
              "Le Monde \u2014 wires read to press time 04:00 WIB, Wed 25 Nov 2026 \u00b7 Scenes are drawn illustrations",
              W // 2, y, INK, 1)
    return cv

def main():
    out = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out, exist_ok=True)
    cv = build()
    with open(os.path.join(out, "entry.png"), "wb") as f:
        f.write(png_bytes(cv))

if __name__ == "__main__":
    main()
