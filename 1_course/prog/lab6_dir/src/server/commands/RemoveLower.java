package server.commands;

import common.console.Console;
import common.data.City;
import common.packing.Answer;
import server.managers.CollectionManager;

/**
 * Команда для удаления из коллекции всех элементов, у которых значение поля population меньше заданного.
 */
public class RemoveLower extends Command {
    /** Консоль для взаимодействия с пользователем. */
    private final Console console;

    /** Менеджер коллекции, из которой удаляются элементы. */
    private final CollectionManager collectionManager;

    /**
     * Конструктор команды.
     *
     * @param console           консоль для взаимодействия с пользователем
     * @param collectionManager менеджер коллекции
     */
    public RemoveLower(Console console, CollectionManager collectionManager) {
        super("remove_lower {element}", "удалить из коллекции все элементы, меньшие чем заданный (по population)");
        this.console = console;
        this.collectionManager = collectionManager;
    }

    /**
     * Выполняет команду удаления элементов, у которых значение поля population меньше заданного.
     *
     * @param arguments аргументы команды (ожидается один аргумент — значение population)
     * @return true, если команда выполнена успешно, иначе false
     */
    @Override
    public Answer execute(String arguments) {
        String[] args = arguments.split(" ");
        if (args.length != 1 || args[0].isEmpty()) {
            return new Answer("Неправильное количество аргументов!\nИспользование: '" + getName() + "'", false);
        }

        int population;
        try {
            population = Integer.parseInt(args[0]);
        } catch (NumberFormatException e) {
            return new Answer("Неверный формат population! Ожидается целое число.", false);
        }

        boolean isFirst = true;
        int removedCount = 0;
        var iterator = collectionManager.getCollection().iterator();

        while (iterator.hasNext()) {
            City city = iterator.next();
            if (city.getPopulation() != null && city.getPopulation() < population) {
                iterator.remove();
                collectionManager.remove(city.getId());
                isFirst = false;
                removedCount++;
            }
        }

        if (removedCount > 0) {
            return new Answer("Удалено " + removedCount + " элементов с population < " + population, true);
        }
        return new Answer("Элементов с population < " + population + " не найдено", true);
    }
}
