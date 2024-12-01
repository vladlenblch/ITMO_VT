package chars;

import java.util.ArrayList;

public class Squad extends Character {
    public Squad(String creature) {
        super(creature);
    }

    @Override
    public boolean isAfraidOf(Object target) {
        if (target instanceof ArrayList) {
            ArrayList<?> wolves = (ArrayList<?>) target;

            if (wolves.size() > 5) {
                System.out.println(getCreature() + " боится волков, их слишком много");
                return true;
            }
        }
        System.out.println(getCreature() + " не боится волков, ведь их не так много");
        return false;
    }
}
