package common.data;

/**
 * Перечисление, представляющее уровни жизни.
 */
public enum StandardOfLiving {

	/** Сверхвысокий уровень жизни. */
	ULTRA_HIGH,

	/** Очень высокий уровень жизни. */
	VERY_HIGH,

	/** Очень низкий уровень жизни. */
	VERY_LOW,

	/** Кошмарный уровень жизни. */
	NIGHTMARE;

	/**
	 * Возвращает строку, содержащую имена всех констант перечисления, разделённые запятыми.
	 *
	 * @return строка с именами констант
	 */
	public static String names() {
		StringBuilder nameList = new StringBuilder();
		for (var standardOfLiving : values()) {
			nameList.append(standardOfLiving.name()).append(", ");
		}
		return nameList.substring(0, nameList.length() - 2);
	}
}