package chars;
import exceptions.NoWolvesException;

import java.util.ArrayList;
import java.util.Random;

public class PoorPerson extends Character {
    public PoorPerson(String creature) {
        super(creature);
    }

    public String shoot(ArrayList<Wolf> wolves) {
        if (wolves.isEmpty()) {
            throw new NoWolvesException("волков нет");
        }

        Random random = new Random();
        int randomIndex = random.nextInt(wolves.size());
        Wolf target = wolves.get(randomIndex);

        String message = getCreature() + " стреляет в " + target;
        System.out.println(message);
        target.die();
        return message;
    }

    public String approach(Object target) {
        String message = getCreature() + " подъезжает к " + target;
        System.out.println(message);
        return message;
    }

    @Override
    public boolean isAfraidOf(Object target) {
        return false;
    }
}
