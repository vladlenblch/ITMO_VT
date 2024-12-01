package moves.special;

import ru.ifmo.se.pokemon.*;

// Magical Leaf deals damage and ignores changes to the Accuracy and Evasion stats.

public class MagicalLeaf extends SpecialMove {
    public MagicalLeaf() {
        super(Type.GRASS, 60, Double.POSITIVE_INFINITY);
    }

    @Override
    protected String describe() {
        return "использует Magical Leaf";
    }
}
