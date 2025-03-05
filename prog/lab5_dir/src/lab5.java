import ask.*;
import console.*;
import managers.*;
import commands.*;
import runner.*;
import utility.*;

/**
 * Основной класс программы, который запускает интерактивный режим работы.
 *
 * @author vladlenblch
 */
public class lab5 {

	/**
	 * Точка входа в программу.
	 *
	 * @param args аргументы командной строки (не используются)
	 * @throws Ask.AskBreak если пользователь прерывает выполнение команды
	 */
	public static void main(String[] args) throws Ask.AskBreak {
		var console = new Console();

		String fileName = ConfigLoader.getJsonPath();

		var dumpManager = new DumpManager(fileName, console);

		var collectionManager = new CollectionManager(dumpManager);

		if (!collectionManager.loadCollection()) {
			System.exit(1);
		}

		var commandManager = new CommandManager() {{
			register("help", new Help(console, this));
			register("history", new History(console, this));
			register("info", new Info(console, collectionManager));
			register("show", new Show(console, collectionManager));
			register("add", new Add(console, collectionManager));
			register("update", new Update(console, collectionManager));
			register("remove_by_id", new RemoveById(console, collectionManager));
			register("clear", new Clear(console, collectionManager));
			register("save", new Save(console, collectionManager));
			register("execute_script", new ExecuteScript(console));
			register("exit", new Exit(console));
			register("remove_greater", new RemoveGreater(console, collectionManager));
			register("remove_lower", new RemoveLower(console, collectionManager));
			register("min_by_meters_above_sea_level", new MinByMetersAboveSeaLevel(console, collectionManager));
			register("count_less_than_governor", new CountLessThanGovernor(console, collectionManager));
			register("filter_greater_than_standard_of_living", new FilterGreaterThanStandardOfLiving(console, collectionManager));
		}};

		new Runner(console, commandManager, collectionManager).interactiveMode();
	}
}
