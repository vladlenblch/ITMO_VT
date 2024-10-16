package pokemons;

import moves.physical.StoneEdge;
import moves.special.DreamEater;
import moves.special.Thunder;
import moves.status.DoubleTeam;
import ru.ifmo.se.pokemon.*;

public class Aurorus extends Pokemon {
    public Aurorus(String name, int level) {
        super(name, level);
        setType(Type.ROCK, Type.ICE);
        setStats(123, 77, 72, 99, 92, 58);
        setMove(new DoubleTeam(), new StoneEdge(), new DreamEater(), new Thunder());
    }
}
