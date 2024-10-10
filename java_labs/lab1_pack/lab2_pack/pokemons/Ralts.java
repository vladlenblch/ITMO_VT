package lab2_pack.pokemons;

import lab2_pack.moves.special.ShadowBall;
import lab2_pack.moves.status.Confide;
import ru.ifmo.se.pokemon.*;



public class Ralts extends Pokemon {
    public Ralts(String name, int level) {
        super(name, level);
        setType(Type.PSYCHIC, Type.FAIRY);
        setStats(28, 25, 25, 45, 35, 40);
        setMove(new ShadowBall(), new Confide());
    }
}
