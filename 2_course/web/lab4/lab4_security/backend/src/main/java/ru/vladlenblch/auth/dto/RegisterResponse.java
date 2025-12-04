package ru.vladlenblch.auth.dto;

import java.util.List;

public record RegisterResponse(
    UserDto user,
    String token,
    List<String> recoveryCodes,
    String ownershipFilePath,
    String ownershipFileContent
) {
}
