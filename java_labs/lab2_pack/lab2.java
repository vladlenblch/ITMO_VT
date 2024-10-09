package lab2_pack;

import lab2_pack.pokemons.*;
import ru.ifmo.se.pokemon.*;

public class lab2 {
    public static void main(String[] args) {
        Battle b = new Battle();

        TapuBulu tapubulu = new TapuBulu("Tapu-Bulu", 1);
        Amaura amaura = new Amaura("Amaura", 1);
        Aurorus aurorus = new Aurorus("Aurorus", 1);
        Ralts ralts = new Ralts("Ralts", 1);
        Kirlia kirlia = new Kirlia("Kirlia", 1);
        Gallade gallade = new Gallade("Gallade", 1);

        // b.addAlly(tapubulu);
        // b.addAlly(amaura);
        b.addAlly(aurorus);

        // b.addFoe(ralts);
        // b.addFoe(kirlia);
        b.addFoe(gallade);

        b.go();
    }
}
