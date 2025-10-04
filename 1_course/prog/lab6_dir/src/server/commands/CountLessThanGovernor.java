package server.commands;

import common.console.Console;
import common.data.City;
import common.data.Human;
import common.packing.Answer;
import server.managers.CollectionManager;

/**
 * Команда для подсчёта количества элементов, у которых значение поля height объекта governor меньше заданного.
 */
public class CountLessThanGovernor extends Command {
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
    public CountLessThanGovernor(Console console, CollectionManager collectionManager) {
        super("count_less_than_governor height",
                "вывести количество элементов, значение поля height объекта governor которых меньше заданного");
        this.console = console;
        this.collectionManager = collectionManager;
    }

    /**
     * Выполняет команду подсчёта количества элементов, у которых значение поля height объекта governor меньше заданного.
     *
     * @param arguments аргументы команды (ожидается один аргумент — значение height)
     * @return true, если команда выполнена успешно, иначе false
     */
    @Override
    public Answer execute(String arguments) {
        String[] args = arguments.split(" ");

        if (args.length != 1) {
            return new Answer("Неправильное количество аргументов!\nИспользование: '" + getName() + " <height>'", false);
        }

        long inputHeight;
        try {
            inputHeight = Long.parseLong(args[0]);
        } catch (NumberFormatException e) {
            return new Answer("Неверный формат height! Ожидается целое число.", false);
        }

        int count = 0;
        for (City city : collectionManager.getCollection()) {
            Human governor = city.getGovernor();
            if (governor != null && governor.getHeight() < inputHeight) {
                count++;
            }
        }

        return new Answer("Количество городов, где рост губернатора меньше " + inputHeight + ": " + count, true);
    }
}