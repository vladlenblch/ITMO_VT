package ru.vladlenblch.auth.credential;

public interface CredentialVerifier {
    CredentialType supports();
    boolean verify(CredentialEntity credential, String evidence, String context);
    default boolean consumeOnSuccess() {
        return false;
    }
}
