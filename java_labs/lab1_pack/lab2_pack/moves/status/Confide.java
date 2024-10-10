package lab2_pack.moves.status;

import ru.ifmo.se.pokemon.*;

// Confide lowers the target's Special Attack by one stage.

public class Confide extends StatusMove {
    public Confide() {
        super(Type.NORMAL, 0, 0);
    }

    @Override
    protected void applyOppEffects(Pokemon def) {
        def.setMod(Stat.SPECIAL_ATTACK, -1);
    }

    @Override
    protected String describe() {
        return "использует Confide";
    }
}
