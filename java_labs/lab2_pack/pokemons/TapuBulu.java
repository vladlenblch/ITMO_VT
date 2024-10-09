package lab2_pack.pokemons;

import lab2_pack.moves.physical.Facade;
import lab2_pack.moves.special.Psywave;
import lab2_pack.moves.status.Swagger;
import lab2_pack.moves.status.Withdraw;
import ru.ifmo.se.pokemon.*;

public class TapuBulu extends Pokemon {
    public TapuBulu(String name, int level) {
        super(name, level);
        setType(Type.GRASS, Type.FAIRY);
        setStats(70, 130, 115, 85, 95, 75);
        setMove(new Psywave(), new Facade(), new Withdraw(), new Swagger());
    }
}
