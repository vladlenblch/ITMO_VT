package enums;

public enum location {
    MOUNTAINS("горы"),
    SNOW("сугробы"),
    OLDCAR("сани"),
    ROAD("тропа");

    private final String description;

    location(String description) {
        this.description = description;
    }

    public String getDescription() {
        return description;
    }
}
