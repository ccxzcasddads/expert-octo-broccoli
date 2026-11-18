package ru.applecosmetic;

import java.util.EnumSet;
import java.util.Locale;
import java.util.Set;
import java.util.logging.Logger;
import net.kyori.adventure.key.Key;
import org.bukkit.NamespacedKey;
import org.bukkit.configuration.file.FileConfiguration;
import org.bukkit.entity.EntityType;
import ru.applecosmetic.util.Text;

/** Значения из config.yml, которые читаются часто. */
public final class Settings {

    private boolean requirePermissions;
    private int skinSyncInterval;
    private boolean hatShowToSelf;
    private boolean hatHideWhenInvisible;
    private boolean hatOnlyWithoutHelmet;
    private int hatRefreshInterval;
    private boolean killOnPlayers;
    private boolean killOnMobs;
    private boolean critOnPlayers;
    private boolean critOnMobs;
    private final Set<EntityType> projectileTypes = EnumSet.noneOf(EntityType.class);
    private int projectileMaxTicks;
    private int critCooldown;
    private boolean fireworkOnRockets;
    private boolean fireworkOnElytra;
    private int maxSprites;
    private float spriteViewRange;
    private NamespacedKey menuTooltipStyle;

    public void load(FileConfiguration config, Logger logger) {
        requirePermissions = config.getBoolean("settings.require-permissions", true);
        skinSyncInterval = Math.max(1, config.getInt("skins.sync-interval-ticks", 20));
        hatShowToSelf = config.getBoolean("hats.show-to-self", true);
        hatHideWhenInvisible = config.getBoolean("hats.hide-when-invisible", true);
        hatOnlyWithoutHelmet = config.getBoolean("hats.only-without-helmet", false);
        hatRefreshInterval = Math.max(5, config.getInt("hats.refresh-interval-ticks", 40));
        killOnPlayers = config.getBoolean("effects.kill.players", true);
        killOnMobs = config.getBoolean("effects.kill.mobs", false);
        critOnPlayers = config.getBoolean("effects.crit.players", true);
        critOnMobs = config.getBoolean("effects.crit.mobs", true);
        projectileMaxTicks = Math.max(1, config.getInt("effects.projectile.max-ticks", 200));
        critCooldown = Math.max(0, config.getInt("effects.crit.cooldown-ticks", 4));
        fireworkOnRockets = config.getBoolean("effects.firework.rockets", true);
        fireworkOnElytra = config.getBoolean("effects.firework.elytra", true);
        maxSprites = Math.max(0, config.getInt("effects.sprites.max", 800));
        // Дальность прорисовки витрин задаётся в долях от 64 блоков.
        spriteViewRange = (float) Math.max(8, Math.min(128, config.getDouble("effects.sprites.view-distance", 48)))
                / 64f;

        menuTooltipStyle = key(config.getString("menu.tooltip-style", ""), "menu.tooltip-style", logger);
        NamespacedKey font = key(config.getString("menu.font", ""), "menu.font", logger);
        Text.uiFont(font == null ? null : Key.key(font.getNamespace(), font.getKey()));

        projectileTypes.clear();
        for (String name : config.getStringList("effects.projectile.types")) {
            try {
                projectileTypes.add(EntityType.valueOf(name.trim().toUpperCase(Locale.ROOT)));
            } catch (IllegalArgumentException e) {
                logger.warning("config.yml: неизвестный тип снаряда «" + name + "».");
            }
        }
    }

    /** Ключ вида пространство:путь; пустая строка — null. */
    private static NamespacedKey key(String raw, String path, Logger logger) {
        if (raw == null || raw.isBlank()) {
            return null;
        }
        NamespacedKey key = NamespacedKey.fromString(raw.trim().toLowerCase(Locale.ROOT));
        if (key == null) {
            logger.warning("config.yml: неверное значение «" + raw + "» в " + path
                    + ", нужен формат пространство:путь.");
        }
        return key;
    }

    public boolean requirePermissions() {
        return requirePermissions;
    }

    public int skinSyncInterval() {
        return skinSyncInterval;
    }

    public boolean hatShowToSelf() {
        return hatShowToSelf;
    }

    public boolean hatHideWhenInvisible() {
        return hatHideWhenInvisible;
    }

    public boolean hatOnlyWithoutHelmet() {
        return hatOnlyWithoutHelmet;
    }

    public int hatRefreshInterval() {
        return hatRefreshInterval;
    }

    public boolean killOnPlayers() {
        return killOnPlayers;
    }

    public boolean killOnMobs() {
        return killOnMobs;
    }

    public boolean critOnPlayers() {
        return critOnPlayers;
    }

    public boolean critOnMobs() {
        return critOnMobs;
    }

    public Set<EntityType> projectileTypes() {
        return projectileTypes;
    }

    public int projectileMaxTicks() {
        return projectileMaxTicks;
    }

    /** Пауза между эффектами крита одного игрока, в тиках. */
    public int critCooldown() {
        return critCooldown;
    }

    /** След за ракетами, запущенными с земли или из арбалета. */
    public boolean fireworkOnRockets() {
        return fireworkOnRockets;
    }

    /** След за игроком, который разгоняется ракетой на элитрах. */
    public boolean fireworkOnElytra() {
        return fireworkOnElytra;
    }

    /** Сколько спрайтов эффектов может одновременно быть на сервере. */
    public int maxSprites() {
        return maxSprites;
    }

    public float spriteViewRange() {
        return spriteViewRange;
    }

    /** Оформление подсказок у предметов меню или null. */
    public NamespacedKey menuTooltipStyle() {
        return menuTooltipStyle;
    }
}
