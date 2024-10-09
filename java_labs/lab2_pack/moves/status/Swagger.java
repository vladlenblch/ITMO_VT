package lab2_pack.moves.status;

import ru.ifmo.se.pokemon.*;

// Swagger confuses the target and raises its Attack by two stages.
// If one of the two effects cannot be invoked, Swagger still works and will invoke the other effect.

public class Swagger extends StatusMove {
    public Swagger() {
        super(Type.NORMAL, 0, 85);
    }

    @Override
    protected void applyOppEffects(Pokemon def) {
        def.confuse();
        def.setMod(Stat.ATTACK, 2);
    }

    @Override
    protected String describe() {
        return "использует Swagger";
    }
}
