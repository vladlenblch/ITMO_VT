package ru.vladlenblch.auth.dto;

public record LoginResponse(UserDto user, String token) {
}
