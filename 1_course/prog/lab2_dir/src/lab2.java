import pokemons.*;
import ru.ifmo.se.pokemon.*;

public class lab2 {
    public static void main(String[] args) {
        Battle b = new Battle();

        TapuBulu tapubulu = new TapuBulu("'летающий гад'", 1);
        Amaura amaura = new Amaura("'морской пони'", 1);
        Aurorus aurorus = new Aurorus("'водный чорт'", 1);
        Ralts ralts = new Ralts("'микро бро'", 1);
        Kirlia kirlia = new Kirlia("'бро побольше'", 1);
        Gallade gallade = new Gallade("'большой бро'", 1);

        b.addAlly(tapubulu);
        b.addAlly(amaura);
        b.addAlly(aurorus);

        b.addFoe(ralts);
        b.addFoe(kirlia);
        b.addFoe(gallade);

        b.go();
    }
}
