package sounds;

public class EchoSound extends SoundEffect {
    public EchoSound(String type, double duration, int volume) {
        super(type, duration, volume);
    }

    @Override
    public void play() {
        System.out.println("вдруг послышался " + getDurationLevel() + " и " + getVolumeLevel() + " звук " + getType());
    }
}
