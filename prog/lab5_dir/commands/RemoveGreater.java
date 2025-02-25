package commands;

import managers.CollectionManager;
import console.Console;
import data.City;

public class RemoveGreater extends Command {
    private final Console console;
    private final CollectionManager collectionManager;

    public RemoveGreater(Console console, CollectionManager collectionManager) {
        super("remove_greater {element}", "удалить из коллекции все элементы, превышающие заданный (по population)");
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

        int inputPopulation;
        try {
            inputPopulation = Integer.parseInt(arguments[1]);
        } catch (NumberFormatException e) {
            console.println("Неверный формат population! Ожидается целое число.");
            return false;
        }

        var isFirst = true;
        var iterator = collectionManager.getCollection().iterator();
        while (iterator.hasNext()) {
            City city = iterator.next();
            if (city.getPopulation() > inputPopulation) {
                iterator.remove();
                collectionManager.remove(city.getId());
                collectionManager.addLog("remove " + city.getId(), isFirst);
                isFirst = false;
            }
        }

        console.println("Элементы, у которых population превышает " + inputPopulation + ", удалены.");
        return true;
    }
}
