package client.commands;

/**
 * Абстрактный класс, представляющий команду.
 * Содержит имя, описание и метод для выполнения команды.
 */
public abstract class Command implements Executable {
    /** Имя команды. */
    private final String name;

    /** Описание команды. */
    private final String description;

    /**
     * Конструктор команды.
     *
     * @param name        имя команды
     * @param description описание команды
     */
    public Command(String name, String description) {
        this.name = name;
        this.description = description;
    }

    /**
     * Возвращает имя команды.
     *
     * @return имя команды
     */
    public String getName() {
        return name;
    }

    /**
     * Возвращает описание команды.
     *
     * @return описание команды
     */
    public String getDescription() {
        return description;
    }

    /**
     * Сравнивает команды по имени и описанию.
     *
     * @param obj объект для сравнения
     * @return true, если команды равны, иначе false
     */
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        Command command = (Command) obj;
        return name.equals(command.name) && description.equals(command.description);
    }

    /**
     * Возвращает хэш-код команды.
     *
     * @return хэш-код команды
     */
    @Override
    public int hashCode() {
        return name.hashCode() + description.hashCode();
    }

    /**
     * Возвращает строковое представление команды.
     *
     * @return строковое представление команды
     */
    @Override
    public String toString() {
        return "Command{" +
                "name='" + name + '\'' +
                ", description='" + description + '\'' +
                '}';
    }
}
