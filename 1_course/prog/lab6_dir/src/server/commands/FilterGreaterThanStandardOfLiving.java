package server.commands;

import common.console.Console;
import common.data.City;
import common.data.StandardOfLiving;
import common.packing.Answer;
import server.managers.CollectionManager;

import java.util.Arrays;

/**
 * Команда для вывода элементов, значение поля standardOfLiving которых больше заданного.
 */
public class FilterGreaterThanStandardOfLiving extends Command {
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
    public FilterGreaterThanStandardOfLiving(Console console, CollectionManager collectionManager) {
        super("filter_greater_than_standard_of_living standardOfLiving",
                "вывести элементы, значение поля standardOfLiving которых больше заданного");
        this.console = console;
        this.collectionManager = collectionManager;
    }

    /**
     * Выполняет команду вывода элементов, значение поля standardOfLiving которых больше заданного.
     *
     * @param arguments аргументы команды (ожидается один аргумент — значение standardOfLiving)
     * @return true, если команда выполнена успешно, иначе false
     */
    @Override
    public Answer execute(String arguments) {
        String[] args = arguments.split(" ");

        if (args.length != 1) {
            return new Answer("Неправильное количество аргументов!\nИспользование: '" + getName() + "'", false);
        }

        StandardOfLiving inputStandard;
        try {
            inputStandard = StandardOfLiving.valueOf(args[0].toUpperCase());
        } catch (IllegalArgumentException e) {
            return new Answer("Неверное значение standardOfLiving! Допустимые значения: "
                    + Arrays.toString(StandardOfLiving.values()), false);
        }

        StringBuilder result = new StringBuilder();
        boolean found = false;

        for (City city : collectionManager.getCollection()) {
            if (city.getStandardOfLiving() != null &&
                    city.getStandardOfLiving().compareTo(inputStandard) > 0) {
                result.append(city.toString()).append("\n\n");
                found = true;
            }
        }

        if (!found) {
            return new Answer("Городов с standardOfLiving больше " + inputStandard + " не найдено", true);
        }
        return new Answer("Найденные города:\n" + result.toString().trim(), true);
    }
}
