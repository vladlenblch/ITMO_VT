package data;

import java.time.LocalDate;
import java.util.Objects;

import utility.Validatable;

public class City implements Validatable {
    private int id; //Значение поля должно быть больше 0, Значение этого поля должно быть уникальным, Значение этого поля должно генерироваться автоматически
    private String name; //Поле не может быть null, Строка не может быть пустой
    private Coordinates coordinates; //Поле не может быть null
    private java.time.LocalDate creationDate; //Поле не может быть null, Значение этого поля должно генерироваться автоматически
    private int area; //Значение поля должно быть больше 0
    private Integer population; //Значение поля должно быть больше 0, Поле не может быть null
    private int metersAboveSeaLevel;
    private Climate climate; //Поле может быть null
    private Government government; //Поле не может быть null
    private StandardOfLiving standardOfLiving; //Поле не может быть null
    private Human governor; //Поле не может быть null

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

    public City(int id, String name, Coordinates coordinates, int area, Integer population, int metersAboveSeaLevel,
                Climate climate, Government government, StandardOfLiving standardOfLiving, Human governor) {
        this(id, name, coordinates, LocalDate.now(), area, population, metersAboveSeaLevel, climate, government, standardOfLiving, governor);
    }

    public void setId(int id) {
        this.id = id;
    }

    public int getId() {
        return id;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public void setCoordinates(Coordinates coordinates) {
        this.coordinates = coordinates;
    }

    public Coordinates getCoordinates() {
        return coordinates;
    }

    public void setCreationDate(LocalDate creationDate) {
        this.creationDate = creationDate;
    }

    public LocalDate getCreationDate() {
        return creationDate;
    }

    public void setArea(int area) {
        this.area = area;
    }

    public int getArea() {
        return area;
    }

    public void setPopulation(Integer population) {
        this.population = population;
    }

    public Integer getPopulation() {
        return population;
    }

    public void setMetersAboveSeaLevel(int metersAboveSeaLevel) {
        this.metersAboveSeaLevel = metersAboveSeaLevel;
    }

    public int getMetersAboveSeaLevel() {
        return metersAboveSeaLevel;
    }

    public void setClimate(Climate climate) {
        this.climate = climate;
    }

    public Climate getClimate() {
        return climate;
    }

    public void setGovernment(Government government) {
        this.government = government;
    }

    public Government getGovernment() {
        return government;
    }

    public void setStandardOfLiving(StandardOfLiving standardOfLiving) {
        this.standardOfLiving = standardOfLiving;
    }

    public StandardOfLiving getStandardOfLiving() {
        return standardOfLiving;
    }

    public void setGovernor(Human governor) {
        this.governor = governor;
    }

    public Human getGovernor() {
        return governor;
    }

    @Override
    public boolean validate() {
        return this.id > 0 && 
            this.name != null && !this.name.isEmpty() && 
            this.coordinates != null && this.coordinates.validate() && 
            this.creationDate != null && 
            this.area > 0 && 
            this.population > 0 && 
            this.government != null && 
            this.standardOfLiving != null && 
            this.governor != null && this.governor.validate();
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        City city = (City) o;
        return Objects.equals(id, city.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id, name, coordinates, creationDate, area, population, metersAboveSeaLevel, climate, government, standardOfLiving, governor);
    }

    @Override
    public String toString() {
        return String.format(
            "{\"id\"=%s, \"name\"=%s, \"coordinates\"=%s, \"creationDate\"=%s, \"area\"=%s, \"population\"=%s, \"metersAboveSeaLevel\"=%s, \"climate\"=%s, \"government\"=%s, \"standardOfLiving\"=%s, \"governor\"=%s}",
            id, name, coordinates, creationDate, area, population, metersAboveSeaLevel, climate, government, standardOfLiving, governor
        );
    }

}
