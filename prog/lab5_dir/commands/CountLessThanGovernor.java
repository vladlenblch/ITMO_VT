package commands;

import managers.CollectionManager;
import console.Console;
import data.City;
import data.Human;

public class CountLessThanGovernor extends Command {
    private final Console console;
    private final CollectionManager collectionManager;

    public CountLessThanGovernor(Console console, CollectionManager collectionManager) {
        super("count_less_than_governor height",
                "вывести количество элементов, значение поля height объекта governor которых меньше заданного");
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

        double inputHeight;
        try {
            inputHeight = Double.parseDouble(arguments[1]);
        } catch (NumberFormatException e) {
            console.println("Неверный формат height! Ожидается число.");
            return false;
        }

        int count = 0;
        for (City city : collectionManager.getCollection()) {
            Human governor = city.getGovernor();
            if (governor != null && governor.getHeight() < inputHeight) {
                count++;
            }
        }

        console.println("Количество элементов, у которых height governor меньше " + inputHeight + ": " + count);
        return true;
    }
}
