package data;

public enum StandardOfLiving {
    ULTRA_HIGH,
    VERY_HIGH,
    VERY_LOW,
    NIGHTMARE;

    public static String names() {
		StringBuilder nameList = new StringBuilder();
		for (var standardOfLiving : values()) {
			nameList.append(standardOfLiving.name()).append(", ");
		}
		return nameList.substring(0, nameList.length() - 2);
	}
}
