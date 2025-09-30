package commands;

import console.Console;

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
     * @param arguments аргументы команды (ожидается один аргумент — имя файла)
     * @return true, если команда выполнена успешно, иначе false
     */
    @Override
    public boolean apply(String[] arguments) {
        if (arguments[1].isEmpty()) {
            console.println("Неправильное количество аргументов!");
            console.println("Использование: '" + getName() + "'");
            return false;
        }

        console.println("Выполнение скрипта '" + arguments[1] + "'...");
        return true;
    }
}