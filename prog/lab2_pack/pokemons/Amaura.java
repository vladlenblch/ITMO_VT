package lab2_pack.pokemons;

import lab2_pack.moves.physical.StoneEdge;
import lab2_pack.moves.special.DreamEater;
import lab2_pack.moves.status.DoubleTeam;
import ru.ifmo.se.pokemon.*;


public class Amaura extends Pokemon {
    public Amaura(String name, int level) {
        super(name, level);
        setType(Type.ROCK, Type.ICE);
        setStats(77, 59, 50, 67, 63, 46);
        setMove(new DoubleTeam(), new StoneEdge(), new DreamEater());
    }
}
