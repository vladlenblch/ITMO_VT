package lab2_pack.moves.special;

import ru.ifmo.se.pokemon.*;

// Shadow Ball deals damage and has a 20% chance of lowering the target's Special Defense by one stage.

public class ShadowBall extends SpecialMove {
    public ShadowBall() {
        super(Type.GHOST, 80, 100);
    }

    @Override
    protected void applyOppEffects(Pokemon def) {
        if (Math.random() < 0.2) def.setMod(Stat.SPECIAL_DEFENSE, -1);
    }

    @Override
    protected String describe() {
        return "использует Shadow Ball";
    }
}
