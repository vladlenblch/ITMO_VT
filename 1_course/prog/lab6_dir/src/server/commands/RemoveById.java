package server.commands;

import common.console.Console;
import common.packing.Answer;
import server.managers.CollectionManager;

/**
 * Команда для удаления элемента из коллекции по ID.
 */
public class RemoveById extends Command {
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
    public RemoveById(Console console, CollectionManager collectionManager) {
        super("remove_by_id <ID>", "удалить элемент из коллекции по ID");
        this.console = console;
        this.collectionManager = collectionManager;
    }

    /**
     * Выполняет команду удаления элемента из коллекции по ID.
     *
     * @param arguments аргументы команды (ожидается один аргумент — значение ID)
     * @return true, если команда выполнена успешно, иначе false
     */
    @Override
    public Answer execute(String arguments) {
        String[] args = arguments.split(" ");
        if (args.length != 1 || args[0].isEmpty()) {
            return new Answer("Неправильное количество аргументов!\nИспользование: '" + getName() + "'", false);
        }

        int id;
        try {
            id = Integer.parseInt(args[0].trim());
        } catch (NumberFormatException e) {
            return new Answer("ID должен быть целым числом", false);
        }

        if (collectionManager.byId(id) == null) {
            return new Answer("Элемент с ID " + id + " не найден", false);
        }

        collectionManager.remove(id);
        collectionManager.update();

        return new Answer("Элемент с ID " + id + " успешно удален", true);
    }
}
