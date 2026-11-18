package ru.applecosmetic.effect;

import java.io.File;
import java.io.IOException;
import java.util.Enumeration;
import java.util.HashSet;
import java.util.Set;
import java.util.jar.JarEntry;
import java.util.jar.JarFile;
import java.util.logging.Logger;
import ru.applecosmetic.item.ItemResolver;

/** Встроенные спрайты эффектов: по этому списку проверяются названия в конфигах. */
public final class SpriteCatalog implements SpriteSpec.Source {

    private static final String ASSETS = "contents/applecosmetic_raw/resourcepack/assets/" + SpriteSpec.NAMESPACE
            + "/items/fx/";
    private static final String BUNDLED = "pack/itemsadder/" + ASSETS;

    private final ItemResolver items;
    private final File itemsAdder;
    private final Set<String> names = new HashSet<>();

    /**
     * @param jar     файл плагина, в котором лежит набор
     * @param plugins папка plugins: свои спрайты можно добавить в набор ItemsAdder
     */
    public SpriteCatalog(File jar, File plugins, ItemResolver items, Logger logger) {
        this.items = items;
        this.itemsAdder = new File(plugins, "ItemsAdder/" + ASSETS);
        try (JarFile archive = new JarFile(jar)) {
            for (Enumeration<JarEntry> entries = archive.entries(); entries.hasMoreElements(); ) {
                String name = entries.nextElement().getName();
                if (name.startsWith(BUNDLED) && name.endsWith(".json")) {
                    names.add(name.substring(BUNDLED.length(), name.length() - ".json".length()));
                }
            }
        } catch (IOException e) {
            logger.warning("Не удалось прочитать список спрайтов: " + e.getMessage());
        }
    }

    @Override
    public ItemResolver items() {
        return items;
    }

    @Override
    public boolean hasSprite(String name) {
        // Если список прочитать не удалось, названия не проверяются.
        return names.isEmpty() || names.contains(name) || new File(itemsAdder, name + ".json").isFile();
    }

    public int size() {
        return names.size();
    }
}
