package ru.vladlenblch.auth.credential;

import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;
import org.springframework.util.StringUtils;

@Component
public class PasswordCredentialVerifier implements CredentialVerifier {

    private final PasswordEncoder passwordEncoder;

    public PasswordCredentialVerifier(PasswordEncoder passwordEncoder) {
        this.passwordEncoder = passwordEncoder;
    }

    @Override
    public CredentialType supports() {
        return CredentialType.PASSWORD;
    }

    @Override
    public boolean verify(CredentialEntity credential, String evidence, String context) {
        if (!StringUtils.hasText(evidence)) {
            return false;
        }
        return passwordEncoder.matches(evidence, credential.getSecretHash());
    }
}
