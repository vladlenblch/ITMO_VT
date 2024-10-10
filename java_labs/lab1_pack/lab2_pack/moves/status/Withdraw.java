package lab2_pack.moves.status;

import ru.ifmo.se.pokemon.*;

// Withdraw raises the user's Defense by one stage.

public class Withdraw extends StatusMove {
    public Withdraw() {
        super(Type.WATER, 0, 0);
    }

    @Override
    protected void applySelfEffects(Pokemon def) {
        def.setMod(Stat.DEFENSE, 1);
    }

    @Override
    protected String describe() {
        return "использует Withdraw";
    }
}
