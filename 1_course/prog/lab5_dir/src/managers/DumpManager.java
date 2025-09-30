package managers;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.stream.Collectors;

import console.Console;
import data.*;

/**
 * Класс, отвечающий за сохранение и загрузку коллекции городов в формате JSON.
 * Используется для работы с файлами, содержащими данные о городах.
 */
public class DumpManager {
    /** Имя файла для сохранения или загрузки коллекции. */
    private final String fileName;

    /** Консоль для вывода сообщений об ошибках и успешных операциях. */
    private final Console console;

    /** Форматтер для даты (используется при сериализации и десериализации). */
    private final DateTimeFormatter dateFormatter = DateTimeFormatter.ISO_LOCAL_DATE;

    /** Форматтер для даты и времени (используется при сериализации и десериализации). */
    private final DateTimeFormatter dateTimeFormatter = DateTimeFormatter.ISO_LOCAL_DATE_TIME;

    /**
     * Конструктор класса.
     *
     * @param fileName имя файла для сохранения или загрузки коллекции
     * @param console  консоль для вывода сообщений
     */
    public DumpManager(String fileName, Console console) {
        this.fileName = fileName;
        this.console = console;
    }

    /**
     * Сохраняет коллекцию городов в файл в формате JSON.
     *
     * @param collection коллекция городов для сохранения
     */
    public void writeCollection(Collection<City> collection) {
        try (FileOutputStream fos = new FileOutputStream(fileName);
             BufferedOutputStream bos = new BufferedOutputStream(fos)) {

            String json = serializeCollection(collection);
            bos.write(json.getBytes(StandardCharsets.UTF_8));
            console.println("Коллекция успешно сохранена!");

        } catch (IOException e) {
            console.printError("Ошибка записи файла: " + e.getMessage());
        }
    }

    /**
     * Преобразует коллекцию городов в JSON-строку.
     *
     * @param collection коллекция городов
     * @return JSON-строка, представляющая коллекцию
     */
    private String serializeCollection(Collection<City> collection) {
        return "[" + collection.stream()
                .map(this::serializeCity)
                .collect(Collectors.joining(", ")) + "]";
    }

    /**
     * Преобразует объект {@link City} в JSON-строку.
     *
     * @param city объект города
     * @return JSON-строка, представляющая город
     */
    private String serializeCity(City city) {
        return "{" +
                "\"id\": " + city.getId() + "," +
                "\"name\": \"" + escapeJson(city.getName()) + "\"," +
                "\"coordinates\": " + city.getCoordinates() + "," +
                "\"creationDate\": \"" + city.getCreationDate().format(dateFormatter) + "\"," +
                "\"area\": " + city.getArea() + "," +
                "\"population\": " + city.getPopulation() + "," +
                "\"metersAboveSeaLevel\": " + city.getMetersAboveSeaLevel() + "," +
                "\"climate\": " + serializeEnum(city.getClimate()) + "," +
                "\"government\": " + serializeEnum(city.getGovernment()) + "," +
                "\"standardOfLiving\": " + serializeEnum(city.getStandardOfLiving()) + "," +
                "\"governor\": " + city.getGovernor() +
                "}";
    }

    /**
     * Преобразует значение перечисления в строку JSON.
     *
     * @param e значение перечисления
     * @return строковое представление перечисления или "null", если значение равно null
     */
    private String serializeEnum(Enum<?> e) {
        return e != null ? "\"" + e.name() + "\"" : "null";
    }

    /**
     * Экранирует специальные символы в строке для корректного формирования JSON.
     *
     * @param s строка для экранирования
     * @return экранированная строка
     */
    private String escapeJson(String s) {
        return s.replace("\\", "\\\\").replace("\"", "\\\"");
    }

    /**
     * Загружает коллекцию городов из файла.
     *
     * @return коллекция городов, загруженная из файла
     */
    public LinkedHashSet<City> readCollection() {
        LinkedHashSet<City> collection = new LinkedHashSet<>();

        if (fileName == null || fileName.isEmpty()) {
            console.printError("Файл не указан!");
            return collection;
        }

        try (BufferedReader reader = new BufferedReader(new FileReader(fileName))) {
            String json = reader.lines().collect(Collectors.joining());
            json = json.trim();

            if (json.isEmpty()) return collection;
            if (json.charAt(0) != '[' || json.charAt(json.length() - 1) != ']') {
                throw new IOException("Некорректный формат JSON массива!");
            }

            String content = json.substring(1, json.length() - 1).trim();
            if (content.isEmpty()) return collection;

            List<String> cityStrings = splitJsonArray(content);
            for (String cityStr : cityStrings) {
                try {
                    City city = parseCity(cityStr);
                    if (city.validate()) {
                        if (!collection.add(city)) {
                            console.printError("Дубликат города с ID: " + city.getId());
                        }
                    } else {
                        console.printError("Невалидный город: " + cityStr);
                    }
                } catch (Exception e) {
                    console.printError("Ошибка парсинга: " + e);
                }
            }
        } catch (FileNotFoundException e) {
            console.printError("Файл не найден: " + fileName);
        } catch (IOException e) {
            console.printError("Ошибка чтения: " + e.getMessage());
        }

        return collection;
    }

    /**
     * Разделяет JSON-массив на отдельные JSON-объекты.
     *
     * @param content JSON-массив в виде строки
     * @return список JSON-объектов
     */
    private List<String> splitJsonArray(String content) {
        return Arrays.asList(content.split("}, \\{"));
    }

    /**
     * Преобразует JSON-строку в объект {@link City}.
     *
     * @param json JSON-строка, представляющая город
     * @return объект города
     */
    private City parseCity(String json) {
        String[] parts = json.trim()
                .replaceAll("[{}]", "")
                .split(",\\s*");

        Map<String, String> fields = new HashMap<>();

        for (String part : parts) {
            String[] keyValue = part.split(":\\s*", 2);
            String key = keyValue[0].replaceAll("\"", "");
            String value = keyValue[1];
            fields.put(key, value);
        }

        return new City(
                parseInt(fields.get("id")),
                parseString(fields.get("name")),
                parseCoordinates(fields.get("coordinates")),
                parseDate(fields.get("creationDate")),
                parseInt(fields.get("area")),
                parseInt(fields.get("population")),
                parseInt(fields.get("metersAboveSeaLevel")),
                parseEnum(fields.get("climate"), Climate.class),
                parseEnum(fields.get("government"), Government.class),
                parseEnum(fields.get("standardOfLiving"), StandardOfLiving.class),
                parseHuman(fields.get("governor"))
        );
    }

    /**
     * Удаляет кавычки из строки.
     *
     * @param value строка для обработки
     * @return строка без кавычек
     */
    private String parseString(String value) {
        return value.replaceAll("^\"|\"$", "");
    }

    /**
     * Преобразует строку в целое число.
     *
     * @param value строка для преобразования
     * @return целое число
     */
    private int parseInt(String value) {
        return Integer.parseInt(value);
    }

    /**
     * Преобразует строку в объект {@link LocalDate}.
     *
     * @param value строка для преобразования
     * @return объект даты
     */
    private LocalDate parseDate(String value) {
        return LocalDate.parse(parseString(value), dateFormatter);
    }

    /**
     * Преобразует JSON-строку в объект {@link Coordinates}.
     *
     * @param value JSON-строка, представляющая координаты
     * @return объект координат
     */
    private Coordinates parseCoordinates(String value) {
        value = value.replaceAll("[{}\"]", "").trim();
        String[] parts = value.split(", ");

        long x = 0;
        double y = 0;

        for (String part : parts) {
            String[] keyValue = part.split(": ");
            if (keyValue.length == 2) {
                String key = keyValue[0].trim();
                String val = keyValue[1].trim();

                if (key.equals("x")) {
                    x = Long.parseLong(val);
                } else if (key.equals("y")) {
                    y = Double.parseDouble(val);
                }
            }
        }
        return new Coordinates(x, y);
    }

    /**
     * Преобразует строку в значение перечисления.
     *
     * @param value     строка для преобразования
     * @param enumClass класс перечисления
     * @return значение перечисления или null, если строка равна "null"
     */
    private <E extends Enum<E>> E parseEnum(String value, Class<E> enumClass) {
        if (value == null || value.equals("null")) return null;
        return Enum.valueOf(enumClass, parseString(value));
    }

    /**
     * Преобразует JSON-строку в объект {@link Human}.
     *
     * @param value JSON-строка, представляющая губернатора
     * @return объект губернатора
     */
    private Human parseHuman(String value) {
        value = value.replaceAll("[{}\"]", "").trim();
        String[] parts = value.split(", ");

        long height = 0;
        LocalDateTime birthday = null;

        for (String part : parts) {
            String[] keyValue = part.split(": ");
            if (keyValue.length == 2) {
                String key = keyValue[0].trim();
                String val = keyValue[1].trim();

                if (key.equals("height")) {
                    height = Long.parseLong(val);
                } else if (key.equals("birthday")) {
                    if (!val.equals("null")) {
                        birthday = LocalDateTime.parse(val, dateTimeFormatter);
                    }
                }
            }
        }
        return new Human(height, birthday);
    }
}