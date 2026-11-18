package ru.applecosmetic.cosmetic;

import java.util.List;
import ru.applecosmetic.effect.EffectDefinition;
import ru.applecosmetic.effect.TrailDefinition;

/**
 * Одна позиция косметики.
 *
 * @param name   название в исходном виде (MiniMessage)
 * @param icons  предметы для меню: используется первый доступный
 * @param items  источники модели для обликов и шляп: используется первый доступный
 * @param effect эффект из спрайтов: для убийства, крита и смерти, а у следов — в конце полёта; иначе null
 * @param trail  след снаряда или ракеты, иначе null
 */
public record Cosmetic(
        Category category,
        String id,
        String name,
        List<String> lore,
        List<String> icons,
        List<String> items,
        String permission,
        EffectDefinition effect,
        TrailDefinition trail) {
}
