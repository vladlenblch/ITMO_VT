package org.example.beans;

import jakarta.annotation.PostConstruct;
import jakarta.enterprise.context.SessionScoped;
import jakarta.inject.Named;

import java.io.Serializable;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

@Named
@SessionScoped
public class ClockBean implements Serializable {

    private boolean clockOn = true;
    private String displayData;

    @PostConstruct
    public void init() {
        updateTime();
    }

    public void updateTime() {
        this.displayData = formatTimeForDisplay();
        System.out.println("Time updated: " + displayData);
    }

    private String formatTimeForDisplay() {
        LocalDateTime now = LocalDateTime.now();
        
        DateTimeFormatter timeFormatter = DateTimeFormatter.ofPattern("HH:mm:ss");
        DateTimeFormatter dateFormatter = DateTimeFormatter.ofPattern("dd.MM.yyyy");
        
        String timePart = now.format(timeFormatter);
        String datePart = now.format(dateFormatter);
        
        return timePart + " " + datePart;
    }

    public String getDisplayData() {
        return displayData;
    }

    public String getChar(int index) {
        if (displayData != null && index < displayData.length()) {
            return String.valueOf(displayData.charAt(index));
        }
        return "0";
    }

    public void toggleClock() {
        clockOn = !clockOn;
    }

    public boolean isClockOn() {
        return clockOn;
    }
}
