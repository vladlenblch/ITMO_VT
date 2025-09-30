package commands;

import managers.CollectionManager;
import console.Console;

/**
 * Команда для удаления элемента из коллекции по ID.
 */
public class RemoveById extends Command {
    /** Консоль для взаимодействия с пользователем. */
    private final Console console;

    /** Менеджер коллекции, в которой производится поиск. */
    private final CollectionManager collectionManager;

    /**
     * Конструктор команды.
     *
     * @param console           консоль для взаимодействия с пользователем
     * @param collectionManager менеджер коллекции
     */
    public RemoveById(Console console, CollectionManager collectionManager) {
        super("remove_by_id <ID>", "удалить элемент из коллекции по ID");
        this.console = console;
        this.collectionManager = collectionManager;
    }

    /**
     * Выполняет команду удаления элемента из коллекции по ID.
     *
     * @param arguments аргументы команды (ожидается один аргумент — значение ID)
     * @return true, если команда выполнена успешно, иначе false
     */
    @Override
    public boolean apply(String[] arguments) {
        if (arguments[1].isEmpty()) {
            console.println("Неправильное количество аргументов!");
            console.println("Использование: '" + getName() + "'");
            return false;
        }
        int id = -1;
        try { id = Integer.parseInt(arguments[1].trim()); } catch (NumberFormatException e) { console.println("ID не распознан"); return false; }

        if (collectionManager.byId(id) == null || !collectionManager.getCollection().contains(collectionManager.byId(id))) {
            console.println("Несуществующий ID");
            return false;
        }
        collectionManager.remove(id);
        collectionManager.addLog("remove " + id, true);
        collectionManager.update();
        console.println("Город успешно удалён!");
        return true;
    }
}
