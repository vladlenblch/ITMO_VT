package org.example.model;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class Result {
    private final int x;
    private final double y;
    private final int r;
    private final boolean hit;
    private final LocalDateTime time;

    public Result(int x, double y, int r, boolean hit, LocalDateTime time) {
        this.x = x;
        this.y = y;
        this.r = r;
        this.hit = hit;
        this.time = time;
    }

    public int getX() { return x; }
    public double getY() { return y; }
    public int getR() { return r; }
    public boolean isHit() { return hit; }
    public LocalDateTime getTime() { return time; }

    public String getFormattedTime() {
        DateTimeFormatter fmt = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
        return time.format(fmt);
    }
}
