package data;

public enum Climate {
    MEDITERRANIAN,
    SUBARCTIC,
    TUNDRA;

    public static String names() {
		StringBuilder nameList = new StringBuilder();
		for (var climate : values()) {
			nameList.append(climate.name()).append(", ");
		}
		return nameList.substring(0, nameList.length() - 2);
	}
}
