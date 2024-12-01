package chars;
import exceptions.InvalidActionException;

public class Friday extends Character {
    public Friday(String creature) {
        super(creature);
    }

    public String gallop(Object target) throws InvalidActionException {
        if (target == null) {
            throw new InvalidActionException("бедняка не существует");
        }
        String message = getCreature() + " подскакивает к " + target;
        System.out.println(message);
        return message;
    }

    @Override
    public boolean isAfraidOf(Object target) {
        return false;
    }
}
