package server.commands;

import common.console.Console;
import common.packing.Answer;
import server.managers.CommandManager;

import java.util.List;

/**
 * Команда для вывода истории последних 12 команд.
 */
public class History extends Command {
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
    public History(Console console, CommandManager commandManager) {
        super("history", "выводит историю последних 12 команд");
        this.console = console;
        this.commandManager = commandManager;
    }

    /**
     * Выполняет команду вывода истории последних 12 команд.
     *
     * @param arguments аргументы команды
     * @return true, если команда выполнена успешно, иначе false
     */
    @Override
    public Answer execute(String arguments) {
        if (!arguments.isEmpty()) {
            return new Answer("Неправильное количество аргументов!\nИспользование: '" + getName() + "'", false);
        }

        List<String> commandHistory = commandManager.getCommandHistory();

        if (commandHistory.isEmpty()) {
            return new Answer("История команд пуста", true);
        } else {
            int limit = 12;
            int startIndex = Math.max(0, commandHistory.size() - limit);
            List<String> lastCommands = commandHistory.subList(startIndex, commandHistory.size());

            StringBuilder result = new StringBuilder("Последние выполненные команды:\n");
            for (String cmd : lastCommands) {
                result.append(" - ").append(cmd).append("\n");
            }

            return new Answer(result.toString().trim(), true);
        }
    }
}
