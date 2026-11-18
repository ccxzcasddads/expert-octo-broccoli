"""Иконки меню 16x16: эффекты, категории и кнопки.

Иконки эффектов собираются из спрайтов fx.py: герой эффекта, вспышка с эмблемой (криты),
стрела со следом (снаряды), ракета с искрами (фейерверки). Кнопки — бордовые плитки
с кремовой пиктограммой, как в остальных меню сервера.
"""
from __future__ import annotations

import colorsys
import math

from PIL import Image

import pixel
from fx import SPRITES
from pixel import RAMPS, rgba, sprite

ICONS = {}


def trim(image):
    """Обрезает прозрачные поля."""
    box = image.getbbox()
    return image.crop(box) if box else image


def place(base, name, x, y):
    """Кладёт спрайт (без полей) так, чтобы его левый верхний угол оказался в x, y."""
    image = trim(SPRITES[name]) if isinstance(name, str) else trim(name)
    base.alpha_composite(image, (x, y))
    return base


def centered(base, image, dx=0, dy=0):
    image = trim(image)
    x = (base.size[0] - image.size[0]) // 2 + dx
    y = (base.size[1] - image.size[1]) // 2 + dy
    base.alpha_composite(image, (x, y))
    return base


# ── Убийства и смерти: герои эффектов ────────────────────────────────────

KILL = {
    "lightning": "lightning", "explosion": "explosion", "blood": "blood", "inferno": "inferno",
    "soul_reaper": "scythe", "firework": "salute", "frost": "frost", "heartbreak": "heartbreak",
    "black_hole": "black_hole", "dna": "dna", "gold_rush": "gold_rush", "pentagram": "pentagram",
    "tornado": "tornado", "sakura": "sakura", "triumph": "trophy",
}
DEATH = {
    "ghost": "ghost", "smoke_bomb": "smoke_bomb", "blood_pool": "blood_pool", "soul_release": "soul",
    "grave": "grave", "ender": "portal", "self_destruct": "tnt", "farewell": "farewell", "wrath": "wrath",
    "ascension": "ascension", "splash": "splash", "sculk": "sculk", "bones": "bones", "confetti": "popper",
}
for effect, hero in KILL.items():
    ICONS[f"kill_{effect}"] = SPRITES[hero]
for effect, hero in DEATH.items():
    ICONS[f"death_{effect}"] = SPRITES[hero]


# ── Криты: вспышка удара и эмблема ───────────────────────────────────────

def rainbow_burst():
    """Вспышка, раскрашенная по кругу во все цвета."""
    base = pixel.burst(16, "white", spikes=8)
    outline = rgba(RAMPS["white"][0])
    result = base.copy()
    for y in range(16):
        for x in range(16):
            color = base.getpixel((x, y))
            if not color[3] or color == outline:
                continue
            hue = (math.atan2(y - 7.5, x - 7.5) / math.tau) % 1.0
            radius = math.hypot(x - 7.5, y - 7.5) / 7.5
            red, green, blue = colorsys.hsv_to_rgb(hue, 0.25 + 0.6 * min(1.0, radius * 1.4), 1.0)
            result.putpixel((x, y), (round(red * 255), round(green * 255), round(blue * 255), 255))
    return result


SPRITES["impact_rainbow"] = rainbow_burst()

CRIT = {
    "magic": ("impact_purple", "star_teal"), "flame": ("impact_red", "flame_orange"),
    "frost": ("impact_blue", "snow_ice"), "love": ("impact_pink", "heart_red"),
    "shock": ("impact_purple", "bolt_gold"), "soul": ("impact_blue", "wisp_teal"),
    "melody": ("impact_purple", "note2_pink"), "slime": ("impact_green", "drop_lime"),
    "blood": ("impact_ink", "drop_blood"), "stars": ("impact_blue", "star_gold"),
    "ink": ("impact_white", "drop_ink"), "rainbow": ("impact_rainbow", "spark_white"),
    "rage": ("impact_orange", "anger_red"), "sonic": ("impact_teal", "halo_white"),
}
for effect, (impact, emblem) in CRIT.items():
    ICONS[f"crit_{effect}"] = centered(SPRITES[impact].copy(), SPRITES[emblem])


# ── Мини-эмблемы для иконок снарядов и фейерверков ───────────────────────

MINI = {}


def mini(name, art, ramps):
    MINI[name] = sprite(art, ramps)


mini("flame", """
..3..
.343.
.3443
34543
34543
.333.
""", ("orange",))
mini("soul_flame", """
..3..
.343.
.3443
34543
34543
.333.
""", ("teal",))
mini("copper_flame", """
..3..
.343.
.3443
34543
34543
.333.
""", ("green",))
mini("heart", """
.4.3.
45333
43332
.332.
..2..
""", ("red",))
mini("note", """
..444
..4.4
..4..
444..
454..
.3...
""", ("pink",))
mini("snow", """
..4..
4.5.4
.555.
4.5.4
..4..
""", ("ice",))
mini("star", """
..4..
..5..
45554
.454.
.4.4.
""", ("gold",))
mini("drop", """
..4.
.45.
4543
4433
.33.
""", ("lime",))
mini("petal", """
.4.4.
45454
.454.
..3..
""", ("pink",))
mini("puff", """
.44..
45544
45543
.333.
""", ("purple",))
mini("rune", """
4.4.4
.444.
..4..
..4..
..4..
""", ("teal",))
mini("bolt", """
..44
.45.
4554
.54.
44..
""", ("gold",))
mini("gem", """
.444.
45443
.433.
..3..
""", ("green",))
mini("skull", """
.444.
45554
4o5o4
.454.
.4.4.
""", ("white",))
mini("orb", """
.33.
3443
3432
.22.
""", ("ink",))
for color in ("red", "gold", "green", "blue", "pink", "purple", "teal", "orange", "ice", "lime", "white"):
    mini(f"dot_{color}", """
44
43
""", (color,))
    mini(f"glint_{color}", """
.4.
454
.4.
""", (color,))


# ── Снаряды: стрела и её след ────────────────────────────────────────────

ARROW = """
.........444
..........54
.........s.4
........s...
.......s....
......s.....
.....s......
.d..s.......
.dds........
..sdd.......
...d........
"""
SHORT_ARROW = """
......444
.......54
......s.4
.....s...
....s....
.d.s.....
.dds.....
..sdd....
...d.....
"""


def arrow(feather, trail=()):
    """Стрела; trail — (мини-эмблема, x, y): тогда стрела короче и сдвинута в правый верхний угол."""
    base = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    if not trail:
        return centered(base, sprite(ARROW, ("white", feather, "brown")))
    base.alpha_composite(trim(sprite(SHORT_ARROW, ("white", feather, "brown"))), (5, 0))
    for name, x, y in trail:
        base.alpha_composite(trim(MINI[name]), (x, y))
    return base


PROJECTILE = {
    "flame": ("orange", (("flame", 0, 8), ("glint_gold", 8, 11))),
    "soul_flame": ("teal", (("soul_flame", 0, 8), ("glint_teal", 8, 11))),
    "copper_flame": ("green", (("copper_flame", 0, 8), ("glint_lime", 8, 11))),
    "love": ("pink", (("heart", 0, 9), ("glint_pink", 8, 11))),
    "melody": ("purple", (("note", 0, 8), ("glint_teal", 8, 11))),
    "rainbow": ("pink", (("dot_red", 0, 8), ("dot_gold", 2, 12), ("dot_green", 6, 11), ("dot_blue", 10, 12),
                         ("dot_purple", 12, 8))),
    "frost": ("ice", (("snow", 0, 9), ("glint_ice", 8, 11))),
    "stars": ("gold", (("star", 0, 9), ("glint_gold", 8, 11))),
    "slime": ("lime", (("drop", 0, 9), ("dot_lime", 8, 12))),
    "sakura": ("pink", (("petal", 0, 9), ("dot_pink", 8, 12))),
    "witch": ("purple", (("puff", 0, 10), ("glint_purple", 8, 10))),
    "runes": ("teal", (("rune", 0, 9), ("glint_teal", 8, 11))),
    "shock": ("gold", (("bolt", 0, 9), ("glint_white", 8, 11))),
    "emerald": ("green", (("gem", 0, 10), ("glint_lime", 8, 11))),
}
for effect, (feather, trail) in PROJECTILE.items():
    ICONS[f"projectile_{effect}"] = arrow(feather, trail)


# ── Фейерверки: ракета и искры ───────────────────────────────────────────

ROCKET = """
...4...
..454..
.45543.
.dddcb.
.45432.
.45432.
.dddcb.
.45432.
..s32..
..s....
.es.e..
..s....
"""


def rocket(body, sparks=()):
    """Ракета слева; sparks — (мини-эмблема, x, y) справа от неё."""
    base = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    art = trim(sprite(ROCKET, (body, "gold", "brown")))
    base.alpha_composite(art, (0 if sparks else 4, 2 if sparks else 1))
    for name, x, y in sparks:
        base.alpha_composite(trim(MINI[name]), (x, y))
    return base


FIREWORK = {
    "classic": ("red", (("star", 9, 0), ("glint_orange", 10, 8), ("dot_gold", 12, 12))),
    "flame": ("orange", (("flame", 9, 0), ("glint_gold", 10, 9))),
    "soul": ("teal", (("soul_flame", 9, 0), ("glint_teal", 10, 9))),
    "love": ("pink", (("heart", 9, 1), ("glint_pink", 10, 9))),
    "stars": ("blue", (("star", 9, 0), ("glint_gold", 10, 8), ("glint_white", 11, 12))),
    "rainbow": ("purple", (("dot_red", 9, 0), ("dot_gold", 12, 3), ("dot_green", 9, 6), ("dot_blue", 12, 9),
                           ("dot_pink", 9, 12))),
    "frost": ("ice", (("snow", 9, 0), ("glint_ice", 10, 9))),
    "sakura": ("pink", (("petal", 9, 1), ("dot_pink", 11, 9))),
    "melody": ("purple", (("note", 9, 0), ("glint_pink", 10, 10))),
    "emerald": ("green", (("gem", 9, 1), ("glint_lime", 10, 9))),
    "shock": ("blue", (("bolt", 9, 0), ("glint_white", 10, 9))),
    "void": ("purple", (("orb", 9, 1), ("glint_purple", 10, 9))),
    "confetti": ("gold", (("dot_red", 9, 0), ("dot_teal", 12, 4), ("dot_green", 9, 7), ("dot_pink", 12, 11))),
    "skull": ("white", (("skull", 9, 0), ("glint_white", 10, 9))),
}
for effect, (body, sparks) in FIREWORK.items():
    ICONS[f"firework_{effect}"] = rocket(body, sparks)


# ── Категории ────────────────────────────────────────────────────────────

ICONS["cat_sword"] = SPRITES["sword"]
ICONS["cat_pickaxe"] = SPRITES["pickaxe"]
ICONS["cat_totem"] = SPRITES["totem"]
ICONS["cat_hat"] = SPRITES["hat"]
ICONS["cat_kill"] = centered(Image.new("RGBA", (16, 16), (0, 0, 0, 0)), SPRITES["bones"])
ICONS["cat_crit"] = centered(pixel.burst(16, "gold", spikes=8), sprite("""
44
44
44
44
..
44
""", ("red",)))
ICONS["cat_projectile"] = arrow("red")
ICONS["cat_firework"] = rocket("red", (("star", 9, 0), ("glint_orange", 10, 8), ("dot_gold", 12, 12)))
ICONS["cat_death"] = SPRITES["ghost"]


# ── Кнопки: бордовая плитка и кремовая пиктограмма ───────────────────────

TILE = {
    "red": ("#ff707a", "#e23648", ("#fa5c68", "#d62438"), ("#e23648", "#be1a2e"), "#ba182c",
            ("#861226", "#5c0a1a"), "#34040e"),
    "green": ("#ff707a", "#e23648", ("#fa5c68", "#d62438"), ("#e23648", "#be1a2e"), "#ba182c",
              ("#3aac4a", "#1c682e"), "#0a3416"),
    "gray": ("#ff707a", "#e23648", ("#fa5c68", "#d62438"), ("#e23648", "#be1a2e"), "#ba182c",
             ("#6c6470", "#3c3642"), "#16101a"),
}
CREAM = "#fffcf0"


def blend(first, second, share):
    a, b = rgba(first), rgba(second)
    return tuple(round(a[i] + (b[i] - a[i]) * share) for i in range(3)) + (255,)


def tile(pictogram, field="red"):
    """Плитка 16x16 в стиле кнопок bordo; пиктограмма 12x12 из «#» отбрасывает тень вниз."""
    top, top_right, left, right, bottom, inner, shadow = TILE[field]
    image = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    black = rgba(pixel.BORDO_BLACK)
    for x in range(1, 15):
        image.putpixel((x, 0), black)
        image.putpixel((x, 15), black)
    for y in range(1, 15):
        image.putpixel((0, y), black)
        image.putpixel((15, y), black)
    image.putpixel((2, 15), rgba("#28060e"))
    image.putpixel((13, 15), rgba("#28060e"))
    for x in range(1, 14):
        image.putpixel((x, 1), rgba(top))
    image.putpixel((14, 1), rgba(top_right))
    for y in range(2, 14):
        share = (y - 2) / 11
        image.putpixel((1, y), blend(left[0], left[1], share))
        image.putpixel((14, y), blend(right[0], right[1], (y - 1) / 12))
        for x in range(2, 14):
            image.putpixel((x, y), blend(inner[0], inner[1], share))
    for x in range(1, 15):
        image.putpixel((x, 14), rgba(bottom))
    rows = [row.ljust(12, ".") for row in pictogram.strip("\n").split("\n")]
    rows = ([""] * ((12 - len(rows)) // 2) + rows)
    rows = [row.ljust(12, ".") for row in rows] + ["." * 12] * (12 - len(rows))
    cells = {(x, y) for y, row in enumerate(rows) for x, char in enumerate(row) if char == "#"}
    for x, y in cells:
        image.putpixel((2 + x, 2 + y), rgba(CREAM))
    for x, y in cells:
        if (x, y + 1) not in cells and y + 1 < 12:
            image.putpixel((2 + x, 3 + y), rgba(shadow))
    return image


NEXT = """
.....##.....
......##....
.......##...
.#########..
.#########..
.......##...
......##....
.....##.....
"""
ICONS["btn_next"] = tile(NEXT)
ICONS["btn_prev"] = tile("\n".join(row[::-1] for row in NEXT.strip("\n").split("\n")))
ICONS["btn_close"] = tile("""
..##....##..
..###..###..
...######...
....####....
....####....
...######...
..###..###..
..##....##..
""")
ICONS["btn_back"] = tile("""
....#.......
...##.......
..########..
...##....##.
....#....##.
.........##.
...#######..
...######...
""")
ICONS["btn_reset"] = tile("""
....####....
..########..
............
...######...
...#.##.#...
...#.##.#...
...#.##.#...
...######...
""")
ICONS["btn_unequip"] = tile("""
............
............
............
.##########.
.##########.
............
............
............
""", "gray")
ICONS["btn_done"] = tile("""
.........##.
........###.
.##....###..
.###..###...
..######....
...####.....
....##......
""", "green")
ICONS["invisible"] = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
