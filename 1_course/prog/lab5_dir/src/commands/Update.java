package commands;

import managers.CollectionManager;
import console.Console;
import ask.Ask;

/**
 * Команда для обновления значения элемента коллекции по ID.
 */
public class Update extends Command {
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
    public Update(Console console, CollectionManager collectionManager) {
        super("update <ID> {element}", "обновить значение элемента коллекции по ID");
        this.console = console;
        this.collectionManager = collectionManager;
    }

    /**
     * Выполняет команду обновления значения элемента коллекции по ID.
     *
     * @param arguments аргументы команды (ожидается один аргумент — значение ID)
     * @return true, если команда выполнена успешно, иначе false
     */
    @Override
    public boolean apply(String[] arguments) {
        try {
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

            console.println("* Обновление города:");
            var d = Ask.askCity(console, collectionManager);
            if (d != null && d.validate()) {
                collectionManager.add(d);
                collectionManager.addLog("add " + d.getId(), true);
                collectionManager.update();

                var old = collectionManager.byId(id);
                collectionManager.swap(d.getId(), id);
                collectionManager.addLog("swap " + old.getId() + " " + id, false);
                collectionManager.update();

                collectionManager.remove(old.getId());
                collectionManager.addLog("remove " + old.getId(), false);
                collectionManager.update();
                console.println("Город успешно обновлен!");
                return true;
            } else {
                console.println("Поля города невалидны! Город не создан!");
                return false;
            }
        } catch (Ask.AskBreak e) {
            console.println("Отмена");
            return false;
        }
    }
}
