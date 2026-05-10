package org.example.validation;

import jakarta.faces.validator.*;
import org.junit.jupiter.api.*;

import static org.junit.jupiter.api.Assertions.*;

class RValidatorTest {

    private final RValidator validator = new RValidator();

    @Test
    void validRPasses() {
        validator.validate(null, null, 3.0);
    }

    @Test
    void nullRThrows() {
        assertTrue(fails(null));
    }

    @Test
    void invalidRThrows() {
        assertTrue(fails(2.5));
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
