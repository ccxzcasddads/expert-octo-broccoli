package ru.applecosmetic.effect;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.function.Consumer;
import org.bukkit.configuration.ConfigurationSection;
import ru.applecosmetic.util.Params;

/** Разовый эффект: слои спрайтов и звуки. */
public record EffectDefinition(List<EffectLayer> layers, List<SoundSpec> sounds) {

    public static EffectDefinition parse(ConfigurationSection section, SpriteSpec.Source source,
                                         Consumer<String> warn) {
        List<EffectLayer> layers = new ArrayList<>();
        for (Map<?, ?> entry : section.getMapList("layers")) {
            EffectLayer layer = EffectLayer.parse(Params.of(entry), source, warn);
            if (layer != null) {
                layers.add(layer);
            }
        }
        List<SoundSpec> sounds = new ArrayList<>();
        List<?> rawSounds = section.getList("sounds");
        if (rawSounds != null) {
            for (Object entry : rawSounds) {
                SoundSpec sound = SoundSpec.parse(entry);
                if (sound == null) {
                    warn.accept("звук без названия пропущен");
                } else {
                    if (!sound.known()) {
                        warn.accept("неизвестный звук «" + sound.name() + "»");
                    }
                    sounds.add(sound);
                }
            }
        }
        for (String removed : List.of("lightning", "firework")) {
            if (section.isSet(removed)) {
                warn.accept("поле «" + removed + "» больше не используется: молния и салют собираются"
                        + " из спрайтов в layers");
            }
        }
        return new EffectDefinition(List.copyOf(layers), List.copyOf(sounds));
    }

    public boolean isEmpty() {
        return layers.isEmpty() && sounds.isEmpty();
    }
}
