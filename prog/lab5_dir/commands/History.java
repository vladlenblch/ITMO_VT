package commands;

import managers.CommandManager;
import console.Console;

import java.util.List;

public class History extends Command {
    private final Console console;
    private final CommandManager commandManager;

    public History(Console console, CommandManager commandManager) {
        super("history", "выводит историю последних 12 команд");
        this.console = console;
        this.commandManager = commandManager;
    }

    @Override
    public boolean apply(String[] arguments) {
        if (!arguments[1].isEmpty()) {
            console.println("Неправильное количество аргументов!");
            console.println("Использование: '" + getName() + "'");
            return false;
        }

        List<String> commandHistory = commandManager.getCommandHistory();

        if (commandHistory.isEmpty()) {
            console.println("История команд пуста.");
        } else {
            int startIndex = Math.max(0, commandHistory.size() - 12);

            List<String> last12Commands = commandHistory.subList(startIndex, commandHistory.size());

            console.println("Последние выполненные команды:");
            last12Commands.forEach(command -> console.println(" " + command));
        }

        return true;
    }
}
