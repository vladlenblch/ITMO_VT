package common.data;

/**
 * Перечисление, представляющее типы климата.
 */
public enum Climate {

	/** Средиземноморский климат. */
	MEDITERRANIAN,

	/** Субарктический климат. */
	SUBARCTIC,

	/** Тундровый климат. */
	TUNDRA;

	/**
	 * Возвращает строку, содержащую имена всех констант перечисления, разделённые запятыми.
	 *
	 * @return строка с именами констант, например: "MEDITERRANIAN, SUBARCTIC, TUNDRA"
	 */
	public static String names() {
		StringBuilder nameList = new StringBuilder();
		for (var climate : values()) {
			nameList.append(climate.name()).append(", ");
		}
		return nameList.substring(0, nameList.length() - 2);
	}
}