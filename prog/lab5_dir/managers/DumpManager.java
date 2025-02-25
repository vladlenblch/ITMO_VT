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

public class DumpManager {
    private final String fileName;
    private final Console console;
    private final DateTimeFormatter dateFormatter = DateTimeFormatter.ISO_LOCAL_DATE;
    private final DateTimeFormatter dateTimeFormatter = DateTimeFormatter.ISO_LOCAL_DATE_TIME;

    public DumpManager(String fileName, Console console) {
        this.fileName = fileName;
        this.console = console;
    }

    public void writeCollection(Collection<City> collection) {
        try (FileOutputStream fos = new FileOutputStream(fileName);
             BufferedOutputStream bos = new BufferedOutputStream(fos)) {

            String json = serializeCollection(collection);
            bos.write(json.getBytes(StandardCharsets.UTF_8));
            console.println("Коллекция успешно сохранена");

        } catch (IOException e) {
            console.printError("Ошибка записи файла: " + e.getMessage());
        }
    }

    private String serializeCollection(Collection<City> collection) {
        return "[" + collection.stream()
                .map(this::serializeCity)
                .collect(Collectors.joining(", ")) + "]";
    }

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

    private String serializeEnum(Enum<?> e) {
        return e != null ? "\"" + e.name() + "\"" : "null";
    }

    private String escapeJson(String s) {
        return s.replace("\\", "\\\\").replace("\"", "\\\"");
    }

    public LinkedHashSet<City> readCollection() {
        LinkedHashSet<City> collection = new LinkedHashSet<>();

        if (fileName == null || fileName.isEmpty()) {
            console.printError("Файл не указан");
            return collection;
        }

        try (BufferedReader reader = new BufferedReader(new FileReader(fileName))) {
            String json = reader.lines().collect(Collectors.joining());
            json = json.trim();

            if (json.isEmpty()) return collection;
            if (json.charAt(0) != '[' || json.charAt(json.length() - 1) != ']') {
                throw new IOException("Некорректный формат JSON массива");
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
                    console.printError("Ошибка парсинга: " + e.getMessage());
                }
            }
        } catch (FileNotFoundException e) {
            console.printError("Файл не найден: " + fileName);
        } catch (IOException e) {
            console.printError("Ошибка чтения: " + e.getMessage());
        }

        return collection;
    }

    private List<String> splitJsonArray(String content) {
        return Arrays.asList(content.split("}, \\{"));
    }

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

    private String parseString(String value) {
        return value.replaceAll("^\"|\"$", ""); // Удаляем кавычки в начале и конце
    }

    private int parseInt(String value) {
        return Integer.parseInt(value);
    }

    private LocalDate parseDate(String value) {
        return LocalDate.parse(parseString(value), dateFormatter);
    }

    private Coordinates parseCoordinates(String value) {
        String[] parts = value.replaceAll("[{}\"]", "").split(", ");
        return new Coordinates(
            Long.parseLong(parts[0].split(": ")[1]),
            Double.parseDouble(parts[1].split(": ")[1])
        );
    }

    private <E extends Enum<E>> E parseEnum(String value, Class<E> enumClass) {
        if (value == null || value.equals("null")) return null;
        return Enum.valueOf(enumClass, parseString(value));
    }

    private Human parseHuman(String value) {
        String[] parts = value.replaceAll("[{}\"]", "").split(", ");
        long height = Long.parseLong(parts[0].split(": ")[1]);
        String birthdayPart = parts[1].split(": ")[1];
        LocalDateTime birthday = birthdayPart.equals("null") ? null :
            LocalDateTime.parse(birthdayPart, dateTimeFormatter);

        return new Human(height, birthday);
    }
}
