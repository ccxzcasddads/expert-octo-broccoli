package ru.applecosmetic.effect;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ThreadLocalRandom;
import java.util.function.Consumer;
import java.util.regex.Pattern;
import org.bukkit.Color;
import org.bukkit.Material;
import org.bukkit.NamespacedKey;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.meta.LeatherArmorMeta;
import ru.applecosmetic.item.ItemResolver;
import ru.applecosmetic.util.Params;

/**
 * Спрайт эффекта: картинка из ресурспака, которую в мире показывает предмет с этой моделью.
 * В конфиге: sprite — один спрайт или список (для каждой частицы выбирается случайный),
 * frames — кадры, которые сменяются по порядку.
 */
public final class SpriteSpec {

    /** Встроенные спрайты лежат в ресурспаке как applecosmetic:fx/имя. */
    public static final String NAMESPACE = "applecosmetic";
    private static final Pattern BUILT_IN = Pattern.compile("[a-z0-9_]+");

    private final List<ItemStack> variants;
    private final List<ItemStack> frames;
    private final int frameTicks;
    private final boolean rainbow;
    private final boolean glow;

    private SpriteSpec(List<ItemStack> variants, List<ItemStack> frames, int frameTicks, boolean rainbow,
                       boolean glow) {
        this.variants = variants;
        this.frames = frames;
        this.frameTicks = frameTicks;
        this.rainbow = rainbow;
        this.glow = glow;
    }

    /** Откуда берутся предметы спрайтов и какие встроенные спрайты существуют. */
    public interface Source {
        ItemResolver items();

        boolean hasSprite(String name);
    }

    /** Возвращает null и сообщает причину, если спрайт нельзя показать. */
    public static SpriteSpec parse(Params params, Source source, Consumer<String> warn) {
        List<String> names = params.strings("sprite");
        List<String> frameNames = params.strings("frames");
        if (names.isEmpty() && frameNames.isEmpty()) {
            warn.accept("не указан спрайт (sprite или frames)");
            return null;
        }
        Color color = params.has("color") ? params.color("color", null) : null;
        if (params.has("color") && color == null) {
            warn.accept("неверный цвет «" + params.string("color", "") + "», нужен формат #RRGGBB");
        }
        boolean rainbow = params.flag("rainbow", false);
        boolean tinted = color != null || rainbow;

        List<ItemStack> variants = items(names, source, tinted, color, warn);
        List<ItemStack> frames = items(frameNames, source, tinted, color, warn);
        if (variants.isEmpty() && frames.isEmpty()) {
            return null;
        }
        if (variants.isEmpty()) {
            variants = List.of(frames.get(0));
        }
        return new SpriteSpec(List.copyOf(variants), List.copyOf(frames),
                Math.max(1, Math.min(40, params.integer("frame-ticks", 2))), rainbow, params.flag("glow", true));
    }

    private static List<ItemStack> items(List<String> names, Source source, boolean tinted, Color color,
                                         Consumer<String> warn) {
        List<ItemStack> result = new ArrayList<>();
        for (String raw : names) {
            String name = raw.trim();
            ItemStack item = item(name, source, tinted, warn);
            if (item == null) {
                continue;
            }
            if (color != null) {
                tint(item, color);
            }
            result.add(item);
        }
        return result;
    }

    private static ItemStack item(String name, Source source, boolean tinted, Consumer<String> warn) {
        if (!BUILT_IN.matcher(name).matches()) {
            ItemStack item = source.items().resolve(name);
            if (item == null) {
                warn.accept("неизвестный предмет «" + name + "» в поле sprite");
            }
            return item;
        }
        if (!source.hasSprite(name)) {
            warn.accept("спрайта «" + name + "» нет во встроенном наборе: проверьте название"
                    + " или добавьте модель " + NAMESPACE + ":fx/" + name + " в ресурспак");
        }
        // Цвет задаётся компонентом окраски кожаной брони: он есть только у кожаных предметов.
        ItemStack item = new ItemStack(tinted ? Material.LEATHER_HORSE_ARMOR : Material.PAPER);
        NamespacedKey model = new NamespacedKey(NAMESPACE, "fx/" + name);
        item.editMeta(meta -> meta.setItemModel(model));
        return item;
    }

    private static void tint(ItemStack item, Color color) {
        item.editMeta(LeatherArmorMeta.class, meta -> meta.setColor(color));
    }

    /** Предмет для нового спрайта: случайный вариант, для радужных — со случайным оттенком. */
    public ItemStack pick() {
        ThreadLocalRandom random = ThreadLocalRandom.current();
        return pick(variants.size() == 1 ? 0 : random.nextInt(variants.size()), random.nextDouble());
    }

    /**
     * @param index номер варианта из списка sprite (берётся по кругу)
     * @param hue   оттенок от 0 до 1 для радужных спрайтов
     */
    public ItemStack pick(int index, double hue) {
        ItemStack item = variants.get(Math.floorMod(index, variants.size()));
        if (!rainbow) {
            return item;
        }
        ItemStack copy = item.clone();
        tint(copy, fromHue(hue));
        return copy;
    }

    public boolean rainbow() {
        return rainbow;
    }

    /** Кадры по порядку; пустой список — картинка не меняется. */
    public List<ItemStack> frames() {
        return frames;
    }

    public int frameTicks() {
        return frameTicks;
    }

    /** Светится ли спрайт в темноте. */
    public boolean glow() {
        return glow;
    }

    private static Color fromHue(double hue) {
        double h = (hue - Math.floor(hue)) * 6.0;
        int rising = (int) Math.round((h - Math.floor(h)) * 255);
        int falling = 255 - rising;
        return switch ((int) h) {
            case 0 -> Color.fromRGB(255, rising, 0);
            case 1 -> Color.fromRGB(falling, 255, 0);
            case 2 -> Color.fromRGB(0, 255, rising);
            case 3 -> Color.fromRGB(0, falling, 255);
            case 4 -> Color.fromRGB(rising, 0, 255);
            default -> Color.fromRGB(255, 0, falling);
        };
    }
}
