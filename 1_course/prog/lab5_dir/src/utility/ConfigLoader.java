package utility;

/**
 * Класс для загрузки пути JSON-файла.
 * Использует переменные окружения для настройки пути.
 */
public class ConfigLoader {

    /**
     * Возвращает путь к JSON-файлу.
     * Если переменная окружения "PATH_TO_JSON" не установлена, используется путь по умолчанию.
     *
     * @return путь к JSON-файлу
     */
    public static String getJsonPath() {
        String jsonPath = System.getenv("PATH_TO_JSON");

        if (jsonPath == null || jsonPath.isEmpty()) {
            jsonPath = "/home/studs/s466468/cities.json";
        }

        return jsonPath;
    }
}