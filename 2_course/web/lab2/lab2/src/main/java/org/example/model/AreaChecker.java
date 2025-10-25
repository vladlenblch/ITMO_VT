package org.example.model;

public class AreaChecker {
    public static boolean isInside(double x, double y, double r) {
        if (x < 0 && y > 0) return false;
        if (x >= 0 && y >= 0) return (x + y) <= r;
        if (x <= 0 && y <= 0) return (x >= -r/2 && x <= 0) && (y >= -r && y <= 0);
        if (x >= 0 && y <= 0) return (x * x + y * y) <= (r * r);
        return false;
    }
}
