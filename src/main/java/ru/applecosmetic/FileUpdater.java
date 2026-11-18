package ru.applecosmetic;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import org.bukkit.configuration.file.YamlConfiguration;
import org.bukkit.plugin.java.JavaPlugin;

/**
 * Обновляет файлы настроек, формат которых изменился. В каждом таком файле есть поле file-version:
 * если в плагине оно больше, чем в файле на диске, старый файл сохраняется рядом как *.yml.vN.bak,
 * а на его место кладётся новый.
 */
public final class FileUpdater {

    private static final String KEY = "file-version";

    private FileUpdater() {
    }

    /** @param name путь к файлу внутри папки плагина, например effects/kill.yml */
    public static void update(JavaPlugin plugin, String name) {
        File file = new File(plugin.getDataFolder(), name);
        if (!file.isFile()) {
            return;
        }
        int bundled;
        try (InputStream in = plugin.getResource(name)) {
            if (in == null) {
                return;
            }
            bundled = YamlConfiguration.loadConfiguration(new InputStreamReader(in, StandardCharsets.UTF_8))
                    .getInt(KEY, 1);
        } catch (IOException e) {
            return;
        }
        YamlConfiguration current = new YamlConfiguration();
        try {
            current.load(file);
        } catch (Exception e) {
            // Файл с ошибкой не трогаем: о ней сообщит тот, кто будет его читать.
            return;
        }
        int version = current.getInt(KEY, 1);
        if (version >= bundled) {
            return;
        }
        File backup = new File(file.getParentFile(), file.getName() + ".v" + version + ".bak");
        for (int copy = 2; backup.exists(); copy++) {
            backup = new File(file.getParentFile(), file.getName() + ".v" + version + "-" + copy + ".bak");
        }
        try {
            Files.move(file.toPath(), backup.toPath());
        } catch (IOException e) {
            plugin.getLogger().warning("Не удалось обновить " + name + ": " + e.getMessage());
            return;
        }
        plugin.saveResource(name, false);
        plugin.getLogger().info("Файл " + name + " обновлён до версии " + bundled + ". Прежний сохранён как "
                + backup.getName() + ".");
    }
}
