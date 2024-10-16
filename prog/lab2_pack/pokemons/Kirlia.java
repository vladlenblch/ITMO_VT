package pokemons;

import moves.special.MagicalLeaf;
import moves.special.ShadowBall;
import moves.status.Confide;
import ru.ifmo.se.pokemon.*;


public class Kirlia extends Pokemon {
    public Kirlia(String name, int level) {
        super(name, level);
        setType(Type.PSYCHIC, Type.FAIRY);
        setStats(38, 35, 35, 65, 55, 50);
        setMove(new ShadowBall(), new Confide(), new MagicalLeaf());
    }
}
