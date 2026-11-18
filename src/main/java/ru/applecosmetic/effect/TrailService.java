package ru.applecosmetic.effect;

import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.concurrent.ThreadLocalRandom;
import org.bukkit.Location;
import org.bukkit.World;
import org.bukkit.entity.AbstractArrow;
import org.bukkit.entity.Firework;
import org.bukkit.entity.Player;
import org.bukkit.entity.Projectile;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.entity.FireworkExplodeEvent;
import org.bukkit.event.entity.ProjectileHitEvent;
import org.bukkit.event.entity.ProjectileLaunchEvent;
import org.bukkit.scheduler.BukkitRunnable;
import org.bukkit.util.Vector;
import ru.applecosmetic.AppleCosmeticPlugin;
import ru.applecosmetic.Settings;
import ru.applecosmetic.cosmetic.Category;
import ru.applecosmetic.cosmetic.Cosmetic;

/** Рисует следы за снарядами и ракетами фейерверков и проигрывает эффект в конце полёта. */
public final class TrailService implements Listener {

    /** Больше спрайтов за тик один снаряд не оставляет: у быстрых стрел след просто реже. */
    private static final int MAX_PER_TICK = 4;
    private static final double TAU = Math.PI * 2;

    private final AppleCosmeticPlugin plugin;
    private final Map<Projectile, State> active = new HashMap<>();

    public TrailService(AppleCosmeticPlugin plugin) {
        this.plugin = plugin;
    }

    @EventHandler(priority = EventPriority.MONITOR, ignoreCancelled = true)
    public void onLaunch(ProjectileLaunchEvent event) {
        Projectile projectile = event.getEntity();
        if (!(projectile.getShooter() instanceof Player shooter)) {
            return;
        }
        Category category = category(projectile);
        if (category == null) {
            return;
        }
        Cosmetic cosmetic = plugin.cosmetics().selected(shooter, category);
        if (cosmetic != null && cosmetic.trail() != null) {
            active.put(projectile, new State(cosmetic, projectile.getLocation()));
        }
    }

    /** Категория косметики для снаряда или null, если за ним след не тянется. */
    private Category category(Projectile projectile) {
        Settings settings = plugin.settings();
        if (projectile instanceof Firework firework) {
            // Ракета, которой игрок разгоняется на элитрах, летит вместе с ним.
            boolean boost = firework.getAttachedTo() != null;
            return (boost ? settings.fireworkOnElytra() : settings.fireworkOnRockets()) ? Category.FIREWORK : null;
        }
        return settings.projectileTypes().contains(projectile.getType()) ? Category.PROJECTILE : null;
    }

    @EventHandler(priority = EventPriority.MONITOR, ignoreCancelled = true)
    public void onHit(ProjectileHitEvent event) {
        // Ракета при попадании взрывается: её эффект проигрывается по событию взрыва.
        if (!(event.getEntity() instanceof Firework)) {
            finish(event.getEntity());
        }
    }

    @EventHandler(priority = EventPriority.MONITOR, ignoreCancelled = true)
    public void onExplode(FireworkExplodeEvent event) {
        finish(event.getEntity());
    }

    private void finish(Projectile projectile) {
        State state = active.remove(projectile);
        if (state != null && state.cosmetic.effect() != null) {
            plugin.effects().play(state.cosmetic.effect(), projectile.getLocation(), null);
        }
    }

    /** Вызывается каждый тик. */
    public void tick() {
        if (active.isEmpty()) {
            return;
        }
        int maxTicks = plugin.settings().projectileMaxTicks();
        Iterator<Map.Entry<Projectile, State>> iterator = active.entrySet().iterator();
        while (iterator.hasNext()) {
            Map.Entry<Projectile, State> entry = iterator.next();
            Projectile projectile = entry.getKey();
            State state = entry.getValue();
            if (!projectile.isValid() || state.age > maxTicks
                    || projectile instanceof AbstractArrow arrow && arrow.isInBlock()) {
                iterator.remove();
                continue;
            }
            Location now = projectile.getLocation();
            if (now.getWorld() == state.last.getWorld()) {
                draw(state, now, null);
            }
            state.last = now;
            state.age++;
        }
    }

    public void clear() {
        active.clear();
    }

    /** Показывает след только одному игроку: спрайты пролетают перед ним слева направо. */
    public void preview(Player viewer, Cosmetic cosmetic) {
        Vector forward = forward(viewer);
        Vector right = new Vector(-forward.getZ(), 0, forward.getX());
        Location start = viewer.getEyeLocation().add(forward.clone().multiply(3.5))
                .subtract(right.clone().multiply(3));
        State state = new State(cosmetic, start);
        new BukkitRunnable() {
            private int tick;

            @Override
            public void run() {
                if (!viewer.isOnline()) {
                    cancel();
                    return;
                }
                if (tick++ >= 20) {
                    cancel();
                    if (cosmetic.effect() != null) {
                        plugin.effects().play(cosmetic.effect(), state.last, viewer);
                    }
                    return;
                }
                Location next = state.last.clone().add(right.clone().multiply(0.3));
                draw(state, next, viewer);
                state.last = next;
            }
        }.runTaskTimer(plugin, 0L, 1L);
    }

    /** Направление взгляда без наклона вверх или вниз. */
    public static Vector forward(Player player) {
        double yaw = Math.toRadians(player.getLocation().getYaw());
        return new Vector(-Math.sin(yaw), 0, Math.cos(yaw));
    }

    /** Ставит спрайты вдоль отрезка пути через равные промежутки, учитывая остаток с прошлого тика. */
    private void draw(State state, Location to, Player only) {
        World world = to.getWorld();
        TrailDefinition trail = state.cosmetic.trail();
        Location from = state.last;
        double dx = to.getX() - from.getX();
        double dy = to.getY() - from.getY();
        double dz = to.getZ() - from.getZ();
        double distance = Math.sqrt(dx * dx + dy * dy + dz * dz);
        double travelled = state.carry + distance;
        double spacing = trail.spacing();
        int count = (int) (travelled / spacing);
        if (count <= 0 || distance < 1.0E-6) {
            state.carry = travelled;
            return;
        }
        double first = spacing - state.carry;
        if (count > MAX_PER_TICK) {
            count = MAX_PER_TICK;
            spacing = distance / count;
            first = spacing;
            state.carry = 0;
        } else {
            state.carry = travelled - count * spacing;
        }

        Vector side = null;
        Vector up = null;
        if (trail.spiral() > 0) {
            Vector direction = new Vector(dx, dy, dz).multiply(1 / distance);
            Vector reference = Math.abs(direction.getY()) > 0.95 ? new Vector(1, 0, 0) : new Vector(0, 1, 0);
            side = direction.getCrossProduct(reference).normalize();
            up = direction.getCrossProduct(side).normalize();
        }

        ThreadLocalRandom random = ThreadLocalRandom.current();
        for (int index = 0; index < count; index++) {
            double t = Math.min(1.0, (first + index * spacing) / distance);
            double x = from.getX() + dx * t;
            double y = from.getY() + dy * t;
            double z = from.getZ() + dz * t;
            if (side != null) {
                state.angle += 0.9;
                double a = Math.cos(state.angle) * trail.spiral();
                double b = Math.sin(state.angle) * trail.spiral();
                x += side.getX() * a + up.getX() * b;
                y += side.getY() * a + up.getY() * b;
                z += side.getZ() * a + up.getZ() * b;
            }
            if (trail.spread() > 0) {
                x += random.nextGaussian() * trail.spread();
                y += random.nextGaussian() * trail.spread();
                z += random.nextGaussian() * trail.spread();
            }
            state.hue += 0.07;
            emit(trail, world, only, x, y, z, state.hue);
        }
    }

    /** Один спрайт следа: появляется сразу в полном размере и тает на месте. */
    private void emit(TrailDefinition trail, World world, Player only, double x, double y, double z, double hue) {
        ThreadLocalRandom random = ThreadLocalRandom.current();
        SpriteSpec sprite = trail.sprite();
        SpritePlan plan = new SpritePlan(world, only).at(x, y, z);
        // Радужный след переливается по порядку, а не случайно.
        plan.item = sprite.rainbow() ? sprite.pick(random.nextInt(1 << 16), hue) : sprite.pick();
        plan.frames = sprite.frames();
        plan.frameTicks = sprite.frameTicks();
        plan.glow = sprite.glow();
        plan.life = trail.duration();
        double size = trail.sizeMax() > trail.sizeMin()
                ? random.nextDouble(trail.sizeMin(), trail.sizeMax()) : trail.sizeMin();
        plan.size = (float) size;
        plan.endSize = (float) (size * trail.endSize());
        plan.out = Math.max(2, trail.duration() * 2 / 3);
        double rise = trail.rise();
        if (rise != 0) {
            plan.path = (t, out) -> {
                out[0] = x;
                out[1] = y + rise * t;
                out[2] = z;
            };
            plan.step = trail.duration();
        }
        if (trail.spin() != 0) {
            plan.roll = (float) random.nextDouble(TAU);
            plan.spin = (float) Math.toRadians(random.nextBoolean() ? trail.spin() : -trail.spin());
        }
        plugin.sprites().add(plan);
    }

    private static final class State {
        final Cosmetic cosmetic;
        Location last;
        int age;
        double angle;
        /** Путь, пройденный после последнего спрайта. */
        double carry;
        double hue;

        State(Cosmetic cosmetic, Location last) {
            this.cosmetic = cosmetic;
            this.last = last;
        }
    }
}
