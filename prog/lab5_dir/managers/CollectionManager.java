package managers;

import data.City;

import java.time.LocalDateTime;
import java.util.*;

public class CollectionManager {
    private int currentId = 1;
    private Map<Integer, City> cities = new HashMap<>();
    private ArrayDeque<String> logStack = new ArrayDeque<String>();

    private Set<City> collection = new LinkedHashSet<City>();
    private LocalDateTime lastInitTime;
    private LocalDateTime lastSaveTime;
    private final DumpManager dumpManager;

    public CollectionManager(DumpManager dumpManager) {
        this.lastInitTime = null;
        this.lastSaveTime = null;
        this.dumpManager = dumpManager;
    }

    public LocalDateTime getLastInitTime() {
        return lastInitTime;
    }

    public LocalDateTime getLastSaveTime() {
        return lastSaveTime;
    }

    public Set<City> getCollection() {
        return collection;
    }

    public City byId(int id) {
        return cities.get(id);
    }

    public boolean isContain(City e) {
        return e == null || byId(e.getId()) != null;
    }

    public int getFreeId() {
        while (byId(currentId) != null) {
            currentId++;
        }
        return currentId;
    }

    public boolean add(City city) {
        if (isContain(city)) return false;
        cities.put(city.getId(), city);
        collection.add(city);
        update();
        return true;
    }

    public boolean update(City city) {
        if (!isContain(city)) return false;
        collection.remove(byId(city.getId()));
        cities.put(city.getId(), city);
        collection.add(city);
        update();
        return true;
    }

    public boolean remove(int id) {
        City city = byId(id);
        if (city == null) return false;
        cities.remove(city.getId());
        collection.remove(city);
        update();
        return true;
    }

    public void update() {
        List<City> list = new ArrayList<>(collection);

        list.sort(Comparator.comparing(City::getName));

        collection.clear();
        collection.addAll(list);
    }

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
                if (city.getId()>currentId) currentId = city.getId();
                cities.put(city.getId(), city);
            }
        update();
        return true;
    }

    public void saveCollection() {
        dumpManager.writeCollection(collection);
        lastSaveTime = LocalDateTime.now();
    }

    public void addLog(String cmd, boolean isFirst) {
        if (isFirst)
            logStack.push("+");
        if (!cmd.isEmpty())
            logStack.push(cmd);
    }

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
