package org.example.validation;

import jakarta.faces.validator.*;
import org.junit.jupiter.api.*;

import static org.junit.jupiter.api.Assertions.*;

class YValidatorTest {

    private final YValidator validator = new YValidator();

    @Test
    void validYPasses() {
        validator.validate(null, null, 0.0);
    }

    @Test
    void nullYThrows() {
        assertTrue(fails(null));
    }

    @Test
    void minYThrows() {
        assertTrue(fails(-5.0));
    }

    @Test
    void maxYThrows() {
        assertTrue(fails(5.0));
    }

    private boolean fails(Double value) {
        try {
            validator.validate(null, null, value);
            return false;
        } catch (ValidatorException exception) {
            return true;
        }
    }
}
