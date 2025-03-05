package data;

/**
 * Перечисление, представляющее формы правления.
 */
public enum Government {

    /** Марионеточное государство. */
    PUPPET_STATE,

    /** Олигархия. */
    OLIGARCHY,

    /** Патриархат. */
    PATRIARCHY,

    /** Республика. */
    REPUBLIC,

    /** Теократия. */
    THEOCRACY;

    /**
     * Возвращает строку, содержащую имена всех констант перечисления, разделённые запятыми.
     *
     * @return строка с именами констант
     */
    public static String names() {
        StringBuilder nameList = new StringBuilder();
        for (var government : values()) {
            nameList.append(government.name()).append(", ");
        }
        return nameList.substring(0, nameList.length() - 2);
    }
}