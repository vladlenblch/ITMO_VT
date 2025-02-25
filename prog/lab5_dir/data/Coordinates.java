package data;

import java.util.Objects;

import utility.Validatable;

public class Coordinates implements Validatable {
    private long x;
    private Double y; //Значение поля должно быть больше -339, Поле не может быть null

    public Coordinates(long x, Double y) {
        this.x = x;
        this.y = y;
    }

    public Coordinates() {
    }

    public void setX(long x) {
        this.x = x;
    }

    public long getX() {
        return x;
    }

    public void setY(Double y) {
        this.y = y;
    }

    public Double getY() {
        return y;
    }

    @Override
    public boolean validate() {
        return y > -339;
    }

    @Override
	public boolean equals(Object o) {
		if (this == o) return true;
		if (o == null || getClass() != o.getClass()) return false;
		Coordinates that = (Coordinates) o;
		return Objects.equals(x, that.x) && 
            Objects.equals(y, that.y);
	}

	@Override
	public int hashCode() {
		return Objects.hash(x, y);
    }
    
    @Override
    public String toString() {
        return String.format(
            "{\"x\": %d, \"y\": %s}",
            x,
            y.toString().replace(',', '.')
        );
    }
}
