package commands;

import managers.CollectionManager;
import ask.Ask;
import data.City;
import console.Console;

/**
 * Команда для добавления нового элемента в коллекцию.
 */
public class Add extends Command {
    /** Консоль для взаимодействия с пользователем. */
    private final Console console;

    /** Менеджер коллекции, в которую добавляется элемент. */
    private final CollectionManager collectionManager;

    /**
     * Конструктор команды.
     *
     * @param console           консоль для взаимодействия с пользователем
     * @param collectionManager менеджер коллекции
     */
    public Add(Console console, CollectionManager collectionManager) {
        super("add {element}", "добавить новый элемент в коллекцию");
        this.console = console;
        this.collectionManager = collectionManager;
    }

    /**
     * Выполняет команду добавления нового элемента в коллекцию.
     *
     * @param arguments аргументы команды
     * @return true, если команда выполнена успешно, иначе false
     */
    @Override
    public boolean apply(String[] arguments) {
        try {
            if (!arguments[1].isEmpty()) {
                console.println("Неправильное количество аргументов!");
                console.println("Использование: '" + getName() + "'");
                return false;
            }

            console.println("* Создание нового города:");
            City city = Ask.askCity(console, collectionManager);

            if (city != null && city.validate()) {
                collectionManager.add(city);
                collectionManager.addLog("add " + city.getId(), true);
                console.println("Город успешно добавлен!");
                return true;
            } else {
                console.printError("Поля города невалидны! Город не создан!");
                return false;
            }
        } catch (Ask.AskBreak e) {
            console.println("Отмена");
            return false;
        }
    }
}