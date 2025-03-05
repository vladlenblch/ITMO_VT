package data;

import java.util.Objects;

import utility.Validatable;

/**
 * Класс, представляющий координаты.
 * Содержит информацию о координатах по осям X и Y.
 * Реализует интерфейс {@link utility.Validatable} для проверки валидности данных.
 */
public class Coordinates implements Validatable {

    /** Координата по оси X. */
    private long x;

    /** Координата по оси Y. Значение должно быть больше -339 и не может быть null. */
    private Double y;

    /**
     * Основной конструктор для создания объекта Coordinates.
     *
     * @param x координата по оси X
     * @param y координата по оси Y (должна быть больше -339 и не может быть null)
     */
    public Coordinates(long x, Double y) {
        this.x = x;
        this.y = y;
    }

    /**
     * Возвращает координату по оси X.
     *
     * @return координата по оси X
     */
    public long getX() {
        return x;
    }

    /**
     * Возвращает координату по оси Y.
     *
     * @return координата по оси Y
     */
    public Double getY() {
        return y;
    }

    /**
     * Проверяет валидность объекта.
     *
     * @return true, если координата Y больше -339, иначе false
     */
    @Override
    public boolean validate() {
        return y != null && y > -339;
    }

    /**
     * Сравнивает объекты на равенство.
     *
     * @param o объект для сравнения
     * @return true, если объекты равны, иначе false
     */
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Coordinates that = (Coordinates) o;
        return Objects.equals(x, that.x) &&
                Objects.equals(y, that.y);
    }

    /**
     * Возвращает хэш-код объекта.
     *
     * @return хэш-код
     */
    @Override
    public int hashCode() {
        return Objects.hash(x, y);
    }

    /**
     * Возвращает строковое представление объекта в формате JSON.
     *
     * @return строковое представление объекта
     */
    @Override
    public String toString() {
        return String.format(
                "{\"x\": %d, \"y\": %s}",
                x,
                y.toString().replace(',', '.')
        );
    }
}