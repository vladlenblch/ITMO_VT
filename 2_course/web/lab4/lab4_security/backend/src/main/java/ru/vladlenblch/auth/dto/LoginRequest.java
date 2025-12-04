package ru.vladlenblch.auth.dto;

public record LoginRequest(String username, String credentialType, String value) {
}
