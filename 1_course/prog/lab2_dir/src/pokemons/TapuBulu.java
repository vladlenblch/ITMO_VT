package pokemons;

import moves.physical.Facade;
import moves.special.Psywave;
import moves.status.Swagger;
import moves.status.Withdraw;
import ru.ifmo.se.pokemon.*;

public class TapuBulu extends Pokemon {
    public TapuBulu(String name, int level) {
        super(name, level);
        setType(Type.GRASS, Type.FAIRY);
        setStats(70, 130, 115, 85, 95, 75);
        setMove(new Psywave(), new Facade(), new Withdraw(), new Swagger());
    }
}
