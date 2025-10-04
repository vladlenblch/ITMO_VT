package server.managers;

import server.commands.Command;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Класс, отвечающий за управление командами.
 * Регистрирует команды, предоставляет доступ к ним и хранит историю выполненных команд.
 */
public class CommandManager {
    /** Коллекция зарегистрированных команд, где ключ — имя команды, а значение — сама команда. */
    private final Map<String, Command> commands = new LinkedHashMap<>();

    /** Список для хранения истории выполненных команд. */
    private final List<String> commandHistory = new ArrayList<>();

    /**
     * Регистрирует команду.
     *
     * @param commandName имя команды
     * @param command     объект команды
     */
    public void register(String commandName, Command command) {
        commands.put(commandName, command);
    }

    /**
     * Возвращает коллекцию зарегистрированных команд.
     *
     * @return коллекция команд
     */
    public Map<String, Command> getCommands() {
        return commands;
    }

    /**
     * Возвращает историю выполненных команд.
     *
     * @return список выполненных команд
     */
    public List<String> getCommandHistory() {
        return commandHistory;
    }

    /**
     * Добавляет команду в историю выполненных команд.
     *
     * @param command команда для добавления в историю
     */
    public void addToHistory(String command) {
        commandHistory.add(command);
    }
}