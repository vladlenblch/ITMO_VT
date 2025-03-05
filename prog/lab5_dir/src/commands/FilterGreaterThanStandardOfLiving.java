package commands;

import managers.CollectionManager;
import console.Console;
import data.City;
import data.StandardOfLiving;

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
    public boolean apply(String[] arguments) {
        if (arguments.length < 2) {
            console.println("Неправильное количество аргументов!");
            console.println("Использование: '" + getName() + "'");
            return false;
        }

        StandardOfLiving inputStandardOfLiving;
        try {
            inputStandardOfLiving = StandardOfLiving.valueOf(arguments[1].toUpperCase());
        } catch (IllegalArgumentException e) {
            console.println("Неверный формат standardOfLiving! Допустимые значения: " + Arrays.toString(StandardOfLiving.values()));
            return false;
        }

        boolean found = false;
        for (City city : collectionManager.getCollection()) {
            if (city.getStandardOfLiving() != null && city.getStandardOfLiving().ordinal() < inputStandardOfLiving.ordinal()) {
                console.println(city.toString());
                found = true;
            }
        }

        if (!found) {
            console.println("Элементы, у которых standardOfLiving больше " + inputStandardOfLiving + ", не найдены.");
        }

        return true;
    }
}
