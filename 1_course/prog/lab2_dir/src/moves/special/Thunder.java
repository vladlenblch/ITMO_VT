package moves.special;

import ru.ifmo.se.pokemon.*;

// Thunder deals damage and has a 30% chance of paralyzing the target.
// Electric type Pokémon cannot be paralyzed.

public class Thunder extends SpecialMove {
    public Thunder() {
        super(Type.ELECTRIC, 110, 70);
    }

    @Override
    protected void applyOppEffects(Pokemon def) {
        if (!def.hasType(Type.ELECTRIC)) {
            if (Math.random() < 0.3) Effect.paralyze(def);
        }
    }

    @Override
    protected String describe() {
        return "использует Thunder";
    }
}
