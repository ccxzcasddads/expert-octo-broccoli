package ru.applecosmetic.effect;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.TreeSet;
import org.bukkit.Location;
import org.bukkit.entity.Display;
import org.bukkit.entity.ItemDisplay;
import org.bukkit.util.Transformation;
import org.joml.Quaternionf;
import org.joml.Vector3f;
import ru.applecosmetic.AppleCosmeticPlugin;

/**
 * Показывает спрайты эффектов. Каждый спрайт — сущность-витрина с предметом: сервер задаёт ей
 * несколько опорных состояний, а плавное движение между ними клиент дорисовывает сам.
 * Сущности не сохраняются в мир и убираются сами, когда спрайт отыграл.
 */
public final class SpriteEngine {

    /** За один отрезок спрайт поворачивается меньше чем на пол-оборота, иначе клиент выберет короткий путь. */
    private static final float MAX_TURN = 2.0f;
    private static final int MAX_TELEPORT_TICKS = 59;
    private static final float HALF_PI = (float) (Math.PI / 2);

    private final AppleCosmeticPlugin plugin;
    private final List<Live> live = new ArrayList<>();
    private final List<SpritePlan> waiting = new ArrayList<>();
    private boolean spawnFailureReported;

    public SpriteEngine(AppleCosmeticPlugin plugin) {
        this.plugin = plugin;
    }

    /** Ставит спрайт в очередь; при превышении лимита новые спрайты пропускаются. */
    void add(SpritePlan plan) {
        if (plan.item == null || live.size() + waiting.size() >= plugin.settings().maxSprites()) {
            return;
        }
        plan.life = Math.max(2, plan.life);
        if (plan.delay > 0) {
            waiting.add(plan);
        } else {
            spawn(plan);
        }
    }

    /** Вызывается каждый тик. */
    public void tick() {
        if (!waiting.isEmpty()) {
            List<SpritePlan> due = new ArrayList<>();
            for (Iterator<SpritePlan> iterator = waiting.iterator(); iterator.hasNext(); ) {
                SpritePlan plan = iterator.next();
                if (--plan.delay <= 0) {
                    iterator.remove();
                    due.add(plan);
                }
            }
            due.forEach(this::spawn);
        }
        for (Iterator<Live> iterator = live.iterator(); iterator.hasNext(); ) {
            Live sprite = iterator.next();
            if (!sprite.entity.isValid()) {
                iterator.remove();
            } else if (++sprite.age >= sprite.plan.life) {
                sprite.entity.remove();
                iterator.remove();
            } else {
                sprite.update();
            }
        }
    }

    /** Сколько спрайтов сейчас показывается или ждёт своей очереди. */
    public int active() {
        return live.size() + waiting.size();
    }

    /** Убирает все спрайты: при выключении плагина. */
    public void clear() {
        for (Live sprite : live) {
            sprite.entity.remove();
        }
        live.clear();
        waiting.clear();
    }

    private void spawn(SpritePlan plan) {
        if (plan.only != null && !plan.only.isOnline()) {
            return;
        }
        Live sprite = new Live(plan);
        if (plan.path != null) {
            plan.path.at(0, sprite.point);
        } else {
            sprite.point[0] = plan.x;
            sprite.point[1] = plan.y;
            sprite.point[2] = plan.z;
        }
        Location at = new Location(plan.world, sprite.point[0], sprite.point[1], sprite.point[2]);
        float viewRange = plugin.settings().spriteViewRange();
        ItemDisplay entity;
        try {
            entity = plan.world.spawn(at, ItemDisplay.class, display -> {
                display.setItemStack(plan.frames.isEmpty() ? plan.item : plan.frames.get(0));
                display.setBillboard(switch (plan.facing) {
                    case CAMERA -> Display.Billboard.CENTER;
                    case UPRIGHT -> Display.Billboard.VERTICAL;
                    case GROUND -> Display.Billboard.FIXED;
                });
                if (plan.glow) {
                    display.setBrightness(new Display.Brightness(15, 15));
                }
                display.setTeleportDuration(sprite.step);
                display.setInterpolationDuration(0);
                display.setTransformation(sprite.transformation(0));
                display.setViewRange(viewRange);
                display.setShadowRadius(0f);
                display.setPersistent(false);
                display.setInvulnerable(true);
                if (plan.only != null) {
                    display.setVisibleByDefault(false);
                }
            });
        } catch (RuntimeException e) {
            if (!spawnFailureReported) {
                spawnFailureReported = true;
                plugin.getLogger().warning("Не удалось показать спрайт эффекта: " + e);
            }
            return;
        }
        // Другой плагин мог отменить появление сущности.
        if (!entity.isValid()) {
            return;
        }
        if (plan.only != null) {
            plan.only.showEntity(plugin, entity);
        }
        sprite.entity = entity;
        sprite.location = at;
        live.add(sprite);
    }

    /** Спрайт, который сейчас показывается. */
    private static final class Live {
        final SpritePlan plan;
        final int step;
        final int[] scaleTicks;
        final float[] scaleValues;
        /** Тики опорных состояний по возрастанию; последний — конец жизни. */
        final int[] keys;
        final double[] point = new double[3];
        ItemDisplay entity;
        Location location;
        int age;
        int key;
        int frame;

        Live(SpritePlan plan) {
            this.plan = plan;
            this.step = plan.path == null ? 0 : Math.max(1, Math.min(MAX_TELEPORT_TICKS, plan.step));

            List<int[]> ticks = new ArrayList<>();
            List<Float> values = new ArrayList<>();
            int life = plan.life;
            int in = Math.min(plan.in <= 0 ? 0 : Math.max(2, plan.in), life);
            ticks.add(new int[] {0});
            values.add(in > 0 ? 0f : plan.size);
            int last = 0;
            if (in > 0) {
                boolean overshoot = plan.overshoot && in + 2 < life;
                ticks.add(new int[] {in});
                values.add(overshoot ? plan.size * 1.2f : plan.size);
                last = in;
                if (overshoot) {
                    last = in + 2;
                    ticks.add(new int[] {last});
                    values.add(plan.size);
                }
            }
            if (plan.out > 0) {
                int hold = Math.max(last, life - plan.out);
                if (hold > last) {
                    ticks.add(new int[] {hold});
                    values.add(plan.size);
                }
                if (life > hold) {
                    ticks.add(new int[] {life});
                    values.add(plan.endSize);
                }
            } else if (life > last) {
                ticks.add(new int[] {life});
                values.add(plan.size);
            }
            scaleTicks = new int[ticks.size()];
            scaleValues = new float[ticks.size()];
            for (int i = 0; i < scaleTicks.length; i++) {
                scaleTicks[i] = ticks.get(i)[0];
                scaleValues[i] = values.get(i);
            }

            TreeSet<Integer> stops = new TreeSet<>();
            for (int tick : scaleTicks) {
                if (tick >= 2) {
                    stops.add(tick);
                }
            }
            if (plan.spin != 0f) {
                int segment = Math.max(2, (int) (MAX_TURN / Math.abs(plan.spin)));
                for (int tick = segment; tick < life; tick += segment) {
                    stops.add(tick);
                }
            }
            stops.add(life);
            keys = stops.stream().mapToInt(Integer::intValue).toArray();
        }

        float scaleAt(int tick) {
            for (int i = 1; i < scaleTicks.length; i++) {
                if (tick <= scaleTicks[i]) {
                    int from = scaleTicks[i - 1];
                    float share = (float) (tick - from) / (scaleTicks[i] - from);
                    return scaleValues[i - 1] + (scaleValues[i] - scaleValues[i - 1]) * share;
                }
            }
            return scaleValues[scaleValues.length - 1];
        }

        Transformation transformation(int tick) {
            float scale = scaleAt(tick);
            float angle = plan.roll + plan.spin * tick;
            Quaternionf rotation = plan.facing == SpritePlan.Facing.GROUND
                    ? new Quaternionf().rotationY(angle).rotateX(-HALF_PI)
                    : new Quaternionf().rotationZ(angle);
            float height = plan.tall > 0f ? plan.tall : scale;
            return new Transformation(new Vector3f(), rotation, new Vector3f(scale, height, scale),
                    new Quaternionf());
        }

        void update() {
            // Первое изменение отправляется через тик после появления: иначе клиент применит его мгновенно.
            if (age == 1) {
                aim(keys[0], keys[0] - 1);
            } else if (age == keys[key] && key + 1 < keys.length) {
                key++;
                aim(keys[key], keys[key] - age);
            }
            if (step > 0 && (age - 1) % step == 0) {
                int target = Math.min(plan.life, age - 1 + step);
                plan.path.at((double) target / plan.life, point);
                location.set(point[0], point[1], point[2]);
                entity.teleport(location);
            }
            if (!plan.frames.isEmpty() && age % plan.frameTicks == 0) {
                int next = Math.min(plan.frames.size() - 1, age / plan.frameTicks);
                if (next != frame) {
                    frame = next;
                    entity.setItemStack(plan.frames.get(next));
                }
            }
        }

        private void aim(int tick, int duration) {
            entity.setInterpolationDelay(0);
            entity.setInterpolationDuration(Math.max(1, duration));
            entity.setTransformation(transformation(tick));
        }
    }
}
