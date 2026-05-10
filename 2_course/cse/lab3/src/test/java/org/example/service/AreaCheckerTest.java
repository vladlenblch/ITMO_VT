package org.example.service;

import org.junit.jupiter.api.*;

import static org.junit.jupiter.api.Assertions.*;

class AreaCheckerTest {

    @Test
    void pointInsideUpperLeftTriangleReturnsHit() {
        assertTrue(check("-1", "1", "4"));
    }

    @Test
    void pointLeftOfTriangleReturnsMiss() {
        assertFalse(check("-3", "1", "4"));
    }

    @Test
    void pointAboveTriangleLineReturnsMiss() {
        assertFalse(check("-1", "3", "4"));
    }

    @Test
    void pointInsideLowerLeftSquareReturnsHit() {
        assertTrue(check("-2", "-2", "4"));
    }

    @Test
    void pointLeftOfSquareReturnsMiss() {
        assertFalse(check("-5", "-1", "4"));
    }

    @Test
    void pointBelowSquareReturnsMiss() {
        assertFalse(check("-1", "-5", "4"));
    }

    @Test
    void pointInsideLowerRightCircleReturnsHit() {
        assertTrue(check("2", "-2", "4"));
    }

    @Test
    void pointOutsideLowerRightCircleReturnsMiss() {
        assertFalse(check("4", "-4", "4"));
    }

    @Test
    void pointOnBorderReturnsHit() {
        assertTrue(check("0", "4", "4"));
    }

    @Test
    void pointOutsideAreaReturnsMiss() {
        assertFalse(check("3", "3", "4"));
    }

    @Test
    void round3RoundsToThreeDecimalPlaces() {
        assertEquals(1.235, AreaChecker.round3(1.23456));
    }

    private static boolean check(String x, String y, String r) {
        return AreaChecker.checkHit(decimal(x), decimal(y), decimal(r));
    }

    private static Double decimal(String value) {
        return Double.valueOf(value);
    }
}
