package commands;

import console.Console;
import managers.CommandManager;

/**
 * Команда для вывода справки по доступным командам.
 */
public class Help extends Command {
    /** Консоль для взаимодействия с пользователем. */
    private final Console console;

    /** Менеджер команд. */
    private final CommandManager commandManager;

    /**
     * Конструктор команды.
     *
     * @param console        консоль для взаимодействия с пользователем
     * @param commandManager менеджер команд
     */
    public Help(Console console, CommandManager commandManager) {
        super("help", "вывести справку по доступным командам");
        this.console = console;
        this.commandManager = commandManager;
    }

    /**
     * Выполняет команду вывода справки по доступным командам.
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

        commandManager.getCommands().values().forEach(command -> {
            console.printTable(command.getName(), command.getDescription());
        });
        return true;
    }
}
