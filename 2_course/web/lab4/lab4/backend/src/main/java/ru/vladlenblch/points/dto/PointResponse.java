package ru.vladlenblch.points.dto;

import java.time.Instant;

public record PointResponse(
    Long id,
    double x,
    double y,
    double r,
    boolean hit,
    Instant timestamp
) {
}
