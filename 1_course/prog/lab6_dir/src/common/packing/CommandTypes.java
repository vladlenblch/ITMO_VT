package common.packing;

import java.io.Serializable;

/**
 * Перечисление, представляющее команды
 */
public enum CommandTypes implements Serializable {
    Add("add"),
    Clear("clear"),
    CountLessThanGovernor("count_less_than_governor"),
    ExecuteScript("execute_script"),
    Exit("exit"),
    FilterGreaterThanStandardOfLiving("filter_greater_than_standard_of_living"),
    Help("help"),
    History("history"),
    Info("info"),
    MinByMetersAboveSeaLevel("min_by_meters_above_sea_level"),
    RemoveById("remove_by_id"),
    RemoveGreater("remove_greater"),
    RemoveLower("remove_lower"),
    Show("show"),
    Update("update");

    /**
     * Описание
     */
    private final String description;

    /**
     * Конструктор
     *
     * @param description описание
     */
    CommandTypes(String description) {
        this.description = description;
    }

    /**
     * Описание константы
     *
     * @return возвращает имя команды
     */
    public String Type() {
        return description;
    }

    /**
     * Возвращает CommandType по строковому имени команды
     *
     * @param message команды
     * @return возвращает CommandType по строковому имени команды
     */
    public static CommandTypes getByString(String message) {
        String[] line;
        try {
            line = message.split("_");
            if (line.length == 1) return CommandTypes.valueOf(message.toUpperCase().charAt(0) + message.toLowerCase().substring(1));
            StringBuilder sb = new StringBuilder();
            for (String e: line) {
                sb.append(e.toUpperCase().charAt(0)).append(e.toLowerCase().substring(1));
            }
            return CommandTypes.valueOf(sb.toString());
        } catch (NullPointerException | IllegalArgumentException e) {}
        return null;
    }
}
