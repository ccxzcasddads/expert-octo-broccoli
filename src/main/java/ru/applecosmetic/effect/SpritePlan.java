package ru.applecosmetic.effect;

import java.util.List;
import org.bukkit.World;
import org.bukkit.entity.Player;
import org.bukkit.inventory.ItemStack;

/** Один спрайт от появления до исчезновения: где он, как движется и как меняет размер. */
final class SpritePlan {

    /** Как спрайт повёрнут в мире. */
    enum Facing {
        /** Всегда лицом к игроку. */
        CAMERA,
        /** Стоит вертикально и поворачивается к игроку только вокруг своей оси. */
        UPRIGHT,
        /** Лежит на земле. */
        GROUND
    }

    /** Положение спрайта в момент t от 0 до 1; координаты записываются в out. */
    @FunctionalInterface
    interface Path {
        void at(double t, double[] out);
    }

    final World world;
    /** Единственный зритель (предпросмотр); null — видят все поблизости. */
    final Player only;

    ItemStack item;
    /** Кадры по порядку; пустой список — картинка не меняется. */
    List<ItemStack> frames = List.of();
    int frameTicks = 2;
    boolean glow = true;
    Facing facing = Facing.CAMERA;

    double x;
    double y;
    double z;
    /** Траектория; null — спрайт стоит на месте. */
    Path path;
    /** Раз в сколько тиков серверу сдвигать спрайт: между сдвигами клиент ведёт его плавно. */
    int step = 2;

    /** Сколько тиков живёт спрайт и через сколько тиков появляется. */
    int life = 20;
    int delay;

    float size = 1f;
    float endSize;
    /** Тики на появление (от нуля до size) и на исчезновение (от size до endSize); 0 — без этой фазы. */
    int in;
    int out;
    /** При появлении спрайт на мгновение становится чуть больше своего размера. */
    boolean overshoot;
    /** Больше нуля — высота спрайта в блоках, которая не зависит от size (столбы света). */
    float tall;

    /** Начальный поворот и скорость вращения, в радианах и радианах за тик. */
    float roll;
    float spin;

    SpritePlan(World world, Player only) {
        this.world = world;
        this.only = only;
    }

    SpritePlan at(double x, double y, double z) {
        this.x = x;
        this.y = y;
        this.z = z;
        return this;
    }
}
