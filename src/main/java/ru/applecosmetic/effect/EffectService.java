package ru.applecosmetic.effect;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;
import org.bukkit.Bukkit;
import org.bukkit.Location;
import org.bukkit.World;
import org.bukkit.entity.ArmorStand;
import org.bukkit.entity.LivingEntity;
import org.bukkit.entity.Mob;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.entity.EntityDamageByEntityEvent;
import org.bukkit.event.entity.EntityDeathEvent;
import ru.applecosmetic.AppleCosmeticPlugin;
import ru.applecosmetic.Settings;
import ru.applecosmetic.cosmetic.Category;
import ru.applecosmetic.cosmetic.Cosmetic;

/** Проигрывает эффекты убийства, смерти и критического удара. */
public final class EffectService implements Listener {

    private final AppleCosmeticPlugin plugin;
    private final Map<UUID, Integer> lastCrit = new HashMap<>();

    public EffectService(AppleCosmeticPlugin plugin) {
        this.plugin = plugin;
    }

    /**
     * @param origin точка у ног цели
     * @param only   единственный зритель (предпросмотр); null — видят все поблизости
     */
    public void play(EffectDefinition effect, Location origin, Player only) {
        World world = origin.getWorld();
        if (world == null) {
            return;
        }
        for (SoundSpec sound : effect.sounds()) {
            sound.play(origin, only);
        }
        Animation.Scene scene = new Animation.Scene(plugin.sprites(), world, only,
                origin.getX(), origin.getY(), origin.getZ());
        for (EffectLayer layer : effect.layers()) {
            layer.animation().start(layer, scene);
        }
    }

    public void forget(UUID id) {
        lastCrit.remove(id);
    }

    private void playSelected(Player owner, Category category, Location at) {
        Cosmetic cosmetic = plugin.cosmetics().selected(owner, category);
        if (cosmetic != null && cosmetic.effect() != null) {
            play(cosmetic.effect(), at, null);
        }
    }

    @EventHandler(priority = EventPriority.MONITOR, ignoreCancelled = true)
    public void onDeath(EntityDeathEvent event) {
        LivingEntity victim = event.getEntity();
        Location at = victim.getLocation();
        if (victim instanceof Player dead) {
            playSelected(dead, Category.DEATH, at);
        }
        Player killer = victim.getKiller();
        if (killer == null || killer.equals(victim)) {
            return;
        }
        Settings settings = plugin.settings();
        boolean allowed = victim instanceof Player ? settings.killOnPlayers()
                : victim instanceof Mob && settings.killOnMobs();
        if (allowed) {
            playSelected(killer, Category.KILL, at);
        }
    }

    @EventHandler(priority = EventPriority.MONITOR, ignoreCancelled = true)
    public void onCriticalHit(EntityDamageByEntityEvent event) {
        if (!event.isCritical() || !(event.getDamager() instanceof Player attacker)
                || !(event.getEntity() instanceof LivingEntity victim) || victim instanceof ArmorStand) {
            return;
        }
        Settings settings = plugin.settings();
        if (!(victim instanceof Player ? settings.critOnPlayers() : settings.critOnMobs())) {
            return;
        }
        // Без паузы частые удары (например, на серверах со старым боем) засыпали бы цель спрайтами.
        int now = Bukkit.getCurrentTick();
        Integer last = lastCrit.get(attacker.getUniqueId());
        if (last != null && now - last < settings.critCooldown()) {
            return;
        }
        lastCrit.put(attacker.getUniqueId(), now);
        playSelected(attacker, Category.CRIT, victim.getLocation());
    }
}
