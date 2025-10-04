package client;

import client.ask.Ask;
import client.commands.ExecuteScript;
import client.commands.Help;
import client.connector.ClientConnector;
import common.console.Console;
import common.data.City;
import common.data.StandardOfLiving;
import common.packing.Answer;
import common.packing.CommandTypes;
import common.packing.Container;
import server.managers.CollectionManager;

import java.io.File;
import java.io.FileNotFoundException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;

/**
 * Основной класс клиентского приложения, обеспечивающий взаимодействие с сервером.
 * Обрабатывает пользовательский ввод, выполняет команды и управляет сетевым соединением.
 * Поддерживает два режима работы: интерактивный и скриптовый.
 */
public class Client {
    /**
     * Сетевой коннектор для обмена данными с сервером по протоколу UDP
     */
    private final ClientConnector connector;

    /**
     * Интерфейс для ввода/вывода данных
     */
    private final Console console;

    /**
     * Карта доступных команд и их описаний (команда -> описание)
     */
    private final Map<CommandTypes, String[]> commands;

    /**
     * Стек выполняемых скриптов для контроля рекурсивных вызовов
     */
    private final List<String> scriptStack = new ArrayList<>();

    /**
     * Максимальная допустимая глубина рекурсии при выполнении скриптов
     */
    private int lengthRecursion = -1;


    private final CollectionManager collectionManager;

    /**
     * Создает новый клиентский объект
     * @param console консоль для ввода/вывода
     * @param commands карта доступных команд
     */
    public Client(Console console, Map<CommandTypes, String[]> commands, CollectionManager collectionManager) {
        this.connector = new ClientConnector("localhost", 6789, console);
        this.console = console;
        this.commands = commands;
        this.collectionManager = collectionManager;
    }

    /**
     * Устанавливает соединение с сервером с автоматическими повторными попытками
     * @throws IllegalStateException если подключение не удалось после всех попыток
     */
    public void start(){
        Answer initAnswer = new Answer("", false);
        connector.init();
        initAnswer = connector.send(new Container(new Answer(connector.getAddress().toString(), true)));
        while(!initAnswer.code()){
            connector.init();
            initAnswer = connector.send( new Container(new Answer(connector.getAddress().toString(), true)));
            console.println(initAnswer.message());
            if (!initAnswer.code()) {
                console.println("Попытка повторного подключения через 10 секунд");
                try {
                    Thread.sleep(10000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
            else{
                break;
            }
        }
    }

    /**
     * Запускает интерактивный режим работы с консолью
     * @throws NoSuchElementException если ввод не обнаружен
     * @throws IllegalStateException при возникновении непредвиденной ошибки
     */
    public void interactiveMode() {
        Answer commandAnswer;
        try {
            start();
            while (true) {
                console.prompt();
                String[] userCommand = (console.readln().trim() + " ").split(" ");
                if (userCommand.length > 2) {
                    console.printError("Перепроверьте кол-во аргументов");
                    continue;
                }
                if (userCommand.length == 2) userCommand[1] = userCommand[1].trim();
                if (userCommand.length == 0) userCommand = new String[]{""};

                commandAnswer = launchCommand(userCommand);

                if (commandAnswer.message().equals("exit") && commandAnswer.code()) {
                    console.println("Завершение работы клиента...");
                    System.exit(0);
                }

                if (commandAnswer.code()) {
                    console.println(commandAnswer.message());
                } else {
                    console.printError(commandAnswer.message());
                    if (commandAnswer.message().equals("Сервер временно недоступен")) {
                        start();
                    }
                }
            }
        } catch (NoSuchElementException exception) {
            console.printError("Пользовательский ввод не обнаружен!");
        } catch (IllegalStateException exception) {
            console.printError("Непредвиденная ошибка!");
        }
    }

    /**
     * Проверяет наличие рекурсивного вызова скриптов
     * @param argument имя проверяемого скрипта
     * @param scriptScanner сканер текущего скрипта
     * @return true если рекурсия допустима, false если превышена максимальная глубина
     */
    private boolean checkRecursion(String argument, Scanner scriptScanner) {
        int recStart = -1;
        int i = 0;
        for (String script : scriptStack) {
            i++;
            if (argument.equals(script)) {
                if (recStart < 0) recStart = i;
                if (lengthRecursion < 0) {
                    console.selectConsoleScanner();
                    console.println("Обнаружена рекурсия! Введите максимальную глубину рекурсии (0..500)");
                    while (lengthRecursion < 0 || lengthRecursion > 500) {
                        try {
                            console.print("> ");
                            lengthRecursion = Integer.parseInt(console.readln().trim());
                            if (lengthRecursion < 0 || lengthRecursion > 500) {
                                console.println("Некорректное значение");
                            }
                        } catch (NumberFormatException e) {
                            console.println("Некорректное значение");
                        }
                    }
                    console.selectFileScanner(scriptScanner);
                }
                if (i > recStart + lengthRecursion || i > 500)
                    return false;
            }
        }
        return true;
    }

    /**
     * Выполняет команды из указанного файла скрипта
     * @param argument путь к файлу скрипта
     * @return результат выполнения в виде объекта Answer
     */
    private Answer scriptMode(String argument) {
        String[] userCommand;
        StringBuilder executionOutput = new StringBuilder();
        if (!new File(argument).exists()) return new Answer( "Файл не существует!", false);
        if (!Files.isReadable(Paths.get(argument))) return new Answer ("Прав для чтения нет!", false );

        scriptStack.add(argument);
        try (Scanner scriptScanner = new Scanner(new File(argument))) {

            Answer commandStatus;

            if (!scriptScanner.hasNext()) throw new NoSuchElementException();
            console.selectFileScanner(scriptScanner);
            do {
                userCommand = (console.readln().trim() + " ").split(" ");
                if (userCommand.length>1) userCommand[1] = userCommand[1].trim();
                while (console.canReadln() && userCommand[0].isEmpty()) {
                    userCommand = (console.readln().trim() + " ").split(" ", 2);
                    if (userCommand.length>1) userCommand[1] = userCommand[1].trim();
                }
                executionOutput.append(console.getPrompt()).append(String.join(" ", userCommand)).append("\n");
                var needLaunch = true;
                if (userCommand[0].equals("execute_script")) {
                    needLaunch = checkRecursion(userCommand[1], scriptScanner);
                }
                commandStatus = needLaunch ? launchCommand(userCommand) : new Answer("Превышена максимальная глубина рекурсии", false);
                if (userCommand[0].equals("execute_script")) console.selectFileScanner(scriptScanner);
                executionOutput.append(commandStatus.message()).append("\n");
            } while (commandStatus.code() && !commandStatus.message().equals("exit") && console.canReadln());

            console.selectConsoleScanner();
            if (!commandStatus.code() && !(userCommand[0].equals("execute_script") && !userCommand[1].isEmpty())) {
                executionOutput.append("Проверьте скрипт на корректность введенных данных!\n");
            }

            return new Answer(executionOutput.toString(), commandStatus.code());
        } catch (FileNotFoundException exception) {
            return new Answer("Файл со скриптом не найден!", false);
        } catch (NoSuchElementException exception) {
            return new Answer("Файл со скриптом пуст!", false );
        } catch (IllegalStateException exception) {
            console.printError("Непредвиденная ошибка!");
            System.exit(0);
        } finally {
            scriptStack.remove(scriptStack.size() - 1);
        }
        return new Answer("Непредвиденная ошибка!", false);
    }

    /**
     * Обрабатывает и выполняет команду
     * @param request массив строк с командой и аргументами
     * @return результат выполнения команды
     */
    private Answer launchCommand(String[] request) {
        String message = "";
        if (request[0].isEmpty()) return new Answer("Команда не распознана", false);
        var command = CommandTypes.getByString(request[0]);
        if (command == null && !request[0].equalsIgnoreCase("execute_script"))
            return new Answer("Команда \"" + request[0] + "\" не найдена. Используйте 'help'", false);
        if (request[0].toLowerCase().equals("execute_script")) {
            Answer tmp = new ExecuteScript(console).execute(request[1]);
            if (!tmp.code()) return tmp;
            Answer tmp2 = scriptMode(request[1]);
            return new Answer(tmp.message() + "\n" + tmp2.message().trim(), true);
        }
        if (command == CommandTypes.Add) {
            try {
                if (request.length > 1 && !request[1].isEmpty()) {
                    return new Answer("Неверное использование команды", false);
                }
                City city = Ask.askCity(console, collectionManager);
                if (city == null) {
                    return new Answer("Создание города отменено", false);
                }
                message = city.toStr();
            } catch (Ask.AskBreak e) {
                return new Answer("Создание города отменено пользователем", false);
            } catch (Exception e) {
                return new Answer("Ошибка при создании города: " + e.getMessage(), false);
            }
        } else if (command == CommandTypes.Update) {
            try {
                if (request.length < 2) return new Answer("Укажите ID для обновления", false);
                int id = Integer.parseInt(request[1]);
                City city = Ask.askCity(console, collectionManager);
                if (city == null) {
                    return new Answer("Обновление города отменено", false);
                }
                city.setId(id);
                message = city.toStr();
            } catch (NumberFormatException e) {
                return new Answer("Неверный числовой формат аргумента", false);
            } catch (Ask.AskBreak e) {
                return new Answer("Обновление города отменено пользователем", false);
            } catch (Exception e) {
                return new Answer("Ошибка при обновлении города: " + e.getMessage(), false);
            }
        } else if (command == CommandTypes.RemoveById ||
                command == CommandTypes.RemoveGreater ||
                command == CommandTypes.RemoveLower) {
            try {
                if (request.length < 2) return new Answer("Укажите аргумент", false);
                Integer.parseInt(request[1]);
                message = request[1];
            } catch (NumberFormatException e) {
                return new Answer("Неверный числовой формат аргумента", false);
            }
        } else if (command == CommandTypes.CountLessThanGovernor) {
            try {
                if (request.length < 2) return new Answer("Укажите значение governor", false);
                Long.parseLong(request[1]);
                message = request[1];
            } catch (NumberFormatException e) {
                return new Answer("Неверный числовой формат аргумента", false);
            }
        } else if (command == CommandTypes.FilterGreaterThanStandardOfLiving) {
            try {
                if (request.length < 2) return new Answer("Укажите standardOfLiving", false);
                StandardOfLiving.valueOf(request[1].toUpperCase());
                message = request[1];
            } catch (IllegalArgumentException e) {
                return new Answer("Неверное значение standardOfLiving", false);
            }
        } else if (command == CommandTypes.Help) return new Help(commands).execute("");
        else if (command == CommandTypes.Info ||
                command == CommandTypes.Show ||
                command == CommandTypes.Clear ||
                command == CommandTypes.History ||
                command == CommandTypes.MinByMetersAboveSeaLevel) {
            if (request.length > 1 && !request[1].isEmpty()) {
                return new Answer("Команда не принимает аргументов", false);
            }
        }

        if (message.isEmpty() && request.length > 1) message = request[1];
        if (message.isEmpty() && request.length == 1) return connector.send(new Container(command));

        return connector.send(new Container(command, message));
    }
}
