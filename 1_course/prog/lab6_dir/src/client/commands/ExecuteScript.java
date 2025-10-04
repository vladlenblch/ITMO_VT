package client.commands;

import common.console.Console;
import common.packing.Answer;
import server.commands.Command;

/**
 * Команда для выполнения скрипта из указанного файла.
 */
public class ExecuteScript extends Command {
    /** Консоль для взаимодействия с пользователем. */
    private final Console console;

    /**
     * Конструктор команды.
     *
     * @param console консоль для взаимодействия с пользователем
     */
    public ExecuteScript(Console console) {
        super("execute_script <file_name>", "исполнить скрипт из указанного файла");
        this.console = console;
    }

    /**
     * Выполняет команду выполнения скрипта.
     *
     * @param arguments аргумент
     * @return возвращает ответ о выполнении команды
     */
    public Answer execute(String arguments) {
        if (arguments.isEmpty()) return new Answer("Неправильное количество аргументов!\nИспользование: '" + getName() + "'", false);

        return new Answer("Выполнение скрипта '" + arguments + "'...", true);
    }
}
