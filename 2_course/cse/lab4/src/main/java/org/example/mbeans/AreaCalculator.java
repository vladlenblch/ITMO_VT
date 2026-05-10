package org.example.mbeans;

import org.example.mbeans.interfaces.AreaCalculatorMBean;

public class AreaCalculator implements AreaCalculatorMBean {

    private volatile double radius;

    public void setRadius(double radius) {
        this.radius = radius;
    }

    @Override
    public double getArea() {
        return (radius * radius) + (1 / 2 * radius / 2 * radius) + (Math.PI * radius * radius / 4);
    }
}
