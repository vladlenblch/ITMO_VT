package server.commands;

import common.console.Console;
import common.data.City;
import common.packing.Answer;
import server.managers.CollectionManager;

import java.util.Comparator;

/**
 * Команда для вывода любого объекта коллекции, значение поля metersAboveSeaLevel которого является минимальным.
 */
public class MinByMetersAboveSeaLevel extends Command {
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
    public MinByMetersAboveSeaLevel(Console console, CollectionManager collectionManager) {
        super("min_by_meters_above_sea_level",
                "вывести любой объект из коллекции, значение поля metersAboveSeaLevel которого является минимальным");
        this.console = console;
        this.collectionManager = collectionManager;
    }

    /**
     * Выполняет команду вывода любого объекта коллекции, значение поля metersAboveSeaLevel которого является минимальным.
     *
     * @param arguments аргументы команды (ожидается один аргумент — значение metersAboveSeaLevel)
     * @return true, если команда выполнена успешно, иначе false
     */
    @Override
    public Answer execute(String arguments) {
        if (!arguments.isEmpty()) {
            return new Answer("Неправильное количество аргументов!\nИспользование: '" + getName() + "'", false);
        }

        if (collectionManager.getCollection().isEmpty()) {
            return new Answer("Коллекция пуста", true);
        }

        City minCity = collectionManager.getCollection().stream()
                .min(Comparator.comparingInt(City::getMetersAboveSeaLevel))
                .orElse(null);

        if (minCity != null) {
            return new Answer(
                    "Элемент с минимальным значением metersAboveSeaLevel:\n" + minCity.toString(),
                    true
            );
        }
        return new Answer("Не удалось найти элемент с минимальным metersAboveSeaLevel", false);
    }
}
