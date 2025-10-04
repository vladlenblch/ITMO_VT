package server;

import common.console.Console;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import server.commands.*;
import server.managers.CollectionManager;
import server.managers.CommandManager;
import server.managers.DumpManager;

public class MainServer {
    private static final Logger logger = LogManager.getLogger(MainServer.class);

    public static void main(String[] args) {
        System.setProperty("log4j.configurationFile", "D:\\java_itmo\\lab5_dir\\src\\log4j2.xml");

        Console console = new Console();

        String jsonPath = "D:\\java_itmo\\lab5_dir\\src\\cities.json";
        logger.info("Используется файл данных: {}", jsonPath);

        DumpManager dumpManager = new DumpManager(jsonPath, console);
        CollectionManager collectionManager = new CollectionManager(dumpManager, console);

        CommandManager commandManager = new CommandManager(){{
            register("add", new Add(console, collectionManager));
            register("show", new Show(console, collectionManager));
            register("update", new Update(console, collectionManager));
            register("remove_by_id", new RemoveById(console, collectionManager));
            register("clear", new Clear(console, collectionManager));
            register("exit", new Exit(console, collectionManager));
            register("info", new Info(console, collectionManager));
            register("remove_greater", new RemoveGreater(console, collectionManager));
            register("remove_lower", new RemoveLower(console, collectionManager));
            register("min_by_meters_above_sea_level", new MinByMetersAboveSeaLevel(console, collectionManager));
            register("filter_greater_than_standard_of_living", new FilterGreaterThanStandardOfLiving(console, collectionManager));
            register("count_less_than_governor", new CountLessThanGovernor(console, collectionManager));
        }};

        if (!collectionManager.loadCollection()) {
            logger.fatal("Ошибка загрузки коллекции! Завершение работы.");
            System.exit(1);
        }

        logger.info("Сервер запускается на порту 6789");
        new Server(commandManager, collectionManager, console).run(6789);
    }
}
