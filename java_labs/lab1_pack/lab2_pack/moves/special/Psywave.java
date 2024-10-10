package lab2_pack.moves.special;

import ru.ifmo.se.pokemon.*;

// Psywave inflicts a random amount of HP damage, varying between 50% and 150% of the user's level.

public class Psywave extends SpecialMove {
    public Psywave() {
        super(Type.PSYCHIC, 0, 100);
    }

    @Override
    protected void applyOppDamage(Pokemon def, double damage) {
        super.applyOppDamage(def, def.getLevel() * (Math.random() + 0.5));
    }

    @Override
    protected String describe() {
        return "использует Psywave";
    }
}
