package lab2_pack.moves.physical;

import ru.ifmo.se.pokemon.*;

// Facade deals damage, and hits with double power (140) if the user is burned, poisoned or paralyzed.
// In the case of a burn, the usual attack-halving still occurs so Facade hits with an effective power of 70.

public class Facade extends PhysicalMove {
    public Facade() {
        super(Type.NORMAL, 70, 100);
    }

    @Override
    protected void applyOppDamage(Pokemon def, double damage) {
        switch (def.getCondition()) {
            case BURN, POISON, PARALYZE -> super.applyOppDamage(def, damage * 2);
            default -> super.applyOppDamage(def, damage);
        }
    }

    @Override
    protected String describe() {
        return "использует Facade";
    }
}
