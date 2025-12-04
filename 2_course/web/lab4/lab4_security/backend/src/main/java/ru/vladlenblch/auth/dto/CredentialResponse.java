package ru.vladlenblch.auth.dto;

import java.time.Instant;
import ru.vladlenblch.auth.credential.CredentialType;

public record CredentialResponse(
    Long id,
    CredentialType type,
    String displayValue,
    boolean used,
    Instant createdAt
) {
}
