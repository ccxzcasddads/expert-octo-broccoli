"""Пиксель-арт из кода: палитры, спрайты из текстовых сеток и простые фигуры.

Спрайт рисуется строками символов. Каждый символ — тон одной из палитр спрайта:

    палитра 0: 1 2 3 4 5 (от тёмного к блику), o — контур
    палитра 1: a b c d e, f — контур
    палитра 2: q r s t u, v — контур
    палитра 3: A B C D E, F — контур
    W — белый, K — почти чёрный бордовый, «.» — прозрачно

Контур вокруг силуэта добавляется сам, в цвет той палитры, к которой примыкает.
"""
from __future__ import annotations

import math

from PIL import Image

# Палитры: контур и пять тонов от тёмного к блику.
RAMPS = {
    "red": ["#4a0612", "#9c1426", "#d42a3c", "#f75764", "#ff9aa2", "#ffe0e0"],
    "blood": ["#30040a", "#6d0c1f", "#a8101e", "#dc2c39", "#ff707a", "#ffc4c4"],
    "orange": ["#5a1804", "#b8400c", "#ee7418", "#ffa62e", "#ffd45c", "#fff6c0"],
    "gold": ["#5a2a06", "#aa5e0e", "#e4921a", "#ffc83c", "#ffec92", "#fffcde"],
    "green": ["#0a3416", "#1c682e", "#2d913f", "#52c456", "#a4ee84", "#e4ffc8"],
    "lime": ["#1c3a06", "#3e7c10", "#70bc20", "#a8e23c", "#dcfc8c", "#f8ffd8"],
    "teal": ["#05303a", "#0e7288", "#1cb0c4", "#56e4ec", "#b4faff", "#f0ffff"],
    "blue": ["#0c1c58", "#2040a0", "#3e6cd5", "#6ca8ff", "#b4dcff", "#eef8ff"],
    "ice": ["#1c4674", "#4a8cc4", "#8fd8ff", "#c4f0ff", "#ecfcff", "#ffffff"],
    "purple": ["#260a50", "#501e98", "#8848d8", "#b888ff", "#e0c8ff", "#f8f0ff"],
    "pink": ["#580c3a", "#a81c6c", "#e0489c", "#ff8cc8", "#ffc8e6", "#fff0f8"],
    "white": ["#342c3c", "#8a8494", "#c4c0cc", "#eceaf2", "#ffffff", "#ffffff"],
    "gray": ["#1a1a22", "#44444f", "#747482", "#a8a8b4", "#d8d8e0", "#f4f4f8"],
    "ink": ["#07050b", "#1a1622", "#322e46", "#565072", "#8a86ac", "#c4c0de"],
    "brown": ["#2a1206", "#5c2e10", "#8c5020", "#b87838", "#e0a860", "#f8dca4"],
    "skin": ["#3c1c10", "#8c5a3c", "#c69c7b", "#e8c4a0", "#fce4c8", "#fff4e4"],
    "bordo": ["#16070c", "#5c0a1a", "#861226", "#ba182c", "#fa5c68", "#ff9aa2"],
}

BORDO_BLACK = "#16070c"
CHARSETS = (("12345", "o"), ("abcde", "f"), ("qrstu", "v"), ("ABCDE", "F"))


def rgba(color, alpha=255):
    """«#rrggbb» → (r, g, b, a)."""
    if isinstance(color, tuple):
        return color if len(color) == 4 else (*color, alpha)
    color = color.lstrip("#")
    return (int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16), alpha)


def lookup(ramps):
    """Символ → (цвет, номер палитры)."""
    table = {"W": (rgba("#ffffff"), 0), "K": (rgba(BORDO_BLACK), 0)}
    for index, name in enumerate(ramps):
        ramp = RAMPS[name]
        tones, outline = CHARSETS[index]
        for tone, char in enumerate(tones, start=1):
            table[char] = (rgba(ramp[tone]), index)
        table[outline] = (rgba(ramp[0]), index)
    return table


def sprite(art, ramps=("red",), size=16, outline=True, dx=0, dy=0):
    """Картинка из текстовой сетки; рисунок меньше холста ставится по центру."""
    if isinstance(ramps, str):
        ramps = (ramps,)
    rows = [row for row in art.strip("\n").split("\n")]
    width = max(len(row) for row in rows)
    rows = [row.ljust(width, ".") for row in rows]
    height = len(rows)
    if width > size or height > size:
        raise ValueError(f"рисунок {width}x{height} больше холста {size}")
    table = lookup(ramps)
    left = (size - width) // 2 + dx
    top = (size - height) // 2 + dy
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    owner = {}
    for y, row in enumerate(rows):
        for x, char in enumerate(row):
            if char in ". ":
                continue
            if char not in table:
                raise ValueError(f"неизвестный символ «{char}» в строке {y}")
            color, ramp = table[char]
            px, py = left + x, top + y
            if not (0 <= px < size and 0 <= py < size):
                raise ValueError("рисунок выходит за холст")
            image.putpixel((px, py), color)
            owner[(px, py)] = ramp
    if outline:
        add_outline(image, owner, [rgba(RAMPS[name][0]) for name in ramps])
    return image


def add_outline(image, owner, colors):
    """Контур в один пиксель вокруг силуэта; цвет берётся у соседней палитры."""
    size = image.size[0]
    edge = {}
    for (x, y), ramp in owner.items():
        for nx, ny in ((x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)):
            if 0 <= nx < size and 0 <= ny < image.size[1] and (nx, ny) not in owner:
                # Контур снизу и справа важнее: он задаёт «вес» фигуры.
                if (nx, ny) not in edge or ny > y or nx > x:
                    edge[(nx, ny)] = ramp
    for (x, y), ramp in edge.items():
        image.putpixel((x, y), colors[ramp])


def outline_mask(image, color):
    """Обводит непрозрачные пиксели готовой картинки одним цветом."""
    result = image.copy()
    width, height = image.size
    alpha = image.getchannel("A").load()
    fill = rgba(color)
    for y in range(height):
        for x in range(width):
            if alpha[x, y]:
                continue
            for nx, ny in ((x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)):
                if 0 <= nx < width and 0 <= ny < height and alpha[nx, ny]:
                    result.putpixel((x, y), fill)
                    break
    return result


def recolor(image, source, target):
    """Меняет палитру: каждый тон палитры source заменяется тем же тоном target."""
    mapping = {rgba(a): rgba(b) for a, b in zip(RAMPS[source], RAMPS[target])}
    result = image.copy()
    pixels = result.load()
    for y in range(result.size[1]):
        for x in range(result.size[0]):
            if pixels[x, y] in mapping:
                pixels[x, y] = mapping[pixels[x, y]]
    return result


def mirror(image):
    return image.transpose(Image.FLIP_LEFT_RIGHT)


def paste(base, image, x=0, y=0):
    """Накладывает картинку с учётом прозрачности и возвращает основу."""
    base.alpha_composite(image, (x, y))
    return base


def canvas(size=16):
    return Image.new("RGBA", (size, size), (0, 0, 0, 0))


def scale(image, factor):
    return image.resize((image.size[0] * factor, image.size[1] * factor), Image.NEAREST)


def shape(size, inside, ramp, light=(-0.6, -0.8), outline=True, bands=(0.35, 0.72)):
    """Фигура по формуле: inside(x, y) в координатах от -1 до 1 возвращает «глубину» (>0 — внутри).

    Тон выбирается по освещённости: свет падает слева сверху.
    """
    tones = [rgba(color) for color in RAMPS[ramp]]
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    filled = {}
    for py in range(size):
        for px in range(size):
            x = (px + 0.5) / size * 2 - 1
            y = (py + 0.5) / size * 2 - 1
            depth = inside(x, y)
            if depth is None or depth <= 0:
                continue
            filled[(px, py)] = (x, y, depth)
    for (px, py), (x, y, depth) in filled.items():
        lit = -(x * light[0] + y * light[1])
        edge = min(1.0, depth * 4)
        value = 0.5 + lit * 0.55 + (edge - 0.5) * 0.25
        tone = 2 if value < bands[0] else 3 if value < bands[1] else 4
        if value > 0.98:
            tone = 5
        if value < 0.08:
            tone = 1
        image.putpixel((px, py), tones[tone])
    if outline:
        add_outline(image, {key: 0 for key in filled}, [tones[0]])
    return image


def ring(size, radius, thickness, ramp, glow=True):
    """Плоское кольцо для следов на земле: яркая середина и тёмные края."""
    tones = [rgba(color) for color in RAMPS[ramp]]
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    center = size / 2
    for py in range(size):
        for px in range(size):
            distance = math.hypot(px + 0.5 - center, py + 0.5 - center)
            offset = abs(distance - radius) / (thickness / 2)
            if offset > 1:
                continue
            tone = 5 if offset < 0.25 and glow else 4 if offset < 0.5 else 3 if offset < 0.8 else 2
            image.putpixel((px, py), tones[tone])
    return image


def sheet(images, columns=8, factor=6, background="#8b8b8b", gap=2):
    """Лист для просмотра: все картинки на одном фоне."""
    cell = max(max(image.size) for image in images) + gap
    rows = (len(images) + columns - 1) // columns
    result = Image.new("RGBA", (columns * cell + gap, rows * cell + gap), rgba(background))
    for index, image in enumerate(images):
        x = gap + (index % columns) * cell + (cell - gap - image.size[0]) // 2
        y = gap + (index // columns) * cell + (cell - gap - image.size[1]) // 2
        result.alpha_composite(image, (x, y))
    return scale(result, factor)


def polygon(size, points, supersample=4):
    """Маска многоугольника; points — вершины в пикселях холста."""
    from PIL import ImageDraw

    big = Image.new("L", (size * supersample, size * supersample), 0)
    ImageDraw.Draw(big).polygon([(x * supersample, y * supersample) for x, y in points], fill=255)
    small = big.resize((size, size), Image.BOX)
    return {(x, y) for y in range(size) for x in range(size) if small.getpixel((x, y)) >= 128}


def star_points(center, outer, inner, spikes, rotation=-90.0):
    """Вершины звезды: лучи длиной outer и впадины inner."""
    points = []
    for index in range(spikes * 2):
        radius = outer if index % 2 == 0 else inner
        angle = math.radians(rotation + index * 180.0 / spikes)
        points.append((center + math.cos(angle) * radius, center + math.sin(angle) * radius))
    return points


def layers(size, parts, outline=None):
    """Накладывает маски слоями: parts — список (маска, цвет). Контур — по общему силуэту."""
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    union = set()
    for mask, color in parts:
        fill = rgba(color)
        for point in mask:
            image.putpixel(point, fill)
        union |= mask
    if outline:
        add_outline(image, {point: 0 for point in union}, [rgba(outline)])
    return image


def burst(size, ramp, spikes=8, radii=(0.92, 0.5, 0.66, 0.36, 0.42, 0.2), tones=(2, 4, 5), rotation=-90.0,
          outline=True):
    """Вспышка из вложенных звёзд: тёмная снаружи, светлая в середине."""
    colors = RAMPS[ramp]
    center = size / 2
    half = size / 2 - (1 if outline else 0)
    parts = []
    for index, tone in enumerate(tones):
        outer, inner = radii[index * 2] * half, radii[index * 2 + 1] * half
        turn = rotation + (180.0 / spikes if index % 2 else 0.0)
        parts.append((polygon(size, star_points(center, outer, inner, spikes, turn)), colors[tone]))
    return layers(size, parts, colors[0] if outline else None)


def vortex(size, ramp, arms=2, twist=5.0, hole=0.0, core=None, outline=True, limit=0.94, turn=0.0):
    """Спираль: рукава закручиваются к центру. core — цвет середины."""
    colors = [rgba(color) for color in RAMPS[ramp]]
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    center = size / 2
    filled = {}
    for py in range(size):
        for px in range(size):
            x = (px + 0.5 - center) / center
            y = (py + 0.5 - center) / center
            radius = math.hypot(x, y)
            if radius > limit:
                continue
            if radius < hole:
                if core:
                    image.putpixel((px, py), rgba(core))
                    filled[(px, py)] = 0
                continue
            angle = math.atan2(y, x) + turn
            wave = math.sin(arms * angle + twist * radius * math.pi)
            if wave > -0.15:
                tone = 5 if wave > 0.85 and radius < 0.6 else 4 if wave > 0.55 else 3 if wave > 0.2 else 2
                image.putpixel((px, py), colors[tone])
                filled[(px, py)] = 0
            elif radius < limit * 0.8:
                image.putpixel((px, py), colors[1])
                filled[(px, py)] = 0
    if outline:
        add_outline(image, filled, [colors[0]])
    return image


def crescent(size, ramp, radius=0.9, inner=0.86, shift=(0.3, 0.18), outline=True, start=None):
    """Серп удара: большой круг минус сдвинутый круг поменьше."""
    colors = [rgba(color) for color in RAMPS[ramp]]
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    center = size / 2
    filled = {}
    for py in range(size):
        for px in range(size):
            x = (px + 0.5 - center) / center
            y = (py + 0.5 - center) / center
            outer = math.hypot(x, y)
            cut = math.hypot(x - shift[0], y - shift[1])
            if outer > radius or cut < inner:
                continue
            depth = (cut - inner) / max(0.001, radius + math.hypot(*shift) - inner)
            edge = (radius - outer) / radius
            tone = 5 if edge < 0.12 and depth > 0.25 else 4 if depth > 0.45 else 3 if depth > 0.2 else 2
            image.putpixel((px, py), colors[tone])
            filled[(px, py)] = 0
    if outline:
        add_outline(image, filled, [colors[0]])
    return image


def stroke(image, points, color, width=1):
    """Ломаная линия без сглаживания."""
    from PIL import ImageDraw

    ImageDraw.Draw(image).line(points, fill=rgba(color), width=width)
    return image


def rotate(image, quarter_turns):
    """Поворот на четверти оборота без потери пикселей."""
    return image.rotate(-90 * quarter_turns)


def shift(image, dx, dy):
    result = Image.new("RGBA", image.size, (0, 0, 0, 0))
    result.alpha_composite(image, (0, 0))
    return result.transform(image.size, Image.AFFINE, (1, 0, -dx, 0, 1, -dy))
