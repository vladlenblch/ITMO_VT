package moves.special;

import ru.ifmo.se.pokemon.*;

// Dream Eater deals damage only on sleeping foes and the user will recover 50% of the HP drained.

public class DreamEater extends SpecialMove {
    public DreamEater() {
        super(Type.PSYCHIC, 100, 100);
    }

    @Override
    protected void applyOppDamage(Pokemon def, double damage) {
        if (def.getCondition() == Status.SLEEP) {
            super.applyOppDamage(def, damage);
        } else {
            super.applyOppDamage(def, damage * 0);
        }
    }

    @Override
    protected void applySelfDamage(Pokemon def, double damage) {
        super.applySelfDamage(def, -1 * damage);
    }

    @Override
    protected String describe() {
        return "использует Dream Eater";
    }
}
