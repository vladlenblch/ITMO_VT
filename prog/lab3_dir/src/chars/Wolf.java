package chars;

public class Wolf extends Character {
    public Wolf(String creature) {
        super(creature);
    }

    @Override
    public boolean isAfraidOf(Object target) {
        return false;
    }

    @Override
    public String toString() {
        return "волк";
    }
}
