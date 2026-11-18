"""Собирает текстуры эффектов и меню: спрайты, иконки, фоны меню, шрифты и оформление подсказок.

    python3 tools/textures/build.py    — пересобрать набор для ItemsAdder и листы превью

Нужны Python 3 и Pillow. Спрайты описаны в fx.py, иконки — в icons.py, фоны меню — в menus.py.
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

from PIL import Image, ImageDraw  # noqa: E402

import fx  # noqa: E402
import icons  # noqa: E402
import menus  # noqa: E402
import pixel  # noqa: E402

NAMESPACE = "applecosmetic"
MODULE = ROOT / "src/main/resources/pack/itemsadder/contents/applecosmetic_raw"
ASSETS = MODULE / "resourcepack/assets" / NAMESPACE
PREVIEW = ROOT / "docs/preview"
KIT = HERE / "kit"

# Символы шрифта applecosmetic:menu: сдвиг заголовка и фоны окон.
SHIFT = "\ue000"
BACKGROUNDS = {"main": "\ue001", "sword": "\ue010", "pickaxe": "\ue011", "totem": "\ue012", "hat": "\ue013",
               "kill": "\ue014", "crit": "\ue015", "projectile": "\ue016", "firework": "\ue017", "death": "\ue018"}
# Значки шрифта applecosmetic:bold: {|}, {ЛКМ}, {ПКМ}, {СКМ}, яблоко и {•}.
BOLD_ICONS = "\ue100\ue101\ue102\ue103\ue104\ue105"
BOLD_ROWS = [
    "АБВГДЕЁЖЗИЙКЛМНО", "ПРСТУФХЦЧШЩЪЫЬЭЮ", "ЯІЇЄҐABCDEFGHIJK", "LMNOPQRSTUVWXYZ0", "123456789.,:;!?-",
    "+=/\\()[]<>«»\"'%#", "*_|°№~",
]


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    # Только ASCII: символы шрифтов из частной области Юникода записываются как \\uXXXX.
    path.write_text(json.dumps(data, ensure_ascii=True, indent=1), encoding="utf-8")


def write_png(path, image):
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, optimize=True)


def items(folder, table, tinted):
    """Текстура, плоская модель и описание предмета: модель предмета — applecosmetic:<folder>/<имя>."""
    for name, image in sorted(table.items()):
        write_png(ASSETS / f"textures/item/{folder}/{name}.png", image)
        write_json(ASSETS / f"models/item/{folder}/{name}.json", {
            "parent": "minecraft:item/generated",
            "textures": {"layer0": f"{NAMESPACE}:item/{folder}/{name}"},
        })
        model = {"type": "minecraft:model", "model": f"{NAMESPACE}:item/{folder}/{name}"}
        if tinted:
            # Окраска спрайта цветом кожаной брони: поля color и rainbow в слоях эффектов.
            model["tints"] = [{"type": "minecraft:dye", "default": 16777215}]
        write_json(ASSETS / f"items/{folder}/{name}.json", {"model": model})


def fonts(backgrounds):
    providers = [{"type": "space", "advances": {SHIFT: -8}}]
    for name, image in backgrounds.items():
        write_png(ASSETS / f"textures/font/menu/{name}.png", image)
        providers.append({"type": "bitmap", "file": f"{NAMESPACE}:font/menu/{name}.png",
                          "height": image.size[1], "ascent": 37, "chars": [BACKGROUNDS[name]]})
    write_json(ASSETS / "font/menu.json", {"providers": providers})

    shutil.copyfile(KIT / "bold.png", ASSETS / "textures/font/bold.png")
    empty = "\u0000"
    upper = [row.ljust(16, empty) for row in BOLD_ROWS] + [BOLD_ICONS.ljust(16, empty)]
    lower = []
    for row in upper[:4]:
        lower.append("".join(char.lower() if char.isalpha() else empty for char in row))
    lower += [empty * 16] * 4
    sheet = f"{NAMESPACE}:font/bold.png"
    write_json(ASSETS / "font/bold.json", {"providers": [
        {"type": "bitmap", "file": sheet, "height": 8, "ascent": 7, "chars": upper},
        {"type": "bitmap", "file": sheet, "height": 8, "ascent": 7, "chars": lower},
        {"type": "space", "advances": {" ": 4}},
        {"type": "reference", "id": "minecraft:default"},
    ]})


def tooltip():
    target = ASSETS / "textures/gui/sprites/tooltip"
    target.mkdir(parents=True, exist_ok=True)
    for name in ("menu_background.png", "menu_background.png.mcmeta", "menu_frame.png", "menu_frame.png.mcmeta"):
        shutil.copyfile(KIT / f"tooltip_{name}", target / name)


def mock(background, placed):
    """Окно меню с иконками в слотах: так его видит игрок."""
    image = background.copy()
    for slot, icon in placed.items():
        image.alpha_composite(icon, (8 + 18 * (slot % 9), 42 + 18 * (slot // 9)))
    return image


def captioned_sheet(table, columns, factor=4):
    """Лист спрайтов с подписями — справочник названий для конфигов."""
    names = sorted(table)
    cell_w, cell_h = 86, 16 * factor + 16
    rows = (len(names) + columns - 1) // columns
    sheet = Image.new("RGBA", (columns * cell_w, rows * cell_h), pixel.rgba("#2a2030"))
    draw = ImageDraw.Draw(sheet)
    for index, name in enumerate(names):
        image = table[name]
        scale = factor if image.size[0] <= 16 else max(1, factor * 16 // image.size[0])
        big = pixel.scale(image, scale)
        x = (index % columns) * cell_w
        y = (index // columns) * cell_h
        sheet.alpha_composite(big, (x + (cell_w - big.size[0]) // 2, y + 2 + (16 * factor - big.size[1]) // 2))
        draw.text((x + cell_w // 2, y + 16 * factor + 9), name, fill=(232, 224, 236, 255), anchor="mm")
    return sheet


def previews(backgrounds):
    PREVIEW.mkdir(parents=True, exist_ok=True)
    slots = [10, 11, 12, 13, 14, 15, 16, 19, 20, 21, 22, 23, 24, 25, 28, 29, 30, 31, 32, 33, 34]
    main = mock(backgrounds["main"], {
        10: icons.ICONS["cat_sword"], 12: icons.ICONS["cat_pickaxe"], 14: icons.ICONS["cat_totem"],
        16: icons.ICONS["cat_hat"], 29: icons.ICONS["cat_kill"], 30: icons.ICONS["cat_crit"],
        31: icons.ICONS["cat_projectile"], 32: icons.ICONS["cat_firework"], 33: icons.ICONS["cat_death"],
    })
    shots = [main]
    for category in ("kill", "crit", "projectile", "firework", "death"):
        names = [name for name in icons.ICONS if name.startswith(category + "_")]
        shots.append(mock(backgrounds[category], {slot: icons.ICONS[name] for slot, name in zip(slots, names)}))
    gap, factor = 8, 2
    width, height = shots[0].size
    sheet = Image.new("RGBA", (3 * (width + gap) + gap, 2 * (height + gap) + gap), pixel.rgba("#1a0f14"))
    for index, shot in enumerate(shots):
        sheet.alpha_composite(shot, (gap + (index % 3) * (width + gap), gap + (index // 3) * (height + gap)))
    pixel.scale(sheet, factor).save(PREVIEW / "menus.png", optimize=True)

    # По ряду на категорию; в ряду пятнадцать мест, пустые остаются прозрачными.
    effect_icons = []
    for category in ("kill", "crit", "projectile", "firework", "death"):
        row = [image for name, image in icons.ICONS.items() if name.startswith(category + "_")]
        effect_icons += row + [icons.ICONS["invisible"]] * (15 - len(row))
    pixel.sheet(effect_icons, columns=15, factor=4, background="#3e0a16").save(PREVIEW / "effect_icons.png",
                                                                               optimize=True)
    captioned_sheet(fx.SPRITES, columns=12).save(PREVIEW / "sprites.png", optimize=True)


def main():
    if MODULE.exists():
        shutil.rmtree(MODULE)
    backgrounds = menus.build()
    items("fx", fx.SPRITES, tinted=True)
    items("gui", icons.ICONS, tinted=False)
    fonts(backgrounds)
    tooltip()
    previews(backgrounds)
    files = sum(1 for path in MODULE.rglob("*") if path.is_file())
    print(f"спрайтов: {len(fx.SPRITES)}, иконок: {len(icons.ICONS)}, фонов меню: {len(backgrounds)}, "
          f"файлов в наборе: {files}")


if __name__ == "__main__":
    main()
