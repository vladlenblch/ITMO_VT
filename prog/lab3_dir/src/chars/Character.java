package chars;

import interfaces.*;

import java.util.Objects;

public abstract class Character implements IsAlive, IsAfraid {
    private String creature;
    private boolean alive;

    public Character(String creature) {
        this.creature = creature;
        this.alive = true;
    }

    public String getCreature() {
        return creature;
    }

    public void setCreature(String creature) {
        this.creature = creature;
    }

    public boolean isAlive() {
        return alive;
    }

    public void die() {
        if (alive) {
            alive = false;
            System.out.println(creature + " погибает...");
        } else {
            System.out.println(creature + " уже мертв...");
        }
    }

    public abstract boolean isAfraidOf(Object target);

    public void reactToFear(Object target) {
        if (isAfraidOf(target)) {
            System.out.println(creature + " боится " + target);
        } else {
            System.out.println(creature + " не боится " + target);
        }
    }

    @Override
    public String toString() {
        return getCreature();
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) {
            return true;
        }
        if (o == null || getClass() != o.getClass()) {
            return false;
        }
        Character character = (Character) o;
        return alive == character.alive && Objects.equals(creature, character.creature);
    }

    @Override
    public int hashCode() {
        return Objects.hash(creature, alive);
    }
}
