package common.data;

import common.utility.Validatable;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.Locale;
import java.util.Objects;

/**
 * Класс, представляющий сущность "Город".
 * Содержит информацию о городе, такую как название, координаты, площадь, население и т.д.
 * Реализует интерфейс {@link Validatable} для проверки валидности данных.
 */
public class City implements Validatable {

    /** Уникальный идентификатор города. Должен быть больше 0. */
    private int id;

    /** Название города. Не может быть null или пустой строкой. */
    private String name;

    /** Координаты города. Не может быть null. */
    private Coordinates coordinates;

    /** Дата создания записи о городе. Не может быть null. */
    private LocalDate creationDate;

    /** Площадь города. Должна быть больше 0. */
    private int area;

    /** Население города. Должно быть больше 0 и не может быть null. */
    private Integer population;

    /** Высота над уровнем моря. */
    private int metersAboveSeaLevel;

    /** Климат города. Может быть null. */
    private Climate climate;

    /** Форма правления. Не может быть null. */
    private Government government;

    /** Уровень жизни. Не может быть null. */
    private StandardOfLiving standardOfLiving;

    /** Губернатор города. Не может быть null. */
    private Human governor;

    /**
     * Основной конструктор для создания объекта City.
     *
     * @param id                   уникальный идентификатор города
     * @param name                 название города
     * @param coordinates          координаты города
     * @param creationDate         дата создания записи о городе
     * @param area                 площадь города
     * @param population           население города
     * @param metersAboveSeaLevel  высота над уровнем моря
     * @param climate              климат города
     * @param government           форма правления
     * @param standardOfLiving     уровень жизни
     * @param governor             губернатор города
     */
    public City(int id, String name, Coordinates coordinates, LocalDate creationDate, int area, Integer population, int metersAboveSeaLevel,
                Climate climate, Government government, StandardOfLiving standardOfLiving, Human governor) {
        this.id = id;
        this.name = name;
        this.coordinates = coordinates;
        this.creationDate = creationDate;
        this.area = area;
        this.population = population;
        this.metersAboveSeaLevel = metersAboveSeaLevel;
        this.climate = climate;
        this.government = government;
        this.standardOfLiving = standardOfLiving;
        this.governor = governor;
    }

    /**
     * Вспомогательный конструктор для создания объекта City.
     * Устанавливает текущую дату как дату создания записи.
     *
     * @param id                   уникальный идентификатор города
     * @param name                 название города
     * @param coordinates          координаты города
     * @param area                 площадь города
     * @param population           население города
     * @param metersAboveSeaLevel  высота над уровнем моря
     * @param climate              климат города
     * @param government           форма правления
     * @param standardOfLiving     уровень жизни
     * @param governor             губернатор города
     */
    public City(int id, String name, Coordinates coordinates, int area, Integer population, int metersAboveSeaLevel,
                Climate climate, Government government, StandardOfLiving standardOfLiving, Human governor) {
        this(id, name, coordinates, LocalDate.now(), area, population, metersAboveSeaLevel, climate, government, standardOfLiving, governor);
    }

    /**
     * Устанавливает уникальный идентификатор города.
     *
     * @param id уникальный идентификатор города
     */
    public void setId(int id) {
        this.id = id;
    }

    /**
     * Возвращает уникальный идентификатор города.
     *
     * @return уникальный идентификатор города
     */
    public int getId() {
        return id;
    }

    /**
     * Возвращает название города.
     *
     * @return название города
     */
    public String getName() {
        return name;
    }

    /**
     * Возвращает координаты города.
     *
     * @return координаты города
     */
    public Coordinates getCoordinates() {
        return coordinates;
    }

    /**
     * Возвращает дату создания записи о городе.
     *
     * @return дата создания записи о городе
     */
    public LocalDate getCreationDate() {
        return creationDate;
    }

    /**
     * Возвращает площадь города.
     *
     * @return площадь города
     */
    public int getArea() {
        return area;
    }

    /**
     * Возвращает население города.
     *
     * @return население города
     */
    public Integer getPopulation() {
        return population;
    }

    /**
     * Возвращает высоту над уровнем моря.
     *
     * @return высота над уровнем моря
     */
    public int getMetersAboveSeaLevel() {
        return metersAboveSeaLevel;
    }

    /**
     * Возвращает климат города.
     *
     * @return климат города
     */
    public Climate getClimate() {
        return climate;
    }

    /**
     * Возвращает форму правления.
     *
     * @return форма правления
     */
    public Government getGovernment() {
        return government;
    }

    /**
     * Возвращает уровень жизни.
     *
     * @return уровень жизни
     */
    public StandardOfLiving getStandardOfLiving() {
        return standardOfLiving;
    }

    /**
     * Возвращает губернатора города.
     *
     * @return губернатор города
     */
    public Human getGovernor() {
        return governor;
    }

    /**
     * Возвращает строковое представление города в формате "id/name/coordinates/...".
     * Все поля разделены слешами. В случае ошибки возвращает пустую строку.
     *
     * @return строковое представление объекта в упрощенном формате или пустая строка при ошибке
     */
    public String toStr() {
        try {
            String coords = String.format(Locale.US, "%d;%.6f",
                    coordinates.getX(), coordinates.getY());

            return String.format("%d/%s/%s/%s/%d/%d/%d/%s/%s/%s/%d;%s",
                    id,
                    name,
                    coords,
                    creationDate.toString(),
                    area,
                    population,
                    metersAboveSeaLevel,
                    climate != null ? climate.toString() : "null",
                    government != null ? government.toString() : "null",
                    standardOfLiving != null ? standardOfLiving.toString() : "null",
                    governor.getHeight(),
                    governor.getBirthday().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME)
            );
        } catch (NullPointerException e) {
            return "";
        }
    }

    /**
     * Создает объект City из массива строк. Ожидается следующий порядок данных:
     * [0]-ID, [1]-name, [2]-coordinates(x;y), [3]-creationDate(ISO), [4]-area,
     * [5]-population, [6]-metersAboveSeaLevel, [7]-climate, [8]-government,
     * [9]-standardOfLiving, [10]-governor(name;age).
     * Для enum-полей используются их строковые представления.
     *
     * @param args массив строк с данными города
     * @return новый объект City или null при ошибках в данных
     * @throws ArrayIndexOutOfBoundsException если массив короче 11 элементов
     */
    public static City fromArray(String[] args) {
        try {
            Integer id = safeParseInt(args[0]);
            String name = args[1];
            Coordinates coordinates = Coordinates.fromString(args[2]);
            LocalDate creationDate = parseDate(args[3]);
            Integer area = safeParseInt(args[4]);
            Integer population = safeParseInt(args[5]);
            Integer metersAboveSeaLevel = safeParseInt(args[6]);
            Climate climate = parseEnum(Climate.class, args[7]);
            Government government = parseEnum(Government.class, args[8]);
            StandardOfLiving standardOfLiving = parseEnum(StandardOfLiving.class, args[9]);
            Human governor = Human.fromString(args[10]);

            return new City(id, name, coordinates, creationDate, area, population,
                    metersAboveSeaLevel, climate, government, standardOfLiving, governor);
        } catch (ArrayIndexOutOfBoundsException e) {
            return null;
        }
    }

    /**
     * Безопасно парсит строку в Integer, возвращает null при ошибке.
     */
    private static Integer safeParseInt(String s) {
        try {
            return Integer.parseInt(s);
        } catch (NumberFormatException e) {
            return null;
        }
    }

    /**
     * Парсит строку в LocalDate, возвращает null при ошибке.
     */
    private static LocalDate parseDate(String s) {
        try {
            return LocalDate.parse(s);
        } catch (Exception e) {
            return null;
        }
    }
    /**
     * Парсит строку в значение enum, возвращает null при ошибке.
     */
    private static <T extends Enum<T>> T parseEnum(Class<T> enumClass, String s) {
        try {
            return Enum.valueOf(enumClass, s);
        } catch (IllegalArgumentException e) {
            return null;
        }
    }

    /**
     * Проверяет валидность объекта.
     *
     * @return true, если все поля валидны, иначе false
     */
    @Override
    public boolean validate() {
        return this.id > 0 &&
                this.name != null && !this.name.isEmpty() &&
                this.coordinates != null && this.coordinates.validate() &&
                this.creationDate != null &&
                this.area > 0 &&
                this.population != null && this.population > 0 &&
                this.government != null &&
                this.standardOfLiving != null &&
                this.governor != null && this.governor.validate();
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
        City city = (City) o;
        return Objects.equals(id, city.id);
    }

    /**
     * Возвращает хэш-код объекта.
     *
     * @return хэш-код
     */
    @Override
    public String toString() {
        return String.format(Locale.US,
                "{\"id\": %d, \"name\": \"%s\", \"coordinates\": %s, \"creationDate\": \"%s\", " +
                        "\"area\": %d, \"population\": %d, \"metersAboveSeaLevel\": %d, " +
                        "\"climate\": \"%s\", \"government\": \"%s\", \"standardOfLiving\": \"%s\", " +
                        "\"governor\": %s}",
                id,
                name,
                coordinates.toString(),
                creationDate.toString(),
                area,
                population,
                metersAboveSeaLevel,
                climate != null ? climate.toString() : "null",
                government != null ? government.toString() : "null",
                standardOfLiving != null ? standardOfLiving.toString() : "null",
                governor.toString()
        );
    }
}