package server.commands;

import common.console.Console;
import common.data.City;
import common.packing.Answer;
import server.managers.CollectionManager;

/**
 * Команда для добавления нового элемента в коллекцию.
 */
public class Add extends Command {
    /** Консоль для взаимодействия с пользователем. */
    private final Console console;

    /** Менеджер коллекции, в которую добавляется элемент. */
    private final CollectionManager collectionManager;

    /**
     * Конструктор команды.
     *
     * @param console           консоль для взаимодействия с пользователем
     * @param collectionManager менеджер коллекции
     */
    public Add(Console console, CollectionManager collectionManager) {
        super("add {element}", "добавить новый элемент в коллекцию");
        this.console = console;
        this.collectionManager = collectionManager;
    }

    /**
     * Выполняет команду добавления нового города в коллекцию.
     *
     * @param arguments строка с данными города в формате "id/name/coordinates/..."
     * @return ответ с результатом выполнения операции
     */
    @Override
    public Answer execute(String arguments) {
        try {
            City city = City.fromArray(arguments.split("/"));
            if (city == null || !city.validate()) {
                return new Answer("Поля города не валидны!", false);
            }
            city.setId(collectionManager.getFreeId());
            if (collectionManager.add(city)) {
                return new Answer("Город успешно добавлен с ID " + city.getId(), true);
            }
            return new Answer("Ошибка при добавлении города", false);
        } catch (Exception e) {
            return new Answer("Ошибка: " + e.getMessage(), false);
        }
    }
}