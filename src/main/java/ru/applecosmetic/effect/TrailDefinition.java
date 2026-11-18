package ru.applecosmetic.effect;

import java.util.function.Consumer;
import ru.applecosmetic.util.Params;

/**
 * След за снарядом или ракетой фейерверка.
 *
 * @param duration сколько тиков живёт каждый спрайт следа
 * @param spacing  расстояние между спрайтами вдоль траектории, в блоках
 * @param spread   случайный разброс спрайтов вокруг траектории
 * @param spiral   радиус спирали вокруг траектории; 0 — прямой след
 * @param rise     на сколько блоков спрайт поднимается (или опускается) за свою жизнь
 * @param spin     вращение, градусов за тик
 * @param endSize  размер в конце жизни как доля от начального
 */
public record TrailDefinition(
        SpriteSpec sprite,
        double sizeMin,
        double sizeMax,
        int duration,
        double spacing,
        double spread,
        double spiral,
        double rise,
        double spin,
        double endSize) {

    public static TrailDefinition parse(Params params, SpriteSpec.Source source, Consumer<String> warn) {
        if (params.has("particle")) {
            warn.accept("след из частиц (particle) больше не поддерживается: укажите спрайт (sprite)");
            return null;
        }
        SpriteSpec sprite = SpriteSpec.parse(params, source, warn);
        if (sprite == null) {
            return null;
        }
        double[] size = EffectLayer.range(params, "size", 0.4);
        return new TrailDefinition(
                sprite,
                size[0],
                size[1],
                Math.max(2, Math.min(60, params.integer("duration", 10))),
                Math.max(0.25, Math.min(8, params.decimal("spacing", 0.8))),
                Math.max(0, Math.min(2, params.decimal("spread", 0.0))),
                Math.max(0, Math.min(2, params.decimal("spiral", 0.0))),
                Math.max(-4, Math.min(4, params.decimal("rise", 0.0))),
                params.decimal("spin", 0.0),
                Math.max(0, Math.min(4, params.decimal("end-size", 0.0))));
    }
}
