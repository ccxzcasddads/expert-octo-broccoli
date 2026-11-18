"""Проверяет, что конфиги эффектов и меню ссылаются только на существующие спрайты и иконки.

    python3 tools/textures/check.py

Нужны Python 3, Pillow и PyYAML. Проверяется:
  * каждый спрайт из полей sprite и frames есть в fx.py и в собранном наборе;
  * каждая иконка вида model:applecosmetic:gui/… есть в icons.py и в наборе;
  * каждое движение (animation) есть в Animation.java;
  * у каждой категории эффектов в config.yml есть фон окна в шрифте applecosmetic:menu.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

import fx  # noqa: E402
import icons  # noqa: E402

RESOURCES = ROOT / "src/main/resources"
ASSETS = RESOURCES / "pack/itemsadder/contents/applecosmetic_raw/resourcepack/assets/applecosmetic"
ANIMATIONS = set(re.findall(r"^    ([A-Z_]+)\(", (ROOT / "src/main/java/ru/applecosmetic/effect/Animation.java")
                            .read_text(encoding="utf-8"), re.M))
BUILT_IN = re.compile(r"[a-z0-9_]+")
ICON = re.compile(r"model:applecosmetic:(gui|fx)/([a-z0-9_]+)")

problems = []


def names(value):
    if value is None:
        return []
    return [str(entry) for entry in value] if isinstance(value, list) else [str(value)]


def check_sprites(where, params):
    for name in names(params.get("sprite")) + names(params.get("frames")):
        if not BUILT_IN.fullmatch(name):
            continue
        if name not in fx.SPRITES:
            problems.append(f"{where}: нет спрайта «{name}»")
        elif not (ASSETS / f"items/fx/{name}.json").is_file():
            problems.append(f"{where}: спрайт «{name}» не собран — запустите build.py")


def check_icon(where, spec):
    for entry in names(spec):
        match = ICON.fullmatch(entry)
        if not match:
            continue
        folder, name = match.groups()
        table = icons.ICONS if folder == "gui" else fx.SPRITES
        if name not in table:
            problems.append(f"{where}: нет иконки «{entry}»")
        elif not (ASSETS / f"items/{folder}/{name}.json").is_file():
            problems.append(f"{where}: иконка «{entry}» не собрана — запустите build.py")


def walk_icons(where, node):
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "icon":
                check_icon(where, value)
            else:
                walk_icons(f"{where}.{key}", value)


total = 0
for path in sorted((RESOURCES / "effects").glob("*.yml")):
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    for key, effect in data["effects"].items():
        total += 1
        where = f"{path.name} → {key}"
        check_icon(where, effect.get("icon"))
        if "trail" in effect:
            check_sprites(where + " (trail)", effect["trail"])
        for index, layer in enumerate(effect.get("layers", []), start=1):
            if layer.get("animation", "BURST") not in ANIMATIONS:
                problems.append(f"{where}: неизвестное движение «{layer.get('animation')}»")
            check_sprites(f"{where} (слой {index})", layer)
        if not effect.get("layers") and "trail" not in effect:
            problems.append(f"{where}: нет ни слоёв, ни следа")

config = yaml.safe_load((RESOURCES / "config.yml").read_text(encoding="utf-8"))
walk_icons("config.yml", config)
font = json.loads((ASSETS / "font/menu.json").read_text(encoding="utf-8"))
glyphs = {char for provider in font["providers"] for char in "".join(provider.get("chars", []))}
for key, category in config["menu"]["main"]["categories"].items():
    if category.get("background") not in glyphs:
        problems.append(f"config.yml → menu.main.categories.{key}: фона нет в шрифте applecosmetic:menu")

for problem in problems:
    print("ОШИБКА:", problem)
print(f"эффектов: {total}, спрайтов: {len(fx.SPRITES)}, иконок: {len(icons.ICONS)}, движений: {len(ANIMATIONS)}, "
      f"ошибок: {len(problems)}")
sys.exit(1 if problems else 0)
