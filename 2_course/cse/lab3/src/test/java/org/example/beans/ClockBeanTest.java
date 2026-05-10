package org.example.beans;

import org.junit.jupiter.api.*;

import static org.junit.jupiter.api.Assertions.*;

class ClockBeanTest {

    @Test
    void newClockIsOn() {
        ClockBean clockBean = new ClockBean();

        assertTrue(clockBean.isClockOn());
    }

    @Test
    void initSetsDisplayData() {
        ClockBean clockBean = new ClockBean();

        clockBean.init();

        assertTrue(clockBean.getDisplayData().matches("\\d{2}:\\d{2}:\\d{2} \\d{2}\\.\\d{2}\\.\\d{4}"));
    }

    @Test
    void updateTimeSetsDisplayData() {
        ClockBean clockBean = new ClockBean();

        clockBean.updateTime();

        assertTrue(clockBean.getDisplayData().matches("\\d{2}:\\d{2}:\\d{2} \\d{2}\\.\\d{2}\\.\\d{4}"));
    }

    @Test
    void getDisplayDataReturnsCurrentDisplayData() {
        ClockBean clockBean = new ClockBean();

        clockBean.updateTime();

        assertTrue(clockBean.getDisplayData().matches("\\d{2}:\\d{2}:\\d{2} \\d{2}\\.\\d{2}\\.\\d{4}"));
    }

    @Test
    void getCharReturnsCharacterByIndex() {
        ClockBean clockBean = new ClockBean();

        clockBean.updateTime();

        assertEquals(1, clockBean.getChar(0).length());
    }

    @Test
    void getCharReturnsZeroWhenIndexIsOutsideDisplayData() {
        ClockBean clockBean = new ClockBean();

        clockBean.updateTime();

        assertEquals("0", clockBean.getChar(100));
    }

    @Test
    void getCharReturnsZeroWhenDisplayDataIsNull() {
        ClockBean clockBean = new ClockBean();

        assertEquals("0", clockBean.getChar(0));
    }

    @Test
    void toggleClockChangesClockState() {
        ClockBean clockBean = new ClockBean();

        clockBean.toggleClock();

        assertFalse(clockBean.isClockOn());

        clockBean.toggleClock();

        assertTrue(clockBean.isClockOn());
    }
}
