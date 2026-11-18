"""Спрайты эффектов: частицы и «герои», которые видны в мире и служат иконками в меню.

Каждая запись — имя и картинка 16x16. Рисунки описаны текстовыми сетками, см. pixel.py.
Частицы перекрашиваются в разные палитры: spark_gold, spark_teal и т. д.
"""
from __future__ import annotations

from pixel import sprite

SPRITES = {}


def add(name, art, ramps=("red",), **options):
    SPRITES[name] = sprite(art, ramps, **options)


def family(name, art, variants, **options):
    """Одна форма в нескольких палитрах: name_<палитра>."""
    for variant in variants:
        add(f"{name}_{variant}", art, (variant,), **options)


WARM = ("gold", "orange", "red")
COOL = ("teal", "blue", "ice", "purple")
ALL = ("gold", "orange", "red", "pink", "purple", "blue", "teal", "ice", "green", "lime", "white")

# ── Частицы ──────────────────────────────────────────────────────────────

family("spark", """
...3...
...4...
..454..
3455543
..454..
...4...
...3...
""", ALL)

family("glint", """
..4..
..5..
45554
..5..
..4..
""", ALL)

family("star", """
.....4.....
....454....
....454....
4444555444.
.4555555443
..45555433.
..45554433.
.445434433.
.444...333.
.33.....33.
""", ("gold", "white", "teal", "pink", "purple"))

family("orb", """
..3444..
.345554.
34555443
34554443
34444433
33444332
.333332.
..2222..
""", ALL + ("ink", "blood"))

family("dot", """
.44.
4554
4443
.33.
""", ALL + ("ink", "blood", "brown", "gray"))

family("shard", """
..5..
.454.
.4543
45433
45433
45432
.4332
.432.
..3..
""", ("ice", "teal", "purple", "green", "red", "gold", "white"))

family("drop", """
..4..
..4..
.454.
.4543
45443
44433
.333.
""", ("blood", "red", "blue", "ice", "lime", "green", "ink", "purple", "teal"))

family("flame", """
...3....
..33....
..343...
.3443.3.
.34443..
3445433.
3455443.
3455543.
.34543..
..333...
""", ("orange", "teal", "green", "purple", "blood", "pink", "ice"))

family("puff", """
...444.....
..45554.44.
.4555554554
45555555554
45555555543
.4555555433
..444.4433.
""", ("white", "gray", "ink", "purple", "teal", "pink", "orange"))

family("heart", """
.44...33.
4554.3333
454333333
433333332
.3333332.
..33322..
...322...
....2....
""", ("red", "pink", "purple", "white", "gold"))

family("note", """
...4444
...4334
...4...
...4...
...4...
.444...
4554...
4443...
.33....
""", ("pink", "teal", "gold", "purple", "lime", "blue", "red"))

family("note2", """
..4444444
..4333334
..4.....4
..4.....4
..4.....4
.44....44
454...454
443...443
.3.....3.
""", ("pink", "teal", "gold", "purple", "lime", "blue", "red"))

family("bolt", """
....44
...454
..454.
.4544.
455554
.4454.
.454..
454...
44....
""", ("gold", "teal", "purple", "white", "blue"))

family("petal", """
.44.44.
4554554
4555543
.45543.
.44433.
..433..
...3...
""", ("pink", "white", "red", "purple"))

family("leaf", """
....444
..44543
.455433
.45443.
45443..
4433...
33.....
""", ("green", "lime", "orange", "gold"))

add("feather", """
......44.
.....4554
....45543
...45543.
..45543..
.45543...
.4543....
.443.....
43.......
2........
""", ("white",))

family("rune_a", """
4..4...
4.44...
444....
44..4..
4..44..
4.44...
444....
44.....
4......
""", ("teal", "purple", "gold", "red"))

family("rune_b", """
4..4..4
4..4..4
44.4.44
.44444.
..444..
...4...
...4...
...4...
...4...
""", ("teal", "purple", "gold", "red"))

family("rune_c", """
...4...
..444..
.44.44.
44...44
.44.44.
..444..
.44.44.
44...44
4.....4
""", ("teal", "purple", "gold", "red"))

family("gem", """
..44444..
.4555544.
455444433
454444333
444433332
.4433332.
..43322..
...322...
....2....
""", ("green", "red", "blue", "purple", "teal", "pink"))

add("coin", """
..33333..
.3555443.
355444432
354434432
354434332
354434332
344433332
.3333322.
..22222..
""", ("gold",))

family("skull", """
..4444444..
.455555554.
45555555544
45oo555oo44
45oo555oo43
45555o55543
.455555543.
..45o5o53..
..4444433..
""", ("white", "blood", "teal", "purple", "gold"))

add("bone", """
.4.4......
4544......
.4554.....
4.4554....
...4554...
....4554.4
.....4554.
......4454
......4.4.
""", ("white",))

family("confetti", """
.44.
4554
.33.
""", ("red", "gold", "green", "blue", "pink", "purple", "teal"))

family("strip", """
.4...
454..
.454.
..453
...3.
""", ("red", "gold", "green", "blue", "pink", "purple", "teal"))

family("snow", """
....4....
.4..5..4.
..4.5.4..
...555...
455555554
...555...
..4.5.4..
.4..5..4.
....4....
""", ("ice", "white"))

family("wisp", """
...4....
..45....
..454...
.4554...
.45554..
4555554.
45o55o54
45555554
45555543
.455543.
..4433..
""", ("teal", "white", "purple", "green", "blood"))

family("anger", """
...44...44...
...44...44...
...44...44...
44444...44444
44444...44444
.............
.............
.............
44444...44444
44444...44444
...44...44...
...44...44...
...44...44...
""", ("red", "blood"))

family("splat", """
...33.....3.
.3.343..3...
..3344333...
.33455443.3.
3345555443..
.3455555433.
..345554433.
.3344554433.
.3.3344333.3
....3333....
..3..33..3..
""", ("lime", "ink", "blood", "blue", "purple", "pink"))

# ── Герои: крупные спрайты эффектов, они же иконки в меню ────────────────

add("lightning", """
......5544..
.....5544...
....5544....
...55544....
..55555444..
.....5544...
....5544....
....544.....
...544......
...54.......
..54........
..4.........
""", ("gold",))

add("blood", """
.....4.....
.....4.....
....454....
....4543...
...45543...
...455433..
..4555433..
..4554333..
..4554332..
..3443332..
...33322...
....222....
""", ("blood",))

add("inferno", """
.....3.....
....33.....
....333....
...3343..3.
...3443.33.
..334443332
.3344443432
.3345544432
33455554432
33455555432
33455555432
.334555432.
..3344432..
...33322...
""", ("orange",))

add("scythe", """
......4444....
....44555544..
...4554433454c
..454......ccb
..44......cbc.
.43......cbc..
.3......cbc...
.......cbc.t..
......cbc.ttt.
.....cbc..tut.
....cbc...ttt.
...cbc.....s..
..cbc.........
..bc..........
""", ("white", "brown", "teal"))

add("frost", """
.......5......
......454.....
......4543....
.....45433....
..5..45433..5.
.454o45433o454
.453o45433o453
.453o45433o453
.453o45432o453
.433o44332o433
.333o33322o332
..2..22222..2.
""", ("ice",))

add("heartbreak", """
.4444...3333.
455554o333333
45544o3333333
454443o333332
4444433o33332
.44443o33332.
..444o33332..
...443o3332..
....43o332...
.....3o2.....
......o......
""", ("red",))

add("dna", """
.44....aa.
.454..aba.
..4544ba..
...45ba...
...ab54...
..aba454..
.aba..454.
.ab3553 44.
.aba..454.
..aba454..
...ab54...
...45ba...
..4544ba..
.454..aba.
""".replace("3553 44", "355344"), ("purple", "pink"))

add("gold_rush", """
....444444....
...45555543...
...44444433...
...33333322...
.44444..44444.
4555543o555543
4444433o444433
3333332o333332
""", ("gold",))

add("tornado", """
3445555554433.
.34455554433..
.2333444332...
..345555443...
...3455443....
...2334432....
....345543....
.....34543....
.....23332....
......3443....
.......343....
.......232....
........33....
........3.....
""", ("white",))

add("sakura", """
.....444.....
....45554....
....45554....
.444.454.444.
4555443445554
45554dcd45554
.4443cdc3444.
...443c344...
..4554.4554..
.45554.45554.
.45543.34554.
..443...344..
""", ("pink", "gold"))

add("trophy", """
...44444444...
44445555443333
4..45555443..3
4..45555443..3
44.45555443.33
.444555544333.
....455443....
.....4543.....
......43......
......43......
.....4543.....
....455433....
...45554433...
...33333322...
""", ("gold",))

add("ghost", """
...44444...
..4555554..
.455555554.
.45o555o54.
.45o555o543
45555555543
4555ooo5543
45555o55543
45555555543
45555555433
45545554433
44.444.433.
4...4...3..
""", ("white",))

add("smoke_bomb", """
........e.
.......ede
......b.e.
.....b....
..2222....
.233332...
23443322..
23433222..
23332221..
22222211..
.222211...
..1111....
""", ("ink", "gold"))

add("blood_pool", """
...4444444...
..455555554..
.45555555544.
.45oo555oo44.
.45oo555oo43.
.45555o55543.
..455555543..
...45o5o53...
...4444433...
.23333333332.
2333343333332
.22333333322.
""", ("blood",))

add("soul", """
....44.....
...4554....
...45554...
..455554...
.45555554..
.455555554.
455o555o554
455o555o554
45555555544
4555oo55543
.455555543.
..4555443..
...44433...
""", ("teal",))

add("grave", """
...44444....
..4555554...
.455555543..
.4555o5543..
.455ooo543..
.4555o5543..
.4555o5543..
.455555543..
.455555433..
.444444333..
cdcccdccdccc
bcbbcbbcbbcb
""", ("gray", "green"))

add("tnt", """
......b.e..
.....b.ede.
....b...e..
34444444443
34555555433
WWWWWWWWWWW
KKKWKWKWKKK
WKWWKKKWWKW
WKWWKWKWWKW
WWWWWWWWWWW
33333333332
33333333322
22222222221
""", ("red", "gold"))

add("wrath", """
....34443....
..344555443..
.345555555433
3455555555443
3445555544433
.33444443333.
.....dee.....
....dee......
...deeed.....
.....ded.....
....ded......
....dd.......
...d.........
""", ("gray", "gold"))

add("ascension", """
....cddddc....
...cd....dc...
....cddddc....
..............
.44........44.
4554..dd..4554
45554deed45554
45555deed55554
.4555.dd.5554.
.45454..45454.
..4.4....4.4..
""", ("white", "gold"))

add("splash", """
......4......
.4...454...4.
.....454.....
.4...454...4.
.44..454..44.
.454.454.454.
.45444544454.
.45555555554.
..455555554..
3333444443333
.33333333333.
""", ("blue",))

add("sculk", """
......2......
..2..222..2..
...2233322...
..223444322..
..23o444o32..
.223o444o322.
2234444444322
.2234ooo4322.
..234454432..
..223333322..
...2222222...
..2..222..2..
......2......
""", ("teal",))

add("bones", """
..4444444..
.455555554.
45555555544
45oo555oo44
45oo555oo43
45555o55543
.455555543.
..45o5o53..
..4444433..
44.......44
.444...444.
...44444...
.444...444.
44.......44
""", ("white",))

add("popper", """
...........aa.
.....qq.......
..........d...
..aa..........
.......q....a.
....44........
...4554..dd...
...45c54......
..455cc54.....
..45cc5543....
..4c55433.....
.455433.......
.4433.........
.33...........
""", ("gold", "red", "teal"))

# ── Иконки категорий ─────────────────────────────────────────────────────

add("sword", """
...........444
..........4554
.........45543
........45543.
.......45543..
..d...45543...
..dd.45543....
...dd5543.....
....ddc3......
...sdddc......
..sr..cdd.....
.sr.....c.....
dr............
dd............
""", ("teal", "gold", "brown"))

add("pickaxe", """
.....444444...
...4455555544.
...44...sr454.
.......sr.4554
......sr...454
.....sr....454
....sr.....454
...sr......44.
..sr.......44.
.sr...........
sr............
r.............
""", ("gold", "gold", "brown"))

add("totem", """
..44444..
.4555554.
.4c545c4.
.4555554.
..45o54..
444555444
455555554
4.45554.4
..45554..
..45554..
..45554..
..44.44..
""", ("gold", "green"))

add("hat", """
......44.....
.....4554....
.....45543...
....455443...
....45e443...
...45eee433..
...455e4433..
..455544433..
..cddccccbb..
3444444444332
.33333333322.
""", ("purple", "gold"))

add("rocket", """
....4....
...454...
..45543..
.4555433.
.dddcccb.
.4554332.
.4554332.
.dddcccb.
.4554332.
..33322..
....s...e
..e.s..d.
....s.e..
...es....
""", ("red", "gold", "brown"))

add("arrow", """
.....4555
......455
.....s.45
....s...4
.d.s.....
.dds.....
..sdd....
...d.....
""", ("white", "red", "brown"))

# ── Фигуры по формулам: вспышки, кольца, круги, воронки ──────────────────

import math  # noqa: E402

from PIL import Image  # noqa: E402

import pixel  # noqa: E402
from pixel import RAMPS, rgba  # noqa: E402


def put(name, image):
    SPRITES[name] = image


def explosion(size, grow=1.0, smoke=0.0):
    """Взрыв: красные языки, оранжевая середина, белое ядро. smoke — доля дыма вместо огня."""
    center = size / 2
    half = (size / 2 - 1) * grow
    red, orange, gold, gray = RAMPS["red"], RAMPS["orange"], RAMPS["gold"], RAMPS["gray"]
    outer = gray[2] if smoke > 0.6 else red[2]
    middle = gray[3] if smoke > 0.6 else orange[2] if smoke > 0.3 else orange[3]
    parts = [
        (pixel.polygon(size, pixel.star_points(center, half, half * 0.56, 9, -90)), outer),
        (pixel.polygon(size, pixel.star_points(center, half * 0.74, half * 0.42, 9, -70)), middle),
    ]
    if smoke < 0.6:
        parts.append((pixel.polygon(size, pixel.star_points(center, half * 0.5, half * 0.26, 8, -90)), gold[3]))
    if smoke < 0.3:
        parts.append((pixel.polygon(size, pixel.star_points(center, half * 0.3, half * 0.14, 4, -90)), gold[5]))
    return pixel.layers(size, parts, gray[0] if smoke > 0.6 else red[0])


put("explosion", explosion(16))
put("boom_1", explosion(32, 0.45))
put("boom_2", explosion(32, 0.8))
put("boom_3", explosion(32, 1.0, smoke=0.4))
put("boom_4", explosion(32, 1.0, smoke=0.8))

for ramp in ("gold", "orange", "red", "pink", "purple", "blue", "teal", "ice", "green", "lime", "white", "blood",
             "ink"):
    put(f"impact_{ramp}", pixel.burst(16, ramp, spikes=8))
    put(f"flash_{ramp}", pixel.burst(32, ramp, spikes=12, radii=(0.96, 0.4, 0.6, 0.3, 0.34, 0.16)))
    put(f"ring_{ramp}", pixel.ring(32, 13.5, 3.2, ramp))
    put(f"halo_{ramp}", pixel.ring(16, 6.0, 2.2, ramp))
    put(f"slash_{ramp}", pixel.crescent(32, ramp))


def claw(ramp):
    """Три параллельных следа когтей."""
    image = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    mark = pixel.crescent(32, ramp, radius=0.92, inner=0.98, shift=(0.16, 0.1), outline=True)
    for offset in (-7, 0, 7):
        image.alpha_composite(pixel.shift(mark, offset, -offset // 2))
    return image


for ramp in ("blood", "red", "white", "purple"):
    put(f"claw_{ramp}", claw(ramp))


def circle(ramp, size=64, star=5, runes=12):
    """Магический круг: два кольца, насечки-руны между ними и звезда внутри."""
    colors = RAMPS[ramp]
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    center = size / 2 - 0.5

    def arc(radius, color, width=1):
        steps = int(radius * 12)
        points = [(center + math.cos(math.tau * i / steps) * radius, center + math.sin(math.tau * i / steps) * radius)
                  for i in range(steps + 1)]
        pixel.stroke(image, points, color, width)

    arc(size * 0.47, colors[2], 3)
    arc(size * 0.47, colors[4], 1)
    arc(size * 0.37, colors[3], 2)
    for index in range(runes):
        angle = math.tau * index / runes
        inner, outer = size * 0.39, size * 0.45
        tilt = 0.09 if index % 2 else -0.09
        pixel.stroke(image, [
            (center + math.cos(angle) * inner, center + math.sin(angle) * inner),
            (center + math.cos(angle + tilt) * outer, center + math.sin(angle + tilt) * outer)], colors[5], 1)
    if star:
        radius = size * 0.36
        tips = [(center + math.cos(math.tau * i / star - math.pi / 2) * radius,
                 center + math.sin(math.tau * i / star - math.pi / 2) * radius) for i in range(star)]
        step = 2 if star % 2 else 3
        for index in range(star):
            pixel.stroke(image, [tips[index], tips[(index + step) % star]], colors[2], 3)
        for index in range(star):
            pixel.stroke(image, [tips[index], tips[(index + step) % star]], colors[4], 1)
    return image


put("circle_purple", circle("purple", star=6))
put("circle_teal", circle("teal", star=6))
put("circle_gold", circle("gold", star=8, runes=16))
put("circle_ice", circle("ice", star=6, runes=18))
put("circle_pink", circle("pink", star=0, runes=16))
put("pentagram_decal", circle("blood", star=5, runes=10))


def pentagram_icon():
    """Иконка пентаграммы: тёмный диск со звездой."""
    blood = RAMPS["blood"]
    disc = pixel.shape(16, lambda x, y: 0.92 - math.hypot(x, y), "blood", bands=(2.0, 3.0), outline=True)
    for y in range(16):
        for x in range(16):
            if disc.getpixel((x, y))[3] and disc.getpixel((x, y)) != rgba(blood[0]):
                disc.putpixel((x, y), rgba(blood[1]))
    center, radius = 7.5, 5.6
    tips = [(center + math.cos(math.tau * i / 5 - math.pi / 2) * radius,
             center + math.sin(math.tau * i / 5 - math.pi / 2) * radius) for i in range(5)]
    for index in range(5):
        pixel.stroke(disc, [tips[index], tips[(index + 2) % 5]], blood[4], 1)
    return disc


put("pentagram", pentagram_icon())
put("portal", pixel.vortex(16, "purple", arms=2, twist=2.6))
put("portal_big", pixel.vortex(32, "purple", arms=3, twist=3.2))
put("black_hole", pixel.vortex(16, "purple", arms=3, twist=2.2, hole=0.46, core=RAMPS["ink"][0]))
put("black_hole_big", pixel.vortex(32, "purple", arms=4, twist=2.8, hole=0.42, core=RAMPS["ink"][0]))
put("swirl_teal", pixel.vortex(32, "teal", arms=2, twist=3.0))
put("swirl_white", pixel.vortex(32, "white", arms=3, twist=2.4))


def pool(ramp, seed):
    """Лужа: неровное пятно с бликом."""
    colors = [rgba(color) for color in RAMPS[ramp]]
    size, center = 32, 16
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    filled = {}
    for py in range(size):
        for px in range(size):
            x, y = (px + 0.5 - center) / center, (py + 0.5 - center) / center
            angle = math.atan2(y, x)
            edge = 0.72 + 0.1 * math.sin(angle * 3 + seed) + 0.07 * math.sin(angle * 5 + seed * 2.3) \
                + 0.05 * math.sin(angle * 9 + seed * 0.7)
            radius = math.hypot(x, y)
            if radius > edge:
                continue
            tone = 2 if radius > edge - 0.1 else 3
            if math.hypot(x + 0.28, y + 0.3) < 0.16:
                tone = 5
            elif math.hypot(x + 0.22, y + 0.24) < 0.3:
                tone = 4
            image.putpixel((px, py), colors[tone])
            filled[(px, py)] = 0
    pixel.add_outline(image, filled, [colors[0]])
    return image


for index, ramp in enumerate(("blood", "ink", "lime", "blue", "purple")):
    put(f"pool_{ramp}", pool(ramp, 1.3 + index))


def beam(ramp):
    """Столб света: яркая середина, к краям темнее. Растягивается по высоте в мире."""
    colors = [rgba(color) for color in RAMPS[ramp]]
    image = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    columns = {3: 2, 4: 3, 5: 4, 6: 5, 7: 5, 8: 5, 9: 5, 10: 4, 11: 3, 12: 2}
    for x, tone in columns.items():
        for y in range(16):
            # Края слегка «дышат», чтобы столб не выглядел прямоугольником.
            if x in (3, 12) and y % 4 == 1:
                continue
            image.putpixel((x, y), colors[tone])
    return image


for ramp in ("gold", "white", "teal", "purple", "ice", "red"):
    put(f"beam_{ramp}", beam(ramp))


def thunder(ramp, flip=False):
    """Длинная молния от неба до земли."""
    colors = RAMPS[ramp]
    image = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    path = [(17, 0), (13, 7), (18, 11), (11, 19), (16, 22), (12, 31)]
    branch = [(18, 11), (23, 15), (21, 20)]
    pixel.stroke(image, path, colors[3], 4)
    pixel.stroke(image, branch, colors[3], 2)
    pixel.stroke(image, path, colors[5], 2)
    image = pixel.outline_mask(image, colors[0])
    return pixel.mirror(image) if flip else image


put("thunder_1", thunder("gold"))
put("thunder_2", thunder("gold", flip=True))
put("thunder_teal", thunder("teal"))
put("thunder_purple", thunder("purple"))


def firework_icon(first, second):
    """Салют: лучи двух цветов и искры на концах."""
    image = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    center = 7.5
    for index in range(8):
        ramp = RAMPS[first if index % 2 == 0 else second]
        angle = math.tau * index / 8 - math.pi / 2
        reach = 6.4 if index % 2 == 0 else 5.0
        for step, tone in ((2.2, 5), (3.4, 4), (4.6, 3), (reach, 4)):
            x = round(center + math.cos(angle) * min(step, reach))
            y = round(center + math.sin(angle) * min(step, reach))
            image.putpixel((x, y), rgba(ramp[tone]))
    for x, y in ((7, 7), (8, 7), (7, 8), (8, 8)):
        image.putpixel((x, y), rgba("#ffffff"))
    return pixel.outline_mask(image, RAMPS[first][0])


put("farewell", firework_icon("blue", "purple"))
put("salute", firework_icon("gold", "red"))


def claws(ramp):
    """Три следа когтей: изогнутые полосы, сужающиеся к концам."""
    colors = RAMPS[ramp]
    image = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    for offset in (-8, 0, 8):
        spine = [(7 + offset * 0.9 + 14 * t + 5 * math.sin(t * math.pi), 3 + 26 * t) for t in
                 [i / 12 for i in range(13)]]
        for index in range(len(spine) - 1):
            middle = 1 - abs(index - 5.5) / 6.5
            width = 1 + round(3 * middle)
            pixel.stroke(image, [spine[index], spine[index + 1]], colors[3] if middle < 0.5 else colors[4], width)
        pixel.stroke(image, spine[3:10], colors[5], 1)
    return pixel.outline_mask(image, colors[0])


for ramp in ("blood", "red", "white", "purple"):
    put(f"claw_{ramp}", claws(ramp))


def firework(first, second):
    """Салют: толстые лучи двух цветов с искрами на концах."""
    image = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    center = 7.5
    for index in range(8):
        ramp = RAMPS[first if index % 2 == 0 else second]
        angle = math.tau * index / 8 - math.pi / 2
        reach = 6.6 if index % 2 == 0 else 5.2
        inner = (center + math.cos(angle) * 2.4, center + math.sin(angle) * 2.4)
        outer = (center + math.cos(angle) * reach, center + math.sin(angle) * reach)
        pixel.stroke(image, [inner, outer], ramp[3], 2)
        pixel.stroke(image, [inner, (center + math.cos(angle) * (reach - 2), center + math.sin(angle) * (reach - 2))],
                     ramp[4], 1)
    for x in range(6, 10):
        for y in range(6, 10):
            if (x, y) not in ((6, 6), (9, 6), (6, 9), (9, 9)):
                image.putpixel((x, y), rgba("#ffffff"))
    return pixel.outline_mask(image, RAMPS[first][0])


put("farewell", firework("blue", "purple"))
put("salute", firework("gold", "red"))
