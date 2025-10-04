package server.commands;

import common.console.Console;
import common.packing.Answer;
import server.managers.CollectionManager;

/**
 * Команда для вывода всех элементов коллекции в строковом представлении.
 */
public class Show extends Command {
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
    public Show(Console console, CollectionManager collectionManager) {
        super("show", "вывести в стандартный поток вывода все элементы коллекции в строковом представлении");
        this.console = console;
        this.collectionManager = collectionManager;
    }

    /**
     * Выполняет команду вывода всех элементов коллекции в строковом представлении.
     *
     * @param arguments аргументы команды
     * @return true, если команда выполнена успешно, иначе false
     */
    @Override
    public Answer execute(String arguments) {
        if (!arguments.trim().isEmpty()) {
            return new Answer("Неправильное количество аргументов!\nИспользование: '" + getName() + "'", false);
        }

        var collection = collectionManager.getCollection();
        if (collection.isEmpty()) {
            return new Answer("Коллекция пуста!", true);
        }

        StringBuilder sb = new StringBuilder();
        for (var city : collection) {
            sb.append(city.toString()).append("\n\n");
        }

        return new Answer(sb.toString().trim(), true);
    }
}
