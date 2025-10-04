package server.commands;

import common.console.Console;
import common.packing.Answer;
import server.managers.CollectionManager;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

/**
 * Команда для вывода информации о коллекции.
 */
public class Info extends Command {
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
    public Info(Console console, CollectionManager collectionManager) {
        super("info", "вывести информацию о коллекции");
        this.console = console;
        this.collectionManager = collectionManager;
    }

    /**
     * Выполняет команду вывода информации о коллекции.
     *
     * @param arguments аргументы команды
     * @return true, если команда выполнена успешно, иначе false
     */
    @Override
    public Answer execute(String arguments) {
        if (!arguments.trim().isEmpty()) {
            return new Answer("Неправильное количество аргументов!\nИспользование: '" + getName() + "'", false);
        }

        LocalDateTime lastInitTime = collectionManager.getLastInitTime();
        String lastInitTimeString = (lastInitTime == null)
                ? "в данной сессии инициализации еще не происходило"
                : lastInitTime.format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"));

        LocalDateTime lastSaveTime = collectionManager.getLastSaveTime();
        String lastSaveTimeString = (lastSaveTime == null)
                ? "в данной сессии сохранения еще не происходило"
                : lastSaveTime.format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"));

        String info = String.format(
                "Сведения о коллекции:%n" +
                        " Тип: %s%n" +
                        " Количество элементов: %d%n" +
                        " Дата последнего сохранения: %s%n" +
                        " Дата последней инициализации: %s",
                collectionManager.getCollection().getClass().getName(),
                collectionManager.getCollection().size(),
                lastSaveTimeString,
                lastInitTimeString
        );

        return new Answer(info, true);
    }
}
