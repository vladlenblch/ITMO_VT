package chars;

public class AnyOther extends Character {
    public AnyOther(String creature) {
        super(creature);
    }

    public String shoot(Object target) {
        String message = getCreature() + " стреляет в " + target;
        System.out.println(message);
        return message;
    }

    public String miss(Object target) {
        String message = getCreature() + " промахивается по " + target;
        System.out.println(message);
        return message;
    }

    @Override
    public boolean isAfraidOf(Object target) {
        return target instanceof Wolf;
    }
}
