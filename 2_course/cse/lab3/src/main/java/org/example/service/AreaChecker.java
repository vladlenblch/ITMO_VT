package org.example.service;

public final class AreaChecker {

    private AreaChecker() {
    }

    public static boolean checkHit(double x, double y, double r) {
        double normalizedX = round3(x);
        double normalizedY = round3(y);
        double normalizedR = round3(r);
        double halfR = normalizedR / 2.0;

        if (normalizedX <= 0 && normalizedY >= 0) {
            if (normalizedX >= -halfR) {
                double lineY = normalizedX * 2.0 + normalizedR;
                if (normalizedY <= lineY) {
                    return true;
                }
            }
        }

        if (normalizedX <= 0 && normalizedY <= 0) {
            if (normalizedX >= -normalizedR && normalizedY >= -normalizedR) {
                return true;
            }
        }

        if (normalizedX >= 0 && normalizedY <= 0) {
            double sumSquares = normalizedX * normalizedX + normalizedY * normalizedY;
            double rSquared = normalizedR * normalizedR;
            if (sumSquares <= rSquared) {
                return true;
            }
        }

        return false;
    }

    public static double round3(double value) {
        return Math.round(value * 1000.0) / 1000.0;
    }
}
