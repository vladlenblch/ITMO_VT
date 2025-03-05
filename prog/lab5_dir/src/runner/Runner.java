package runner;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Scanner;

import managers.CollectionManager;
import managers.CommandManager;
import console.Console;

/**
 * Класс, отвечающий за запуск и управление интерактивным и скриптовым режимами работы программы.
 */
public class Runner {

    /**
     * Перечисление, представляющее возможные коды завершения выполнения команды.
     */
    public enum ExitCode {
        /** Успешное выполнение команды. */
        OK,
        /** Ошибка при выполнении команды. */
        ERROR,
        /** Завершение работы программы. */
        EXIT
    }

    /** Консоль для взаимодействия с пользователем. */
    private Console console;

    /** Менеджер команд. */
    private final CommandManager commandManager;

    /** Стек для хранения путей к выполняемым скриптам (для предотвращения рекурсии). */
    private final List<String> scriptStack = new ArrayList<>();

    /** Максимальная глубина рекурсии при выполнении скриптов. */
    private int lengthRecursion = -1;

    /** Менеджер коллекции, используемый для управления данными. */
    private final CollectionManager collectionManager;

    /**
     * Конструктор класса.
     *
     * @param console           консоль для взаимодействия с пользователем
     * @param commandManager    менеджер команд
     * @param collectionManager менеджер коллекции
     */
    public Runner(Console console, CommandManager commandManager, CollectionManager collectionManager) {
        this.console = console;
        this.commandManager = commandManager;
        this.collectionManager = collectionManager;
    }

    /**
     * Запускает интерактивный режим работы программы.
     * В этом режиме программа ожидает ввода команд от пользователя и выполняет их.
     */
    public void interactiveMode() {
        collectionManager.init();
        try {
            ExitCode commandStatus;
            String[] userCommand = {"", ""};

            do {
                console.prompt();
                userCommand = (console.readln().trim() + " ").split(" ", 2);
                userCommand[1] = userCommand[1].trim();

                commandManager.addToHistory(userCommand[0]);
                commandStatus = launchCommand(userCommand);
            } while (commandStatus != ExitCode.EXIT);

        } catch (NoSuchElementException exception) {
            console.printError("Пользовательский ввод не обнаружен!");
        } catch (IllegalStateException exception) {
            console.printError("Непредвиденная ошибка!");
        }
    }

    /**
     * Запускает выполнение скрипта из указанного файла.
     *
     * @param argument путь к файлу со скриптом
     * @return код завершения выполнения скрипта
     */
    public ExitCode scriptMode(String argument) {
        String[] userCommand = {"", ""};
        ExitCode commandStatus;
        scriptStack.add(argument);

        if (!new File(argument).exists()) {
            console.printError("Файл не существует!");
            return ExitCode.ERROR;
        }
        if (!Files.isReadable(Paths.get(argument))) {
            console.printError("Прав для чтения нет!");
            return ExitCode.ERROR;
        }

        try (FileReader fileReader = new FileReader(argument);
             BufferedReader bufferedReader = new BufferedReader(fileReader);
             Scanner scriptScanner = new Scanner(bufferedReader)) {

            if (!scriptScanner.hasNext()) throw new NoSuchElementException();
            console.selectFileScanner(scriptScanner);

            do {
                userCommand = (console.readln().trim() + " ").split(" ", 2);
                userCommand[1] = userCommand[1].trim();

                while (console.canReadln() && userCommand[0].isEmpty()) {
                    userCommand = (console.readln().trim() + " ").split(" ", 2);
                    userCommand[1] = userCommand[1].trim();
                }

                console.println(console.getPrompt() + String.join(" ", userCommand));
                var needLaunch = true;

                if (userCommand[0].equals("execute_script")) {
                    var recStart = -1;
                    var i = 0;
                    for (String script : scriptStack) {
                        i++;
                        if (userCommand[1].equals(script)) {
                            if (recStart < 0) recStart = i;
                            if (lengthRecursion < 0) {
                                console.selectConsoleScanner();
                                console.println("Была замечена рекурсия! Введите максимальную глубину рекурсии (0-500)");
                                while (lengthRecursion < 0 || lengthRecursion > 500) {
                                    try {
                                        console.print("> ");
                                        lengthRecursion = Integer.parseInt(console.readln().trim());
                                    } catch (NumberFormatException e) {
                                        console.println("Длина не распознана");
                                    }
                                }
                                console.selectFileScanner(scriptScanner);
                            }
                            if (i > recStart + lengthRecursion || i > 500)
                                needLaunch = false;
                        }
                    }
                }

                commandStatus = needLaunch ? launchCommand(userCommand) : ExitCode.OK;
            } while (commandStatus == ExitCode.OK && console.canReadln());

            console.selectConsoleScanner();
            if (commandStatus == ExitCode.ERROR && !(userCommand[0].equals("execute_script") && !userCommand[1].isEmpty())) {
                console.println("Проверьте скрипт на корректность введенных данных!");
            }

            return commandStatus;
        } catch (FileNotFoundException exception) {
            console.printError("Файл со скриптом не найден!");
        } catch (NoSuchElementException exception) {
            console.printError("Файл со скриптом пуст!");
        } catch (IOException exception) {
            console.printError("Ошибка чтения файла со скриптом!");
        } catch (IllegalStateException exception) {
            console.printError("Непредвиденная ошибка!");
            System.exit(0);
        } finally {
            scriptStack.remove(scriptStack.size() - 1);
        }
        return ExitCode.ERROR;
    }

    /**
     * Выполняет команду.
     *
     * @param userCommand массив, содержащий команду и её аргументы
     * @return код завершения выполнения команды
     */
    private ExitCode launchCommand(String[] userCommand) {
        if (userCommand[0].isEmpty()) return ExitCode.OK;

        var command = commandManager.getCommands().get(userCommand[0]);

        if (command == null) {
            console.printError("Команда '" + userCommand[0] + "' не найдена. Наберите 'help' для справки");
            return ExitCode.ERROR;
        }

        switch (userCommand[0]) {
            case "exit" -> {
                if (!commandManager.getCommands().get("exit").apply(userCommand)) return ExitCode.ERROR;
                else return ExitCode.EXIT;
            }
            case "execute_script" -> {
                if (!commandManager.getCommands().get("execute_script").apply(userCommand)) return ExitCode.ERROR;
                else return scriptMode(userCommand[1]);
            }
            default -> {
                if (!command.apply(userCommand)) return ExitCode.ERROR;
            }
        }

        return ExitCode.OK;
    }
}