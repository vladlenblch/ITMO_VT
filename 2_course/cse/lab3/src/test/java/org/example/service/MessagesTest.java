package org.example.service;

import org.junit.jupiter.api.*;

import static org.junit.jupiter.api.Assertions.*;

class MessagesTest {

    @Test
    void getReturnsLocalizedMessage() {
        assertEquals("Ошибка", Messages.get("point.error"));
    }

    @Test
    void formatSubstitutesArguments() {
        assertEquals(
                "X должен быть в диапазоне (-5, 5). Текущее значение: 6",
                Messages.format("validation.x.range", 6)
        );
    }
}
