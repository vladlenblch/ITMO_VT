package common.packing;

import java.io.Serializable;

/**
 * Класс-контейнер для передачи данных между компонентами системы.
 * Поддерживает сериализацию для сетевой передачи.
 *
 * <p>Может содержать один из следующих наборов данных:
 * <ul>
 *   <li>Команда ({@link CommandTypes})</li>
 *   <li>Команда с дополнительным сообщением (String)</li>
 *   <li>Ответ ({@link Answer})</li>
 * </ul>
 *
 * @see CommandTypes
 * @see Answer
 */
public class Container implements Serializable {

    /**
     * Тип команды, хранящейся в контейнере.
     * Может быть null, если контейнер содержит только ответ.
     */
    private CommandTypes command;

    /**
     * Текстовое сообщение, связанное с командой.
     * Может быть null, если не требуется передача дополнительной информации.
     */
    private String message;

    /**
     * Ответ на выполнение команды.
     * Может быть null, если контейнер используется для запроса.
     */
    private Answer answer;

    /**
     * Создает новый контейнер с указанной командой.
     *
     * @param command команда для выполнения, не может быть null
     * @throws IllegalArgumentException если command равен null
     */
    public Container(CommandTypes command) {
        if (command == null) {
            throw new IllegalArgumentException("Command cannot be null");
        }
        this.command = command;
    }

    /**
     * Создает новый контейнер с указанной командой и сообщением.
     *
     * @param command команда для выполнения, не может быть null
     * @param message дополнительное текстовое сообщение
     * @throws IllegalArgumentException если command равен null
     */
    public Container(CommandTypes command, String message) {
        if (command == null) {
            throw new IllegalArgumentException("Command cannot be null");
        }
        this.command = command;
        this.message = message;
    }

    /**
     * Создает новый контейнер с ответом.
     *
     * @param answer объект ответа, не может быть null
     * @throws IllegalArgumentException если answer равен null
     */
    public Container(Answer answer) {
        if (answer == null) {
            throw new IllegalArgumentException("Answer cannot be null");
        }
        this.answer = answer;
    }

    /**
     * Возвращает команду, содержащуюся в контейнере.
     *
     * @return объект CommandTypes или null, если контейнер содержит только ответ
     */
    public CommandTypes getCommand() {
        return command;
    }

    /**
     * Возвращает сообщение, связанное с командой.
     *
     * @return текстовое сообщение или null, если сообщение не было установлено
     */
    public String getMessage() {
        return message;
    }

    /**
     * Возвращает ответ, содержащийся в контейнере.
     *
     * @return объект Answer или null, если контейнер содержит только команду
     */
    public Answer getAnswer() {
        return answer;
    }

    /**
     * Возвращает строковое представление контейнера.
     *
     * @return строковое описание содержимого контейнера
     */
    @Override
    public String toString() {
        return "Container {" +
                "command=" + command +
                ", message='" + message + '\'' +
                ", answer=" + answer +
                '}';
    }
}
