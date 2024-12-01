package sounds;

import java.util.Objects;

public abstract class SoundEffect {
    private String type;
    private double duration;
    private int volume;

    public SoundEffect(String type, double duration, int volume) {
        this.type = type;
        this.duration = duration;
        this.volume = volume;
    }

    public abstract void play();

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public double getDuration() {
        return duration;
    }

    public void setDuration(double duration) {
        this.duration = duration;
    }

    public int getVolume() {
        return volume;
    }

    public void setVolume(int volume) {
        this.volume = volume;
    }

    protected String getDurationLevel() {
        if (duration > 2) {
            return "долгий";
        } else {
            return "короткий";
        }
    }

    protected String getVolumeLevel() {
        if (volume > 60) {
            return "громкий";
        } else {
            return "приглушенный";
        }
    }

    @Override
    public String toString() {
        return getDurationLevel() + " и " + getVolumeLevel() + " звук " + getType();
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) {
            return true;
        }
        if (o == null || getClass() != o.getClass()) {
            return false;
        }
        SoundEffect that = (SoundEffect) o;
        return Double.compare(duration, that.duration) == 0 &&
                volume == that.volume &&
                Objects.equals(type, that.type);
    }

    @Override
    public int hashCode() {
        return Objects.hash(type, volume, duration);
    }
}
