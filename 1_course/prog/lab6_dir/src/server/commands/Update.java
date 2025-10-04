package server.commands;

import common.console.Console;
import common.data.City;
import common.packing.Answer;
import server.managers.CollectionManager;

/**
 * Команда для обновления значения элемента коллекции по ID.
 */
public class Update extends Command {
    /** Консоль для взаимодействия с пользователем. */
    private final Console console;

    /** Менеджер коллекции, в которой производится поиск. */
    private final CollectionManager collectionManager;

    /**
     * Конструктор команды.
     *
     * @param console           консоль для взаимодействия с пользователем
     * @param collectionManager менеджер коллекции
     */
    public Update(Console console, CollectionManager collectionManager) {
        super("update <ID> {element}", "обновить значение элемента коллекции по ID");
        this.console = console;
        this.collectionManager = collectionManager;
    }

    /**
     * Выполняет команду обновления значения элемента коллекции по ID.
     *
     * @param arguments аргументы команды (ожидается один аргумент — значение ID)
     * @return true, если команда выполнена успешно, иначе false
     */
    @Override
    public Answer execute(String arguments) {
        if (arguments.isEmpty()) {
            return new Answer("Перепроверьте аргумент", false);
        }

        String[] parts = arguments.split("/");
        City city = City.fromArray(parts);

        if (collectionManager.byId(city.getId()) == null) {
            return new Answer("Элемент с заданным ID не найден", false);
        }

        collectionManager.remove(city.getId());
        if (collectionManager.add(city)) {
            collectionManager.update();
            return new Answer("Город успешно обновлен", true);
        }

        return new Answer("Произошла непредвиденная ошибка", false);
    }
}
