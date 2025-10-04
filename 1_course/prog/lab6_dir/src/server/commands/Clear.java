package server.commands;

import common.console.Console;
import common.data.City;
import common.packing.Answer;
import server.managers.CollectionManager;

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
     * Выполняет команду очистки коллекции городов.
     *
     * @param arguments аргументы команды (должны быть пустыми)
     * @return ответ с результатом выполнения операции
     */
    @Override
    public Answer execute(String arguments) {
        if (!arguments.isEmpty()) {
            return new Answer("Неправильное количество аргументов!\nИспользование: '" + getName() + "'", false);
        }

        Set<City> copy = new LinkedHashSet<>(collectionManager.getCollection());

        for (City city : copy) {
            collectionManager.remove(city.getId());
        }

        boolean isFirst = true;
        for (City city : copy) {
            isFirst = false;
        }

        collectionManager.update();

        return new Answer("Коллекция успешно очищена. Удалено элементов: " + copy.size(), true);
    }
}