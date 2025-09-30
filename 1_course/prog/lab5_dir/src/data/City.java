package data;

import java.time.LocalDate;
import java.util.Objects;

import utility.Validatable;

/**
 * Класс, представляющий сущность "Город".
 * Содержит информацию о городе, такую как название, координаты, площадь, население и т.д.
 * Реализует интерфейс {@link utility.Validatable} для проверки валидности данных.
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
    public int hashCode() {
        return Objects.hash(id, name, coordinates, creationDate, area, population, metersAboveSeaLevel, climate, government, standardOfLiving, governor);
    }

    /**
     * Возвращает строковое представление объекта в формате JSON.
     *
     * @return строковое представление объекта
     */
    @Override
    public String toString() {
        return String.format(
                "{\"id\"=%s, \"name\"=%s, \"coordinates\"=%s, \"creationDate\"=%s, \"area\"=%s, \"population\"=%s, \"metersAboveSeaLevel\"=%s, \"climate\"=%s, \"government\"=%s, \"standardOfLiving\"=%s, \"governor\"=%s}",
                id, name, coordinates, creationDate, area, population, metersAboveSeaLevel, climate, government, standardOfLiving, governor
        );
    }
}