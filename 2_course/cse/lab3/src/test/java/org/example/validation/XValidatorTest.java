package org.example.validation;

import jakarta.faces.validator.*;
import org.junit.jupiter.api.*;

import static org.junit.jupiter.api.Assertions.*;

class XValidatorTest {

    private final XValidator validator = new XValidator();

    @Test
    void validXPasses() {
        validator.validate(null, null, 0.0);
    }

    @Test
    void nullXThrows() {
        assertTrue(fails(null));
    }

    @Test
    void minXThrows() {
        assertTrue(fails(-5.0));
    }

    @Test
    void maxXThrows() {
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
