package data;

import java.time.format.DateTimeFormatter;
import java.util.Objects;
import java.time.LocalDateTime;

import utility.Validatable;

public class Human implements Validatable {
    private long height; //Значение поля должно быть больше 0
    private java.time.LocalDateTime birthday;

    public Human(long height, LocalDateTime birthday) {
        this.height = height;
        this.birthday = birthday;
    }

    public Human(long height) {
        this(height, LocalDateTime.now());
    }

    public void setHeight(long height) {
        this.height = height;
    }

    public long getHeight() {
        return height;
    }

    public void setBirthday(LocalDateTime birthday) {
        this.birthday = birthday;
    }

    public LocalDateTime getBirthday() {
        return birthday;
    }

    @Override
    public boolean validate() {
        return height > 0;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
		if (o == null || getClass() != o.getClass()) return false;
		Human human = (Human) o;
        return Objects.equals(height, human.height) && 
            Objects.equals(birthday, human.birthday);
    }

    @Override
    public int hashCode() {
        return Objects.hash(height, birthday);
    }

    @Override
    public String toString() {
        return String.format(
                "{\"height\": %d, \"birthday\": %s}",
                height,
                birthday != null ? "\"" + birthday.format(DateTimeFormatter.ISO_LOCAL_DATE_TIME) + "\"" : "null"
        );
    }
}
