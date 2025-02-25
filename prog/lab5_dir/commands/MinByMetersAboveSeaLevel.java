package commands;

import managers.CollectionManager;
import console.Console;
import data.City;

public class MinByMetersAboveSeaLevel extends Command {
    private final Console console;
    private final CollectionManager collectionManager;

    public MinByMetersAboveSeaLevel(Console console, CollectionManager collectionManager) {
        super("min_by_meters_above_sea_level",
                "вывести любой объект из коллекции, значение поля metersAboveSeaLevel которого является минимальным");
        this.console = console;
        this.collectionManager = collectionManager;
    }

    @Override
    public boolean apply(String[] arguments) {
        if (!arguments[1].isEmpty()) {
            console.println("Неправильное количество аргументов!");
            console.println("Использование: '" + getName() + "'");
            return false;
        }

        if (collectionManager.getCollection().isEmpty()) {
            console.println("Коллекция пуста.");
            return true;
        }

        City minCity = null;
        for (City city : collectionManager.getCollection()) {
            if (minCity == null || city.getMetersAboveSeaLevel() < minCity.getMetersAboveSeaLevel()) {
                minCity = city;
            }
        }

        if (minCity != null) {
            console.println("Элемент с минимальным значением metersAboveSeaLevel:");
            console.println(minCity.toString());
        } else {
            console.println("Не удалось найти элемент с минимальным metersAboveSeaLevel.");
        }

        return true;
    }
}
