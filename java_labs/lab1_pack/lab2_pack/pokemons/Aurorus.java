package lab2_pack.pokemons;

import lab2_pack.moves.physical.StoneEdge;
import lab2_pack.moves.special.DreamEater;
import lab2_pack.moves.special.Thunder;
import lab2_pack.moves.status.DoubleTeam;
import ru.ifmo.se.pokemon.*;

public class Aurorus extends Pokemon {
    public Aurorus(String name, int level) {
        super(name, level);
        setType(Type.ROCK, Type.ICE);
        setStats(123, 77, 72, 99, 92, 58);
        setMove(new DoubleTeam(), new StoneEdge(), new DreamEater(), new Thunder());
    }
}
