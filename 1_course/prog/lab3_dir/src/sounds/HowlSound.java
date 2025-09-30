package sounds;

public class HowlSound extends SoundEffect {
    public HowlSound(String type, double duration, int volume) {
        super(type, duration, volume);
    }

    @Override
    public void play() {
        System.out.println("вдруг послышался " + getDurationLevel() + " и " + getVolumeLevel() + " звук " + getType());
    }
}
