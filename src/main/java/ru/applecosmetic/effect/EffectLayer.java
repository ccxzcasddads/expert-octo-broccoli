package ru.applecosmetic.effect;

import java.util.Arrays;
import java.util.Locale;
import java.util.function.Consumer;
import ru.applecosmetic.util.Params;

/**
 * Один слой эффекта: движение, спрайт и их параметры.
 *
 * @param interval пауза между появлением соседних спрайтов, в тиках
 * @param endSize  размер в конце жизни как доля от начального; 0 — спрайт сжимается в точку
 * @param spin     вращение, градусов за тик
 * @param turns    число оборотов вокруг центра для HELIX, VORTEX и ORBIT
 * @param strands  число нитей спирали
 * @param fall     на сколько блоков спрайты опускаются за время жизни (BURST, SPHERE)
 * @param angle    начальный угол в градусах; NaN — по умолчанию для движения
 */
public record EffectLayer(
        Animation animation,
        SpriteSpec sprite,
        int amount,
        double radius,
        double height,
        double yOffset,
        int duration,
        int delay,
        int interval,
        double sizeMin,
        double sizeMax,
        double endSize,
        double spin,
        double turns,
        int strands,
        double fall,
        double angle) {

    public static EffectLayer parse(Params params, SpriteSpec.Source source, Consumer<String> warn) {
        String name = params.string("animation", "BURST");
        Animation animation;
        try {
            animation = Animation.valueOf(name.trim().toUpperCase(Locale.ROOT));
        } catch (IllegalArgumentException e) {
            warn.accept("неизвестная анимация «" + name + "». Доступные: " + Arrays.toString(Animation.values()));
            return null;
        }
        if (params.has("particle")) {
            warn.accept("слой с частицей (particle) больше не поддерживается: укажите спрайт (sprite)");
            return null;
        }
        SpriteSpec sprite = SpriteSpec.parse(params, source, warn);
        if (sprite == null) {
            return null;
        }
        double[] size = range(params, "size", animation.size);
        return new EffectLayer(
                animation,
                sprite,
                clamp(params.integer("amount", animation.amount), 1, 80),
                Math.max(0, params.decimal("radius", animation.radius)),
                params.decimal("height", animation.height),
                params.decimal("y-offset", animation.yOffset),
                clamp(params.integer("duration", animation.duration), 2, 200),
                clamp(params.integer("delay", 0), 0, 200),
                clamp(params.integer("interval", animation.interval), 0, 40),
                size[0],
                size[1],
                Math.max(0, Math.min(4, params.decimal("end-size", 0.0))),
                params.decimal("spin", 0.0),
                params.decimal("turns", 2.0),
                clamp(params.integer("strands", 2), 1, 8),
                params.decimal("fall", 0.0),
                params.decimal("angle", Double.NaN));
    }

    /** Начальный угол в градусах или значение по умолчанию. */
    double angle(double fallback) {
        return Double.isNaN(angle) ? fallback : angle;
    }

    /** Размер: число или диапазон «от-до», тогда у каждого спрайта он свой. */
    static double[] range(Params params, String key, double fallback) {
        String raw = params.string(key, null);
        double min = fallback;
        double max = fallback;
        if (raw != null) {
            String[] parts = raw.trim().split("\\s*-\\s*");
            try {
                min = Double.parseDouble(parts[0]);
                max = parts.length > 1 ? Double.parseDouble(parts[1]) : min;
            } catch (NumberFormatException e) {
                min = fallback;
                max = fallback;
            }
        }
        min = Math.max(0.05, Math.min(16, min));
        max = Math.max(min, Math.min(16, max));
        return new double[] {min, max};
    }

    private static int clamp(int value, int min, int max) {
        return Math.max(min, Math.min(max, value));
    }
}
