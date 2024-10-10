package lab2_pack.pokemons;

import lab2_pack.moves.special.MagicalLeaf;
import lab2_pack.moves.special.ShadowBall;
import lab2_pack.moves.status.Confide;
import ru.ifmo.se.pokemon.*;


public class Kirlia extends Pokemon {
    public Kirlia(String name, int level) {
        super(name, level);
        setType(Type.PSYCHIC, Type.FAIRY);
        setStats(38, 35, 35, 65, 55, 50);
        setMove(new ShadowBall(), new Confide(), new MagicalLeaf());
    }
}
