package ru.vladlenblch.auth.credential;

import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;
import org.springframework.util.StringUtils;

@Component
public class RecoveryCredentialVerifier implements CredentialVerifier {

    private final PasswordEncoder passwordEncoder;

    public RecoveryCredentialVerifier(PasswordEncoder passwordEncoder) {
        this.passwordEncoder = passwordEncoder;
    }

    @Override
    public CredentialType supports() {
        return CredentialType.RECOVERY;
    }

    @Override
    public boolean verify(CredentialEntity credential, String evidence, String context) {
        if (!StringUtils.hasText(evidence) || credential.isUsed()) {
            return false;
        }
        return passwordEncoder.matches(evidence, credential.getSecretHash());
    }

    @Override
    public boolean consumeOnSuccess() {
        return true;
    }
}
