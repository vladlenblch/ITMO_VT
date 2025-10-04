package client.commands;

import common.packing.Answer;
import common.packing.CommandTypes;
import server.commands.Command;

import java.util.Map;

/**
 * Команда для вывода справки по доступным командам.
 */
public class Help extends Command {

    /**
     * Менеджер команд
     */
    private final Map<CommandTypes, String[]> commands;

    /**
     *
     * @param commands команды
     */
    public Help(Map<CommandTypes, String[]> commands) {
        super("help", "help");
        this.commands = commands;
    }

    /**
     *
     * @param arguments аргумент команды
     * @return возвращает ответ о выполнении команды
     */
    public Answer execute(String arguments) {
        StringBuilder sb = new StringBuilder();
        for(var e: commands.values()){
            sb.append(e[0]).append(" - ").append(e[1]).append("\n");
        }
        return new Answer(sb.toString(), true);
    }
}
