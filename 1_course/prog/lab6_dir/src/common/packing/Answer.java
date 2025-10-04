package common.packing;

import java.io.Serial;
import java.io.Serializable;

/**
 * Класс для ответа о выполнении
 * @param message текстовый ответ
 * @param code код выполнения
 */
public record Answer(String message, boolean code) implements Serializable {
    @Serial
    private static final long serialVersionUID = 1L;
}
