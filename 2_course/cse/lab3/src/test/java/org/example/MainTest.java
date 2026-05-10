package org.example;

import org.junit.jupiter.api.*;

import java.io.*;
import java.nio.charset.*;

import static org.junit.jupiter.api.Assertions.*;

class MainTest {

    @Test
    void constructorCreatesMain() {
        new Main();
    }

    @Test
    void mainPrintsApplicationArtifactMessage() {
        ByteArrayOutputStream output = new ByteArrayOutputStream();
        System.setOut(new PrintStream(output, true, StandardCharsets.UTF_8));

        Main.main(new String[0]);

        assertEquals("Lab3 web application artifact" + System.lineSeparator(), output.toString(StandardCharsets.UTF_8));
    }
}
