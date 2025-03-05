package managers;

import data.City;

import java.time.LocalDateTime;
import java.util.*;

/**
 * Класс, отвечающий за управление коллекцией городов.
 * Предоставляет методы для добавления, обновления, удаления и сортировки городов,
 * а также для загрузки и сохранения коллекции.
 */
public class CollectionManager {
    /** Текущий ID для генерации уникальных идентификаторов городов. */
    private int currentId = 1;

    /** Коллекция городов, где ключ — ID города, а значение — сам город. */
    private Map<Integer, City> cities = new HashMap<>();

    /** Стек для хранения логов команд. */
    private ArrayDeque<String> logStack = new ArrayDeque<String>();

    /** Основная коллекция городов. */
    private Set<City> collection = new LinkedHashSet<City>();

    /** Время последней инициализации коллекции. */
    private LocalDateTime lastInitTime;

    /** Время последнего сохранения коллекции. */
    private LocalDateTime lastSaveTime;

    /** Менеджер для загрузки и сохранения коллекции. */
    private final DumpManager dumpManager;

    /**
     * Конструктор класса.
     *
     * @param dumpManager менеджер для работы с файлами
     */
    public CollectionManager(DumpManager dumpManager) {
        this.lastInitTime = null;
        this.lastSaveTime = null;
        this.dumpManager = dumpManager;
    }

    /**
     * Возвращает время последней инициализации коллекции.
     *
     * @return время последней инициализации
     */
    public LocalDateTime getLastInitTime() {
        return lastInitTime;
    }

    /**
     * Возвращает время последнего сохранения коллекции.
     *
     * @return время последнего сохранения
     */
    public LocalDateTime getLastSaveTime() {
        return lastSaveTime;
    }

    /**
     * Возвращает текущую коллекцию городов.
     *
     * @return коллекция городов
     */
    public Set<City> getCollection() {
        return collection;
    }

    /**
     * Возвращает город по его ID.
     *
     * @param id ID города
     * @return город или null, если город не найден
     */
    public City byId(int id) {
        return cities.get(id);
    }

    /**
     * Проверяет, содержится ли город в коллекции.
     *
     * @param e город для проверки
     * @return true, если город содержится в коллекции, иначе false
     */
    public boolean isContain(City e) {
        return e == null || byId(e.getId()) != null;
    }

    /**
     * Возвращает свободный ID для нового города.
     *
     * @return свободный ID
     */
    public int getFreeId() {
        while (byId(currentId) != null) {
            currentId++;
        }
        return currentId;
    }

    /**
     * Добавляет город в коллекцию.
     *
     * @param city город для добавления
     * @return true, если город успешно добавлен, иначе false
     */
    public boolean add(City city) {
        if (isContain(city)) return false;
        cities.put(city.getId(), city);
        collection.add(city);
        update();
        return true;
    }

    /**
     * Обновляет город в коллекции.
     *
     * @param city город для обновления
     * @return true, если город успешно обновлён, иначе false
     */
    public boolean update(City city) {
        if (!isContain(city)) return false;
        collection.remove(byId(city.getId()));
        cities.put(city.getId(), city);
        collection.add(city);
        update();
        return true;
    }

    /**
     * Удаляет город из коллекции по его ID.
     *
     * @param id ID города
     * @return true, если город успешно удалён, иначе false
     */
    public boolean remove(int id) {
        City city = byId(id);
        if (city == null) return false;
        cities.remove(city.getId());
        collection.remove(city);
        update();
        return true;
    }

    /**
     * Сортирует коллекцию по имени города.
     */
    public void update() {
        List<City> list = new ArrayList<>(collection);

        list.sort(Comparator.comparing(City::getName));

        collection.clear();
        collection.addAll(list);
    }

    /**
     * Инициализирует коллекцию, загружая данные из файла.
     *
     * @return true, если коллекция успешно инициализирована, иначе false
     */
    public boolean init() {
        collection.clear();
        cities.clear();
        collection = dumpManager.readCollection();
        lastInitTime = LocalDateTime.now();
        for (City city : collection)
            if (byId(city.getId()) != null) {
                collection.clear();
                cities.clear();
                return false;
            } else {
                if (city.getId() > currentId) currentId = city.getId();
                cities.put(city.getId(), city);
            }
        update();
        return true;
    }

    /**
     * Сохраняет коллекцию в файл.
     */
    public void saveCollection() {
        dumpManager.writeCollection(collection);
        lastSaveTime = LocalDateTime.now();
    }

    /**
     * Добавляет команду в лог.
     *
     * @param cmd     команда для добавления
     * @param isFirst true, если это начало команды
     */
    public void addLog(String cmd, boolean isFirst) {
        if (isFirst)
            logStack.push("+");
        if (!cmd.isEmpty())
            logStack.push(cmd);
    }

    /**
     * Меняет местами ID двух городов.
     *
     * @param id    ID первого города
     * @param repId ID второго города
     * @return true, если ID успешно изменены, иначе false
     */
    public boolean swap(int id, int repId) {
        var e = byId(id);
        var re = byId(repId);
        if (e == null) return false;
        if (re == null) return false;

        List<City> list = new ArrayList<>(collection);

        int ind = list.indexOf(e);
        int rind = list.indexOf(re);
        if (ind < 0) return false;
        if (rind < 0) return false;

        e.setId(repId);
        re.setId(id);

        cities.put(e.getId(), e);
        cities.put(re.getId(), re);

        collection.clear();
        collection.addAll(list);

        update();
        return true;
    }

    /**
     * Загружает коллекцию из файла.
     *
     * @return true, если коллекция успешно загружена, иначе false
     */
    public boolean loadCollection() {
        cities.clear();
        collection.clear();

        Set<City> loadedCollection = dumpManager.readCollection();
        if (loadedCollection == null) {
            return false;
        }

        lastInitTime = LocalDateTime.now();

        for (City city : loadedCollection) {
            if (byId(city.getId()) != null) {
                collection.clear();
                cities.clear();
                return false;
            } else {
                if (city.getId() > currentId) {
                    currentId = city.getId();
                }
                cities.put(city.getId(), city);
                collection.add(city);
            }
        }

        update();

        return true;
    }

    /**
     * Возвращает строковое представление коллекции.
     *
     * @return строковое представление коллекции
     */
    @Override
    public String toString() {
        if (collection.isEmpty()) return "Коллекция пустая";

        StringBuilder info = new StringBuilder();
        for (City city : collection) {
            info.append(city).append("\n\n");
        }
        return info.toString().trim();
    }
}