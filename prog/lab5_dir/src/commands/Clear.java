package commands;

import managers.CollectionManager;
import console.Console;
import data.City;

import java.util.LinkedHashSet;
import java.util.Set;

/**
 * Команда для очистки коллекции.
 */
public class Clear extends Command {
    /** Консоль для взаимодействия с пользователем. */
    private final Console console;

    /** Менеджер коллекции, которая будет очищена. */
    private final CollectionManager collectionManager;

    /**
     * Конструктор команды.
     *
     * @param console           консоль для взаимодействия с пользователем
     * @param collectionManager менеджер коллекции
     */
    public Clear(Console console, CollectionManager collectionManager) {
        super("clear", "очистить коллекцию");
        this.console = console;
        this.collectionManager = collectionManager;
    }

    /**
     * Выполняет команду очистки коллекции.
     *
     * @param arguments аргументы команды
     * @return true, если команда выполнена успешно, иначе false
     */
    @Override
    public boolean apply(String[] arguments) {
        if (!arguments[1].isEmpty()) {
            console.println("Неправильное количество аргументов!");
            console.println("Использование: '" + getName() + "'");
            return false;
        }

        Set<City> copy = new LinkedHashSet<>(collectionManager.getCollection());

        for (City city : copy) {
            collectionManager.remove(city.getId());
        }

        collectionManager.getCollection().clear();

        var isFirst = true;
        for (City city : copy) {
            collectionManager.addLog("remove " + city.getId(), isFirst);
            isFirst = false;
        }

        console.println("Коллекция очищена!");
        return true;
    }
}