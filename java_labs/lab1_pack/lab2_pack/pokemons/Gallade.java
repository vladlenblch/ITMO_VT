package lab2_pack.pokemons;

import lab2_pack.moves.special.MagicalLeaf;
import lab2_pack.moves.special.ShadowBall;
import lab2_pack.moves.status.Confide;
import lab2_pack.moves.status.HealPulse;
import ru.ifmo.se.pokemon.*;

public class Gallade extends Pokemon {
    public Gallade(String name, int level) {
        super(name, level);
        setType(Type.PSYCHIC, Type.FAIRY);
        setStats(68, 125, 65, 65, 115, 80);
        setMove(new ShadowBall(), new Confide(), new MagicalLeaf(), new HealPulse());
    }
}
