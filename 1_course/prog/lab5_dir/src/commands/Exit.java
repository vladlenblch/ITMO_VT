package commands;

import console.Console;

/**
 * Команда для завершения работы программы.
 */
public class Exit extends Command {
    /** Консоль для взаимодействия с пользователем. */
    private final Console console;

    /**
     * Конструктор команды.
     *
     * @param console           консоль для взаимодействия с пользователем
     */
    public Exit(Console console) {
        super("exit", "завершить программу (без сохранения в файл)");
        this.console = console;
    }

    /**
     * Выполняет команду завершения работы программы.
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

        console.println("Завершение выполнения...");
        return true;
    }
}
