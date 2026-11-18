"""Фоны меню в стиле bordo: окно сундука 176 пикселей шириной, нарисованное целиком.

Шапка с короной, пустая табличка заголовка и инвентарь игрока берутся из шаблона kit/menu5.png
(набор оформления сервера), кнопка «Назад» — из kit/back.png. Всё остальное рисуется здесь:
заголовок шрифтом табличек, тематическая панель, ячейки под слоты и кнопки.

Слот k лежит в столбце k % 9 и ряду k // 9; его предмет 16x16 рисуется клиентом
в точке (8 + 18·столбец, 42 + 18·ряд) картинки.
"""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image

import pixel
from fx import SPRITES
from pixel import RAMPS, rgba

KIT = Path(__file__).resolve().parent / "kit"
BLACK = "#16070c"
ROWS = 5
WIDTH, HEIGHT = 176, 138 + 18 * ROWS
# Область рядов сундука в шаблоне: её содержимое заменяется фоном окна.
AREA = (7, 39, 168, 130)

TITLE_FONT = json.loads((KIT / "title_font.json").read_text(encoding="utf-8"))
TITLE_FONT["Ф"] = [
    "........", "........",
    "...##...", ".######.", "########", "##.##.##", "##.##.##", "########", ".######.", "...##...", "...##...",
    "...##...",
]
TITLE_ROWS = ["#fffcde"] * 4 + ["#ffec92"] * 3 + ["#ffc83c"] * 3 + ["#e4921a"] * 2

LABEL_FONT = {
    "А": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "Б": ["#####", "#....", "#....", "####.", "#...#", "#...#", "####."],
    "В": ["####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."],
    "Г": ["#####", "#....", "#....", "#....", "#....", "#....", "#...."],
    "Д": ["..###.", ".#..#.", ".#..#.", ".#..#.", ".#..#.", "######", "#....#"],
    "Е": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
    "Ж": ["#..#..#", "#..#..#", ".#.#.#.", "..###..", ".#.#.#.", "#..#..#", "#..#..#"],
    "З": ["####.", "....#", "....#", ".###.", "....#", "....#", "####."],
    "И": ["#...#", "#...#", "#..##", "#.#.#", "##..#", "#...#", "#...#"],
    "К": ["#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"],
    "Л": ["..###", ".#..#", ".#..#", ".#..#", ".#..#", ".#..#", "#...#"],
    "М": ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"],
    "Н": ["#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "О": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "П": ["#####", "#...#", "#...#", "#...#", "#...#", "#...#", "#...#"],
    "Р": ["####.", "#...#", "#...#", "####.", "#....", "#....", "#...."],
    "С": [".####", "#....", "#....", "#....", "#....", "#....", ".####"],
    "Т": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "У": ["#...#", "#...#", "#...#", ".####", "....#", "....#", "####."],
    "Ф": ["..#..", ".###.", "#.#.#", "#.#.#", ".###.", "..#..", "..#.."],
    "Х": ["#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"],
    "Ц": ["#...#.", "#...#.", "#...#.", "#...#.", "#...#.", "######", ".....#"],
    "Ч": ["#...#", "#...#", "#...#", ".####", "....#", "....#", "....#"],
    "Ш": ["#..#..#", "#..#..#", "#..#..#", "#..#..#", "#..#..#", "#..#..#", "#######"],
    "Ы": ["#.....#", "#.....#", "#.....#", "####..#", "#...#.#", "#...#.#", "####..#"],
    "Ь": ["#....", "#....", "#....", "####.", "#...#", "#...#", "####."],
    "Э": ["####.", "....#", "....#", ".####", "....#", "....#", "####."],
    "Ю": ["#..###.", "#.#...#", "#.#...#", "###...#", "#.#...#", "#.#...#", "#..###."],
    "Я": [".####", "#...#", "#...#", ".####", "..#.#", ".#..#", "#...#"],
}
LABEL_ROWS = ["#ffffff"] * 5 + ["#ffece4", "#f0d6d2"]


def text_mask(font, text, gap=1, space=4):
    """Точки текста относительно левого верхнего угла строки и её ширина."""
    points, x = set(), 0
    for char in text:
        if char == " ":
            x += space
            continue
        glyph = font[char]
        for row, line in enumerate(glyph):
            for column, value in enumerate(line):
                if value == "#":
                    points.add((x + column, row))
        x += len(glyph[0]) + gap
    return points, x - gap


def write(image, font, rows, text, center, top, outline=BLACK, shadow=None, space=4):
    """Пишет строку по центру: буквы с градиентом по рядам, контур и тень под ним."""
    points, width = text_mask(font, text, space=space)
    left = center - width // 2
    placed = {(left + x, top + y): rows[y] for x, y in points}
    edge = set()
    for x, y in placed:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if (x + dx, y + dy) not in placed:
                    edge.add((x + dx, y + dy))
    if shadow:
        for x, y in edge | set(placed):
            if (x, y + 1) not in placed and (x, y + 1) not in edge:
                image.putpixel((x, y + 1), rgba(shadow))
    for point in edge:
        image.putpixel(point, rgba(outline))
    for point, color in placed.items():
        image.putpixel(point, rgba(color))
    return left, width


def blank():
    """Шаблон без рядов сундука: на их месте фон окна с его точечным узором."""
    image = Image.open(KIT / "menu5.png").convert("RGBA")
    x0, y0, x1, y1 = AREA
    sample = next(y for y in range(y0, y1) if y % 8 == 4)
    delta = [a - b for a, b in zip(image.getpixel((4, sample)), image.getpixel((3, sample)))]
    for y in range(y0, y1 + 1):
        base = image.getpixel((3, y))
        dot = tuple(min(255, base[i] + delta[i]) for i in range(3)) + (255,)
        for x in range(x0, x1 + 1):
            dotted = (y % 8 == 4 and x % 8 == 4) or (y % 8 == 0 and x % 8 == 0)
            image.putpixel((x, y), dot if dotted else base)
    return image


def title(image, text):
    """Заголовок на табличке."""
    write(image, TITLE_FONT, TITLE_ROWS, text, WIDTH // 2, 20, shadow="#140208", space=5)


def mix(first, second, share):
    a, b = rgba(first), rgba(second)
    return tuple(round(a[i] + (b[i] - a[i]) * share) for i in range(3)) + (255,)


def panel(image, box, ramp):
    """Тематическая панель: контур, светлые верх и левый край, градиент с растром, тёмная кромка снизу."""
    colors = RAMPS[ramp]
    x0, y0, x1, y1 = box
    top, bottom = colors[3], colors[2]
    height = y1 - y0 - 1
    for y in range(y0 + 1, y1):
        share = (y - y0 - 1) / max(1, height - 1)
        # Четыре ступени градиента, между ними — шахматный растр.
        level = share * 4
        step = int(level)
        frac = level - step
        for x in range(x0 + 1, x1):
            dither = frac > 0.5 and (x + y) % 2 == 0
            tone = min(4, step + (1 if dither else 0)) / 4
            image.putpixel((x, y), mix(top, bottom, tone))
    for x in range(x0 + 1, x1):
        image.putpixel((x, y0 + 1), rgba(colors[4]))
        image.putpixel((x, y1 - 1), rgba(colors[1]))
        image.putpixel((x, y1 - 2), rgba(colors[1]) if x % 2 == 0 else mix(colors[1], colors[2], 0.5))
    for y in range(y0 + 1, y1):
        image.putpixel((x0 + 1, y), rgba(colors[4]))
        image.putpixel((x1 - 1, y), rgba(colors[1]))
    for x in range(x0 + 1, x1):
        image.putpixel((x, y0), rgba(BLACK))
        image.putpixel((x, y1), rgba(BLACK))
    for y in range(y0 + 1, y1):
        image.putpixel((x0, y), rgba(BLACK))
        image.putpixel((x1, y), rgba(BLACK))


def cell(image, column, row, ramp):
    """Ячейка под слот: тёмная, чуть светлее к середине, с бликом по правому и нижнему краю."""
    colors = RAMPS[ramp]
    x0, y0 = 7 + 18 * column, 41 + 18 * row
    dark = mix(colors[0], "#000000", 0.35)
    middle = mix(colors[0], colors[1], 0.55)
    for y in range(18):
        for x in range(18):
            ring = x in (0, 17) or y in (0, 17)
            if ring:
                if (x in (0, 17)) and (y in (0, 17)):
                    continue
                image.putpixel((x0 + x, y0 + y), rgba(BLACK))
                continue
            distance = max(abs(x - 8.5), abs(y - 8.5)) / 8.0
            if distance < 0.38:
                color = middle
            elif distance < 0.62:
                color = middle if (x + y) % 2 == 0 else mix(dark, middle, 0.5)
            elif distance < 0.86:
                color = mix(dark, middle, 0.5) if (x + y) % 2 == 0 else dark
            else:
                color = dark
            if x == 16 or y == 16:
                color = mix(colors[1], colors[2], 0.35)
            image.putpixel((x0 + x, y0 + y), color)


def sparkle(image, x, y, size=1, color="#ffffff"):
    for offset in range(-size, size + 1):
        image.putpixel((x + offset, y), rgba(color))
        image.putpixel((x, y + offset), rgba(color))


def decor(image, name, column, row, dx=0, dy=0):
    """Украшение из набора спрайтов в клетке слота."""
    sprite = SPRITES[name] if isinstance(name, str) else name
    image.alpha_composite(sprite, (8 + 18 * column + dx, 42 + 18 * row + dy))


def plate(image, column, row, text, gem="gem_red"):
    """Тёмная кнопка с золотой рамкой на четыре слота, как «Сбросить» в меню титулов."""
    x0, y0 = 8 + 18 * column, 42 + 18 * row
    width = 70
    fill = ["#751d2d", "#721c2c", "#701b2b", "#6d1a2a", "#6a1929", "#671828", "#651626", "#621525", "#5f1424",
            "#5c1323", "#5a1222"]
    for x in range(1, width - 1):
        image.putpixel((x0 + x, y0), rgba(BLACK))
        image.putpixel((x0 + x, y0 + 1), rgba("#ffec92"))
        for index, color in enumerate(fill):
            image.putpixel((x0 + x, y0 + 2 + index), rgba(color))
        image.putpixel((x0 + x, y0 + 13), rgba("#3a0a16"))
        image.putpixel((x0 + x, y0 + 14), rgba("#20040c"))
        image.putpixel((x0 + x, y0 + 15), rgba(BLACK))
        image.putpixel((x0 + x, y0 + 16), rgba("#540816"))
    for y in range(1, 15):
        image.putpixel((x0, y0 + y), rgba(BLACK))
        image.putpixel((x0 + width - 1, y0 + y), rgba(BLACK))
    for y in range(2, 13):
        image.putpixel((x0 + 1, y0 + y), rgba("#ffc83c"))
        image.putpixel((x0 + width - 2, y0 + y), rgba("#e4921a"))
    image.putpixel((x0 + 1, y0 + 1), rgba("#ae7882"))
    image.putpixel((x0 + width - 2, y0 + 1), rgba("#ae7882"))
    points, text_width = text_mask(LABEL_FONT, text)
    icon = small_gem(gem)
    total = 9 + 3 + text_width
    left = x0 + (width - total) // 2
    image.alpha_composite(icon, (left, y0 + 3))
    write(image, LABEL_FONT, LABEL_ROWS, text, left + 12 + text_width // 2, y0 + 4, shadow="#20040c")


def small_gem(name):
    """Камень 9x9 для кнопок: ромб с бликом."""
    ramp = name.split("_", 1)[1]
    return pixel.sprite("""
..444..
.45543.
4554433
4544333
4443332
.43332.
..322..
""", (ramp,), size=9)


def back(image, column, row):
    """Кнопка «Назад» с дверью на четыре слота."""
    button = Image.open(KIT / "back.png").convert("RGBA")
    image.alpha_composite(button, (8 + 18 * column, 42 + 18 * row))


def divider(image, text, row, ramp):
    """Подпись раздела по центру ряда и золотые линии с ромбами по бокам."""
    y = 41 + 18 * row + 6
    left, width = write(image, LABEL_FONT, LABEL_ROWS, text, WIDTH // 2, y, outline=RAMPS[ramp][0],
                        shadow=RAMPS[ramp][0])
    middle = y + 3
    for start, end in ((16, left - 6), (left + width + 5, WIDTH - 17)):
        for x in range(start, end + 1):
            image.putpixel((x, middle), rgba("#ffc83c"))
            image.putpixel((x, middle + 1), rgba("#aa5e0e"))
        for x in (start, end):
            sparkle(image, x, middle, 1, "#ffec92")
            image.putpixel((x, middle), rgba("#fffcde"))


# ── Меню ─────────────────────────────────────────────────────────────────

# Панель занимает четыре ряда; пятый ряд — кнопки на фоне окна.
PANEL = (7, 39, 168, 113)

# категория → (заголовок, палитра панели, эмблема, украшения по бокам)
CATEGORIES = {
    "sword": ("МЕЧИ", "teal", "sword", ("star_gold", "gem_blue")),
    "pickaxe": ("КИРКИ", "orange", "pickaxe", ("star_gold", "gem_red")),
    "totem": ("ТОТЕМЫ", "green", "totem", ("star_gold", "gem_green")),
    "hat": ("ШЛЯПЫ", "purple", "hat", ("star_gold", "gem_purple")),
    "kill": ("УБИЙСТВА", "ink", "bones", ("skull_white", "gem_red")),
    "crit": ("КРИТЫ", "gold", "impact_red", ("star_white", "gem_red")),
    "projectile": ("СНАРЯДЫ", "blue", "star_gold", ("star_gold", "gem_teal")),
    "firework": ("ФЕЙЕРВЕРКИ", "pink", "salute", ("star_gold", "gem_pink")),
    "death": ("СМЕРТЬ", "gray", "ghost", ("wisp_teal", "gem_teal")),
}


def stars(image, ramp, points):
    """Мелкие блёстки на панели."""
    for index, (x, y) in enumerate(points):
        sparkle(image, x, y, 1 if index % 3 else 2, "#ffffff" if index % 2 else RAMPS[ramp][5])


def main_menu():
    image = blank()
    title(image, "КОСМЕТИКА")
    panel(image, PANEL, "purple")
    stars(image, "purple", [(14, 46), (160, 50), (22, 70), (153, 72), (14, 100), (161, 104), (88, 44)])
    divider(image, "ОБЛИКИ", 0, "purple")
    for column in (1, 3, 5, 7):
        cell(image, column, 1, "purple")
    for column in (2, 4, 6):
        decor(image, "glint_gold", column, 1)
    divider(image, "ЭФФЕКТЫ", 2, "purple")
    for column in range(2, 7):
        cell(image, column, 3, "purple")
    decor(image, "star_gold", 1, 3)
    decor(image, "star_gold", 7, 3)
    plate(image, 0, 4, "СБРОСИТЬ")
    back(image, 5, 4)
    decor(image, "gem_red", 4, 4, dy=1)
    return image


def category_menu(key):
    heading, ramp, emblem, (first, second) = CATEGORIES[key]
    image = blank()
    title(image, heading)
    panel(image, PANEL, ramp)
    stars(image, ramp, [(30, 46), (58, 52), (118, 47), (146, 53), (16, 44), (160, 45)])
    decor(image, emblem, 4, 0)
    decor(image, first, 1, 0)
    decor(image, first, 7, 0)
    for row in (1, 2, 3):
        for column in range(1, 8):
            cell(image, column, row, ramp)
    for row, name in ((1, first), (2, second), (3, first)):
        decor(image, name, 0, row)
        decor(image, name, 8, row)
    back(image, 0, 4)
    plate(image, 5, 4, "СНЯТЬ")
    decor(image, second, 4, 4, dy=1)
    return image


def build():
    """Имя картинки → картинка."""
    menus = {"main": main_menu()}
    for key in CATEGORIES:
        menus[key] = category_menu(key)
    return menus
