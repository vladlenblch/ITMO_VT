package client;

import common.console.Console;
import common.packing.CommandTypes;
import server.managers.CollectionManager;
import server.managers.DumpManager;

import java.util.HashMap;
import java.util.Map;

public class MainClient {
    public static void main(String[] args) {
        Console console = new Console();

        Map<CommandTypes, String[]> commands = new HashMap<>() {{
            put(CommandTypes.Add, new String[]{"add", "добавить новый город в коллекцию"});
            put(CommandTypes.Update, new String[]{"update id", "обновить город по ID"});
            put(CommandTypes.RemoveById, new String[]{"remove_by_id id", "удалить город по ID"});
            put(CommandTypes.Clear, new String[]{"clear", "очистить коллекцию"});
            put(CommandTypes.Exit, new String[]{"exit", "завершить программу"});
            put(CommandTypes.Show, new String[]{"show", "показать все города в коллекции"});
            put(CommandTypes.Info, new String[]{"info", "показать информацию о коллекции"});
            put(CommandTypes.Help, new String[]{"help", "показать справку по командам"});
            put(CommandTypes.MinByMetersAboveSeaLevel, new String[]{"min_by_meters_above_sea_level",
                    "найти город с минимальной высотой над уровнем моря"});
            put(CommandTypes.FilterGreaterThanStandardOfLiving, new String[]{"filter_greater_than_standard_of_living standard",
                    "фильтровать города по стандарту жизни"});
            put(CommandTypes.CountLessThanGovernor, new String[]{"count_less_than_governor height",
                    "посчитать города с губернатором ниже указанного роста"});
            put(CommandTypes.RemoveGreater, new String[]{"remove_greater population",
                    "удалить города с населением больше указанного"});
            put(CommandTypes.RemoveLower, new String[]{"remove_lower population",
                    "удалить города с населением меньше указанного"});
        }};

        String jsonPath = "D:\\java_itmo\\lab5_dir\\src\\cities.json";

        DumpManager dumpManager = new DumpManager(jsonPath, console);
        CollectionManager collectionManager = new CollectionManager(dumpManager, console);

        try {
            Client client = new Client(console, commands, collectionManager);
            client.start();
            client.interactiveMode();
        } catch (Exception e) {
            console.printError("Ошибка в клиенте: " + e.getMessage());
        }
    }
}
