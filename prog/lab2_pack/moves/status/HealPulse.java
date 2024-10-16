package moves.status;

import ru.ifmo.se.pokemon.*;

//Heal Pulse restores half of the target's maximum HP. It can be used on team-mates but not on itself.

public class HealPulse extends StatusMove {
    public HealPulse() {
        super(Type.PSYCHIC, 0, 0);
    }

    @Override
    protected void applyOppEffects(Pokemon def) {
        def.setMod(Stat.HP, (int) def.getStat(Stat.HP) / 2);
    }

    @Override
    protected String describe() {
        return "использует Heal Pulse";
    }
}
