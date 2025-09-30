import chars.*;
import exceptions.*;
import sounds.*;
import enums.*;
import records.*;

import java.util.ArrayList;
import java.util.Random;

public class lab3 {
    public static void main(String[] args) {
        PoorPerson poorPerson = new PoorPerson("бедняк");
        Friday friday = new Friday("пятница");
        Squad squad = new Squad("отряд");
        AnyOther anyOther = new AnyOther("любой другой");
        Wolf wolf = new Wolf("волки");
        ArrayList<Wolf> wolves = generateRandomWolves();

        HowlSound howlSound = new HowlSound("волчий вой", wolves.size()*2, wolves.size()*10);
        EchoSound echoSound = new EchoSound("эхо", howlSound.getDuration()*2, howlSound.getVolume()*2);
        ShotSound shotSound = new ShotSound("выстрел", 0.5, 80);

        ShotInfo shotInfo = new ShotInfo(shotSound.getDuration(), shotSound.getVolume());

        System.out.println(location.MOUNTAINS.getDescription() + " везде");
        System.out.println(location.SNOW.getDescription() + " повсюду");
        System.out.println(location.OLDCAR.getDescription() + " стоят на " + location.ROAD.getDescription());
        System.out.println(" ");

        try {
            friday.gallop(poorPerson);
        } catch (InvalidActionException e) {
            System.out.println("ошибка: " + e.getMessage());
        }

        poorPerson.approach(wolf);
        System.out.println(" ");
        shotSound.play();

        try {
            poorPerson.shoot(wolves);
        } catch (NoWolvesException e) {
            System.out.println("ошибка: " + e.getMessage());
        }
        System.out.println("был произведен выстрел, его продолжительность: " + shotInfo.duration() + " секунд, а громкость: " + shotInfo.volume() + " децибел");

        poorPerson.reactToFear(wolf);
        System.out.println(" ");

        anyOther.shoot(wolf);
        anyOther.miss(wolf);
        anyOther.reactToFear(wolf);
        System.out.println(" ");

        howlSound.play();
        echoSound.play();
        System.out.println(" ");
        squad.isAfraidOf(wolves);
    }

    public static ArrayList<Wolf> generateRandomWolves() {
        Random random = new Random();
        int numberOfWolves = random.nextInt(20) + 1;

        ArrayList<Wolf> wolves = new ArrayList<>();
        for (int i = 1; i <= numberOfWolves; i++) {
            wolves.add(new Wolf("волк " + i));
        }

        return wolves;
    }
}
