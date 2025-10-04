package server.commands;

import common.console.Console;
import common.packing.Answer;
import server.managers.CollectionManager;

/**
 * Команда для завершения работы программы.
 */
public class Exit extends Command {
    /** Консоль для взаимодействия с пользователем. */
    private final Console console;

    private CollectionManager collectionManager;

    /**
     * Конструктор команды.
     *
     * @param console           консоль для взаимодействия с пользователем
     */
    public Exit(Console console, CollectionManager collectionManager) {
        super("exit", "завершить программу (без сохранения в файл)");
        this.console = console;
        this.collectionManager = collectionManager;
    }

    /**
     * Выполняет команду завершения работы программы.
     *
     * @param arguments аргументы команды (должны быть пустыми)
     * @return ответ с результатом выполнения операции
     */
    @Override
    public Answer execute(String arguments) {
        if (!arguments.isEmpty()) {
            return new Answer("Неправильное количество аргументов!\nИспользование: '" + getName() + "'", false);
        }

        Answer saveResult = collectionManager.saveCollection();
        if (!saveResult.code()) {
            return new Answer("Ошибка сохранения: " + saveResult.message(), false);
        }

        return new Answer("exit", true);
    }
}
