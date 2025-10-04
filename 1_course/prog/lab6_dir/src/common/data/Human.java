package common.data;

import common.utility.Validatable;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;
import java.util.Locale;
import java.util.Objects;

/**
 * Класс, представляющий сущность "Человек".
 * Содержит информацию о росте и дате рождения.
 * Реализует интерфейс {@link Validatable} для проверки валидности данных.
 */
public class Human implements Validatable {

    /** Рост человека. Значение должно быть больше 0. */
    private long height;

    /** Дата рождения человека. */
    private LocalDateTime birthday;

    /**
     * Основной конструктор для создания объекта Human.
     *
     * @param height   рост человека (должен быть больше 0)
     * @param birthday дата рождения
     */
    public Human(long height, LocalDateTime birthday) {
        this.height = height;
        this.birthday = birthday;
    }

    /**
     * Возвращает рост человека.
     *
     * @return рост человека
     */
    public long getHeight() {
        return height;
    }

    /**
     * Возвращает дату рождения человека.
     *
     * @return дата рождения
     */
    public LocalDateTime getBirthday() {
        return birthday;
    }

    public static Human fromString(String str) {
        try {
            String[] parts = str.split(";");
            if (parts.length != 2) {
                throw new IllegalArgumentException("Неверный формат данных. Ожидается height;birthday");
            }
            long height = Long.parseLong(parts[0]);
            if (height <= 0) {
                throw new IllegalArgumentException("Рост должен быть больше 0");
            }
            LocalDateTime birthday = LocalDateTime.parse(parts[1], DateTimeFormatter.ISO_LOCAL_DATE_TIME);
            return new Human(height, birthday);
        } catch (DateTimeParseException e) {
            throw new IllegalArgumentException("Неверный формат даты. Используйте ISO формат (yyyy-MM-dd'T'HH:mm:ss)", e);
        } catch (NumberFormatException e) {
            throw new IllegalArgumentException("Рост должен быть целым числом", e);
        }
    }

    /**
     * Проверяет валидность объекта.
     *
     * @return true, если рост больше 0, иначе false
     */
    @Override
    public boolean validate() {
        return height > 0;
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
        Human human = (Human) o;
        return Objects.equals(height, human.height) &&
                Objects.equals(birthday, human.birthday);
    }

    /**
     * Возвращает хэш-код объекта.
     *
     * @return хэш-код
     */
    @Override
    public int hashCode() {
        return Objects.hash(height, birthday);
    }

    /**
     * Возвращает строковое представление объекта в формате JSON.
     *
     * @return строковое представление объекта
     */
    @Override
    public String toString() {
        return String.format(Locale.US,
                "{\"height\": %d, \"birthday\": \"%s\"}",
                height,
                birthday.format(DateTimeFormatter.ISO_LOCAL_DATE_TIME)
        );
    }
}