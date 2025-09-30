package commands;

import managers.CollectionManager;
import console.Console;
import data.City;
import data.Human;

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
    public boolean apply(String[] arguments) {
        if (arguments.length < 2) {
            console.println("Неправильное количество аргументов!");
            console.println("Использование: '" + getName() + "'");
            return false;
        }

        long inputHeight;
        try {
            inputHeight = Long.parseLong(arguments[1]);
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