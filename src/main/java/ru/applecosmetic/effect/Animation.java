package ru.applecosmetic.effect;

import java.util.concurrent.ThreadLocalRandom;
import org.bukkit.World;
import org.bukkit.entity.Player;

/**
 * Движения спрайтов. В скобках — значения слоя по умолчанию:
 * количество, радиус, высота, подъём над землёй, длительность, размер и пауза между спрайтами.
 */
public enum Animation {

    /** Спрайт «выскакивает» на месте и исчезает. */
    POP(1, 0.0, 0.0, 1.0, 20, 1.0, 0) {
        @Override
        void start(EffectLayer layer, Scene scene) {
            for (int i = 0; i < layer.amount(); i++) {
                SpritePlan plan = plan(layer, scene, i);
                scatter(plan, layer, scene);
                popIn(plan);
                plan.out = Math.max(2, layer.duration() / 4);
                scene.engine.add(plan);
            }
        }
    },

    /** Спрайт появляется и плавно поднимается на высоту height. */
    RISE(1, 0.0, 1.5, 0.5, 30, 1.0, 4) {
        @Override
        void start(EffectLayer layer, Scene scene) {
            for (int i = 0; i < layer.amount(); i++) {
                SpritePlan plan = plan(layer, scene, i);
                scatter(plan, layer, scene);
                double x = plan.x;
                double y = plan.y;
                double z = plan.z;
                double height = layer.height();
                plan.path = (t, out) -> set(out, x, y + height * t, z);
                plan.step = layer.duration();
                popIn(plan);
                plan.out = Math.max(3, layer.duration() / 3);
                scene.engine.add(plan);
            }
        }
    },

    /** Спрайты разлетаются из одной точки во все стороны; fall — насколько они при этом падают. */
    BURST(10, 1.2, 0.0, 1.0, 14, 0.4, 0) {
        @Override
        void start(EffectLayer layer, Scene scene) {
            ThreadLocalRandom random = ThreadLocalRandom.current();
            double y = scene.y + layer.yOffset();
            for (int i = 0; i < layer.amount(); i++) {
                double vertical = random.nextDouble(-1.0, 1.0);
                double flat = Math.sqrt(1 - vertical * vertical);
                double angle = random.nextDouble(TAU);
                double reach = layer.radius() * random.nextDouble(0.55, 1.0);
                double dx = Math.cos(angle) * flat * reach;
                double dy = vertical * reach;
                double dz = Math.sin(angle) * flat * reach;
                double fall = layer.fall();
                SpritePlan plan = plan(layer, scene, i);
                plan.path = (t, out) -> {
                    double eased = 1 - (1 - t) * (1 - t);
                    set(out, scene.x + dx * eased, y + dy * eased - fall * t * t, scene.z + dz * eased);
                };
                plan.out = Math.max(2, layer.duration() * 3 / 5);
                tumble(plan);
                scene.engine.add(plan);
            }
        }
    },

    /** Кольцо спрайтов, расходящееся по земле. */
    RING(12, 2.0, 0.0, 0.3, 14, 0.4, 0) {
        @Override
        void start(EffectLayer layer, Scene scene) {
            double phase = ThreadLocalRandom.current().nextDouble(TAU);
            double y = scene.y + layer.yOffset();
            for (int i = 0; i < layer.amount(); i++) {
                double angle = phase + TAU * i / layer.amount();
                double dx = Math.cos(angle) * layer.radius();
                double dz = Math.sin(angle) * layer.radius();
                SpritePlan plan = plan(layer, scene, i);
                plan.path = (t, out) -> {
                    double eased = 1 - (1 - t) * (1 - t);
                    set(out, scene.x + dx * eased, y, scene.z + dz * eased);
                };
                plan.in = 2;
                plan.out = Math.max(2, layer.duration() / 2);
                tumble(plan);
                scene.engine.add(plan);
            }
        }
    },

    /** Спрайты равномерно разлетаются по сфере. */
    SPHERE(24, 1.6, 0.0, 1.0, 16, 0.4, 0) {
        @Override
        void start(EffectLayer layer, Scene scene) {
            double y = scene.y + layer.yOffset();
            int points = layer.amount();
            for (int i = 0; i < points; i++) {
                double vertical = 1 - 2 * (i + 0.5) / points;
                double flat = Math.sqrt(1 - vertical * vertical);
                double angle = i * GOLDEN_ANGLE;
                double dx = Math.cos(angle) * flat * layer.radius();
                double dy = vertical * layer.radius();
                double dz = Math.sin(angle) * flat * layer.radius();
                double fall = layer.fall();
                SpritePlan plan = plan(layer, scene, i);
                plan.path = (t, out) -> {
                    double eased = 1 - (1 - t) * (1 - t);
                    set(out, scene.x + dx * eased, y + dy * eased - fall * t * t, scene.z + dz * eased);
                };
                plan.in = 2;
                plan.out = Math.max(2, layer.duration() / 2);
                tumble(plan);
                scene.engine.add(plan);
            }
        }
    },

    /** Спрайты слетаются со сферы в одну точку. */
    IMPLODE(16, 2.0, 0.0, 1.0, 14, 0.4, 0) {
        @Override
        void start(EffectLayer layer, Scene scene) {
            double y = scene.y + layer.yOffset();
            int points = layer.amount();
            for (int i = 0; i < points; i++) {
                double vertical = 1 - 2 * (i + 0.5) / points;
                double flat = Math.sqrt(1 - vertical * vertical);
                double angle = i * GOLDEN_ANGLE;
                double dx = Math.cos(angle) * flat * layer.radius();
                double dy = vertical * layer.radius();
                double dz = Math.sin(angle) * flat * layer.radius();
                SpritePlan plan = plan(layer, scene, i);
                plan.path = (t, out) -> {
                    double left = 1 - t * t;
                    set(out, scene.x + dx * left, y + dy * left, scene.z + dz * left);
                };
                plan.in = 3;
                plan.out = Math.max(2, layer.duration() / 3);
                tumble(plan);
                scene.engine.add(plan);
            }
        }
    },

    /** Фонтан: спрайты вылетают вверх на высоту height и падают в радиусе radius. */
    FOUNTAIN(10, 1.2, 1.8, 0.3, 30, 0.4, 1) {
        @Override
        void start(EffectLayer layer, Scene scene) {
            ThreadLocalRandom random = ThreadLocalRandom.current();
            double ground = scene.y + 0.15;
            double y = scene.y + layer.yOffset();
            for (int i = 0; i < layer.amount(); i++) {
                double lift = Math.sqrt(2 * GRAVITY * Math.max(0.1, layer.height())) * random.nextDouble(0.8, 1.1);
                double flight = 2 * lift / GRAVITY;
                double angle = random.nextDouble(TAU);
                double reach = layer.radius() * random.nextDouble(0.25, 1.0);
                double vx = Math.cos(angle) * reach / flight;
                double vz = Math.sin(angle) * reach / flight;
                int life = layer.duration();
                SpritePlan plan = plan(layer, scene, i);
                plan.path = (t, out) -> {
                    double ticks = t * life;
                    double moved = Math.min(ticks, flight * 1.15);
                    set(out, scene.x + vx * moved, Math.max(ground, y + lift * ticks - GRAVITY * ticks * ticks / 2),
                            scene.z + vz * moved);
                };
                plan.in = 2;
                plan.out = Math.max(3, life / 4);
                tumble(plan);
                scene.engine.add(plan);
            }
        }
    },

    /** Дождь: спрайты падают с высоты height в радиусе radius. */
    RAIN(12, 1.4, 3.0, 0.1, 24, 0.4, 2) {
        @Override
        void start(EffectLayer layer, Scene scene) {
            ThreadLocalRandom random = ThreadLocalRandom.current();
            double y = scene.y + layer.yOffset();
            for (int i = 0; i < layer.amount(); i++) {
                double angle = random.nextDouble(TAU);
                double distance = Math.sqrt(random.nextDouble()) * layer.radius();
                double x = scene.x + Math.cos(angle) * distance;
                double z = scene.z + Math.sin(angle) * distance;
                double height = layer.height();
                // Лёгкий снос в сторону, чтобы падение не выглядело отвесным.
                double driftX = random.nextDouble(-0.3, 0.3);
                double driftZ = random.nextDouble(-0.3, 0.3);
                SpritePlan plan = plan(layer, scene, i);
                plan.path = (t, out) -> set(out, x + driftX * t, y + height * (1 - t), z + driftZ * t);
                plan.step = layer.duration();
                plan.in = 2;
                plan.out = 3;
                tumble(plan);
                scene.engine.add(plan);
            }
        }
    },

    /** Спираль вверх: strands нитей, в каждой amount спрайтов летят друг за другом. */
    HELIX(4, 0.8, 2.4, 0.1, 28, 0.4, 2) {
        @Override
        void start(EffectLayer layer, Scene scene) {
            swirl(layer, scene, false);
        }
    },

    /** Вихрь: спираль, расширяющаяся кверху. */
    VORTEX(6, 1.4, 3.0, 0.1, 30, 0.4, 2) {
        @Override
        void start(EffectLayer layer, Scene scene) {
            swirl(layer, scene, true);
        }
    },

    /** Спрайты кружат вокруг точки; height — насколько они при этом поднимаются. */
    ORBIT(4, 1.0, 0.0, 1.0, 30, 0.4, 0) {
        @Override
        void start(EffectLayer layer, Scene scene) {
            double phase = ThreadLocalRandom.current().nextDouble(TAU);
            double y = scene.y + layer.yOffset();
            for (int i = 0; i < layer.amount(); i++) {
                double start = phase + TAU * i / layer.amount();
                SpritePlan plan = plan(layer, scene, i);
                plan.path = (t, out) -> {
                    double angle = start + TAU * layer.turns() * t;
                    set(out, scene.x + Math.cos(angle) * layer.radius(), y + layer.height() * t,
                            scene.z + Math.sin(angle) * layer.radius());
                };
                plan.in = 3;
                plan.out = Math.max(2, layer.duration() / 4);
                scene.engine.add(plan);
            }
        }
    },

    /** Столб: спрайты вспыхивают на разной высоте и медленно поднимаются. */
    COLUMN(12, 0.3, 3.0, 0.0, 16, 0.4, 2) {
        @Override
        void start(EffectLayer layer, Scene scene) {
            ThreadLocalRandom random = ThreadLocalRandom.current();
            for (int i = 0; i < layer.amount(); i++) {
                double x = scene.x + random.nextGaussian() * layer.radius();
                double y = scene.y + layer.yOffset() + random.nextDouble() * layer.height();
                double z = scene.z + random.nextGaussian() * layer.radius();
                SpritePlan plan = plan(layer, scene, i);
                plan.path = (t, out) -> set(out, x, y + 0.6 * t, z);
                plan.step = layer.duration();
                plan.in = 2;
                plan.out = Math.max(2, layer.duration() / 2);
                tumble(plan);
                scene.engine.add(plan);
            }
        }
    },

    /** Знак на земле: растёт до размера size, вращается (spin) и исчезает. */
    DECAL(1, 0.0, 0.0, 0.06, 30, 3.0, 0) {
        @Override
        void start(EffectLayer layer, Scene scene) {
            SpritePlan plan = plan(layer, scene, 0);
            plan.at(scene.x, scene.y + layer.yOffset(), scene.z);
            plan.facing = SpritePlan.Facing.GROUND;
            plan.in = Math.max(2, Math.min(8, layer.duration() / 3));
            plan.out = Math.max(3, layer.duration() / 4);
            plan.roll = (float) Math.toRadians(layer.angle(0));
            scene.engine.add(plan);
        }
    },

    /** Вертикальный столб высотой height и шириной size: молния, луч света. */
    BEAM(1, 0.0, 4.0, 0.0, 12, 1.0, 0) {
        @Override
        void start(EffectLayer layer, Scene scene) {
            for (int i = 0; i < layer.amount(); i++) {
                SpritePlan plan = plan(layer, scene, i);
                scatter(plan, layer, scene);
                plan.y += layer.height() / 2;
                plan.facing = SpritePlan.Facing.UPRIGHT;
                plan.tall = (float) layer.height();
                plan.in = 2;
                plan.out = Math.max(2, layer.duration() / 3);
                plan.spin = 0f;
                plan.roll = 0f;
                scene.engine.add(plan);
            }
        }
    },

    /** Росчерк удара под случайным углом (или под углом angle). */
    SLASH(1, 0.0, 0.0, 1.0, 8, 1.4, 2) {
        @Override
        void start(EffectLayer layer, Scene scene) {
            ThreadLocalRandom random = ThreadLocalRandom.current();
            for (int i = 0; i < layer.amount(); i++) {
                SpritePlan plan = plan(layer, scene, i);
                scatter(plan, layer, scene);
                plan.roll = (float) Math.toRadians(layer.angle(random.nextDouble(360)));
                plan.spin = (float) Math.toRadians(layer.spin());
                popIn(plan);
                plan.in = 2;
                plan.out = Math.max(2, layer.duration() / 2);
                scene.engine.add(plan);
            }
        }
    };

    private static final double TAU = Math.PI * 2;
    private static final double GOLDEN_ANGLE = Math.PI * (3 - Math.sqrt(5));
    /** Ускорение падения спрайтов фонтана, блоков за тик в квадрате. */
    private static final double GRAVITY = 0.045;

    final int amount;
    final double radius;
    final double height;
    final double yOffset;
    final int duration;
    final double size;
    final int interval;

    Animation(int amount, double radius, double height, double yOffset, int duration, double size, int interval) {
        this.amount = amount;
        this.radius = radius;
        this.height = height;
        this.yOffset = yOffset;
        this.duration = duration;
        this.size = size;
        this.interval = interval;
    }

    /** Ставит в очередь все спрайты слоя. */
    abstract void start(EffectLayer layer, Scene scene);

    /** Общая заготовка спрайта: картинка, размер, время жизни и задержка. */
    private static SpritePlan plan(EffectLayer layer, Scene scene, int index) {
        ThreadLocalRandom random = ThreadLocalRandom.current();
        SpriteSpec sprite = layer.sprite();
        SpritePlan plan = new SpritePlan(scene.world, scene.only);
        plan.item = sprite.pick();
        plan.frames = sprite.frames();
        plan.frameTicks = sprite.frameTicks();
        plan.glow = sprite.glow();
        plan.life = layer.duration();
        plan.delay = layer.delay() + index * layer.interval();
        double size = layer.sizeMax() > layer.sizeMin()
                ? random.nextDouble(layer.sizeMin(), layer.sizeMax()) : layer.sizeMin();
        plan.size = (float) size;
        plan.endSize = (float) (size * layer.endSize());
        plan.spin = (float) Math.toRadians(layer.spin());
        plan.at(scene.x, scene.y + layer.yOffset(), scene.z);
        return plan;
    }

    /** Случайная точка в круге радиуса radius. */
    private static void scatter(SpritePlan plan, EffectLayer layer, Scene scene) {
        if (layer.radius() <= 0) {
            return;
        }
        ThreadLocalRandom random = ThreadLocalRandom.current();
        double angle = random.nextDouble(TAU);
        double distance = Math.sqrt(random.nextDouble()) * layer.radius();
        plan.x = scene.x + Math.cos(angle) * distance;
        plan.z = scene.z + Math.sin(angle) * distance;
    }

    private static void popIn(SpritePlan plan) {
        plan.in = 3;
        plan.overshoot = true;
    }

    /** Вращающиеся спрайты стартуют под случайным углом и крутятся в случайную сторону. */
    private static void tumble(SpritePlan plan) {
        if (plan.spin == 0f) {
            return;
        }
        ThreadLocalRandom random = ThreadLocalRandom.current();
        plan.roll = (float) random.nextDouble(TAU);
        if (random.nextBoolean()) {
            plan.spin = -plan.spin;
        }
    }

    private static void swirl(EffectLayer layer, Scene scene, boolean widening) {
        double phase = ThreadLocalRandom.current().nextDouble(TAU);
        double y = scene.y + layer.yOffset();
        int strands = Math.max(1, layer.strands());
        for (int strand = 0; strand < strands; strand++) {
            double start = phase + TAU * strand / strands;
            for (int i = 0; i < layer.amount(); i++) {
                SpritePlan plan = plan(layer, scene, i);
                plan.path = (t, out) -> {
                    double angle = start + TAU * layer.turns() * t;
                    double radius = widening ? layer.radius() * (0.15 + 0.85 * t) : layer.radius();
                    set(out, scene.x + Math.cos(angle) * radius, y + layer.height() * t,
                            scene.z + Math.sin(angle) * radius);
                };
                plan.in = 2;
                plan.out = Math.max(2, layer.duration() / 4);
                scene.engine.add(plan);
            }
        }
    }

    private static void set(double[] out, double x, double y, double z) {
        out[0] = x;
        out[1] = y;
        out[2] = z;
    }

    /** Где и для кого проигрывается эффект. */
    static final class Scene {
        final SpriteEngine engine;
        final World world;
        final Player only;
        final double x;
        final double y;
        final double z;

        Scene(SpriteEngine engine, World world, Player only, double x, double y, double z) {
            this.engine = engine;
            this.world = world;
            this.only = only;
            this.x = x;
            this.y = y;
            this.z = z;
        }
    }
}
