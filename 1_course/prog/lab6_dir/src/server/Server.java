package server;

import common.console.Console;
import common.packing.Answer;
import common.packing.CommandTypes;
import common.packing.Container;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import server.connector.ServerConnector;
import server.managers.CollectionManager;
import server.managers.CommandManager;

/**
 * Основной класс сервера для обработки команд и управления коллекцией.
 * Обеспечивает взаимодействие между клиентами и менеджерами команд/коллекции.
 */
public class Server {
    private static final Logger logger = LogManager.getLogger(Server.class);

    private final CollectionManager collectionManager;
    private final CommandManager commandManager;
    private final Console console;
    private ServerConnector connector;

    /**
     * Конструктор сервера.
     *
     * @param commandManager    менеджер команд для обработки запросов
     * @param collectionManager менеджер коллекции для работы с данными
     * @param console           консоль для вывода информации
     */
    public Server(CommandManager commandManager,
                  CollectionManager collectionManager,
                  Console console) {
        this.commandManager = commandManager;
        this.collectionManager = collectionManager;
        this.console = console;
    }

    /**
     * Выполняет команду с указанными аргументами.
     *
     * @param command   тип команды для выполнения
     * @param arguments аргументы команды
     * @return результат выполнения команды
     */
    public Answer launchCommand(CommandTypes command, String arguments) {
        if (command == null) {
            logger.warn("Попытка выполнения null-команды");
            return new Answer("Неверная команда", false);
        }

        try {
            var cmd = commandManager.getCommands().get(command.Type());
            if (cmd == null) {
                logger.warn("Команда не найдена: {}", command.Type());
                return new Answer("Команда не найдена", false);
            }

            commandManager.addToHistory(command.Type());
            Answer response = cmd.execute(arguments);
            logger.info("Выполнена команда: {} с аргументами: {}", command.Type(), arguments);
            return response;

        } catch (Exception e) {
            logger.error("Ошибка выполнения команды {}: {}", command.Type(), e.getMessage());
            return new Answer("Ошибка выполнения: " + e.getMessage(), false);
        }
    }

    /**
     * Выполняет команду без аргументов.
     *
     * @param command тип команды для выполнения
     * @return результат выполнения команды
     */
    public Answer launchCommand(CommandTypes command) {
        return launchCommand(command, "");
    }

    /**
     * Обрабатывает входящий контейнер с командой.
     *
     * @param container контейнер с командой и данными
     * @return результат обработки команды
     */
    public Answer processContainer(Container container) {
        if (container == null) {
            logger.warn("Получен null-контейнер");
            return new Answer("Ошибка: пустой запрос", false);
        }

        if (container.getCommand() != null) {
            if (container.getMessage() != null) {
                return launchCommand(container.getCommand(), container.getMessage());
            }
            return launchCommand(container.getCommand());
        }

        logger.info("Новое подключение: {}", container.getAnswer());
        return new Answer("Сервер готов к работе", true);
    }

    /**
     * Запускает обработку контейнера в зависимости от его содержимого.
     *
     * @param container контейнер с командой и данными
     * @return результат обработки
     */
    public Answer launch(Container container) {
        if (container == null) {
            logger.debug("Получен пустой запрос (таймаут)");
            return new Answer("Нет данных для обработки", true);
        }

        if (container.getCommand() != null && container.getMessage() != null) {
            return launchCommand(container.getCommand(), container.getMessage());
        }
        if (container.getCommand() != null) {
            return launchCommand(container.getCommand());
        }

        logger.info("Новое подключение {}", container.getAnswer() != null ?
                container.getAnswer().message() : "без данных");
        return new Answer("Подключение установлено!", true);
    }

    /**
     * Запускает сервер в работу на указанном порту.
     *
     * @param port порт для прослушивания входящих соединений
     */
    public void run(int port) {
        connector = new ServerConnector(port);
        logger.info("Развертывание сервера");
        var answer = connector.startPolling();
        if (!answer.code()) {
            logger.error(answer.message());
            System.exit(0);
        }

        while (true) {
            Container request = connector.getRequest();
            if (request == null) {
                continue;
            }

            Answer answerReq = launch(request);
            if (answerReq != null) {
                Answer answerSend = connector.sendPacket(new Container(answerReq));
                if (!answerSend.code()) {
                    logger.warn("Ошибка отправки: {}", answerSend.message());
                }
            }
        }
    }
}