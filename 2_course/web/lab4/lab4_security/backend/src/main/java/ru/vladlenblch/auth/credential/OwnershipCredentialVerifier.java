package ru.vladlenblch.auth.credential;

import java.nio.file.Files;
import java.nio.file.Path;
import org.springframework.stereotype.Component;

@Component
public class OwnershipCredentialVerifier implements CredentialVerifier {

    @Override
    public CredentialType supports() {
        return CredentialType.OWNERSHIP;
    }

    @Override
    public boolean verify(CredentialEntity credential, String evidence, String context) {
        String path = credential.getDisplayValue();
        if (path == null || path.isBlank()) {
            return false;
        }
        return Files.exists(Path.of(path));
    }
}
