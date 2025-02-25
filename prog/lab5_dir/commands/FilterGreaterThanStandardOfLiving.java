package commands;

import managers.CollectionManager;
import console.Console;
import data.City;
import data.StandardOfLiving;

import java.util.Arrays;

public class FilterGreaterThanStandardOfLiving extends Command {
    private final Console console;
    private final CollectionManager collectionManager;

    public FilterGreaterThanStandardOfLiving(Console console, CollectionManager collectionManager) {
        super("filter_greater_than_standard_of_living standardOfLiving",
                "вывести элементы, значение поля standardOfLiving которых больше заданного");
        this.console = console;
        this.collectionManager = collectionManager;
    }

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
