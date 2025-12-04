package ru.vladlenblch.auth;

import java.security.SecureRandom;
import java.util.ArrayList;
import java.util.Base64;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;
import ru.vladlenblch.auth.dto.CredentialResponse;
import ru.vladlenblch.auth.dto.LoginRequest;
import ru.vladlenblch.auth.dto.LoginResponse;
import ru.vladlenblch.auth.dto.PasswordRequest;
import ru.vladlenblch.auth.dto.RegisterRequest;
import ru.vladlenblch.auth.dto.RegisterResponse;
import ru.vladlenblch.auth.dto.UserDto;
import ru.vladlenblch.auth.principal.PrincipalEntity;
import ru.vladlenblch.auth.principal.PrincipalRepository;
import ru.vladlenblch.auth.credential.CredentialEntity;
import ru.vladlenblch.auth.credential.CredentialRepository;
import ru.vladlenblch.auth.credential.CredentialType;
import ru.vladlenblch.auth.credential.CredentialVerifier;

@Service
public class AuthService {
    private static final int RECOVERY_CODES_COUNT = 5;
    private static final int RECOVERY_CODE_BYTES = 8;

    private final PrincipalRepository principalRepository;
    private final CredentialRepository credentialRepository;
    private final PasswordEncoder passwordEncoder;
    private final List<CredentialVerifier> verifiers;
    private final Map<String, PrincipalEntity> sessions = new ConcurrentHashMap<>();
    private final SecureRandom secureRandom = new SecureRandom();

    public AuthService(
        PrincipalRepository principalRepository,
        CredentialRepository credentialRepository,
        PasswordEncoder passwordEncoder,
        List<CredentialVerifier> verifiers
    ) {
        this.principalRepository = principalRepository;
        this.credentialRepository = credentialRepository;
        this.passwordEncoder = passwordEncoder;
        this.verifiers = verifiers;
    }

    public RegisterResponse register(RegisterRequest request) {
        if (!StringUtils.hasText(request.username()) || !StringUtils.hasText(request.password())) {
            throw new IllegalArgumentException("Укажите логин и пароль");
        }
        principalRepository.findByUsername(request.username()).ifPresent(existing -> {
            throw new IllegalArgumentException("Пользователь уже существует");
        });
        PrincipalEntity principal = new PrincipalEntity();
        principal.setUsername(request.username().trim());
        PrincipalEntity saved = principalRepository.save(principal);

        CredentialEntity passwordCredential = new CredentialEntity();
        passwordCredential.setPrincipal(saved);
        passwordCredential.setType(CredentialType.PASSWORD);
        passwordCredential.setSecretHash(passwordEncoder.encode(request.password()));
        credentialRepository.save(passwordCredential);

        List<String> recoveryCodes = generateRecoveryCodes(saved);
        OwnershipFile ownershipFile = createOwnershipCredential(saved);

        LoginResponse session = buildSession(saved);
        return new RegisterResponse(session.user(), session.token(), recoveryCodes, ownershipFile.path(), ownershipFile.content());
    }

    public LoginResponse login(LoginRequest request) {
        if (!StringUtils.hasText(request.username()) || !StringUtils.hasText(request.credentialType())
            || (!StringUtils.hasText(request.value()) && !isOwnershipType(request.credentialType()))) {
            throw new IllegalArgumentException("Укажите логин, тип и значение учетных данных");
        }
        CredentialType type = parseCredentialType(request.credentialType());
        PrincipalEntity principal = principalRepository.findByUsername(request.username())
            .orElseThrow(() -> new IllegalArgumentException("Неверный логин или данные"));

        CredentialVerifier verifier = verifiers.stream()
            .filter(v -> v.supports() == type)
            .findFirst()
            .orElseThrow(() -> new IllegalArgumentException("Неподдерживаемый тип учетных данных"));

        List<CredentialEntity> credentials;
        if (type == CredentialType.RECOVERY) {
            credentials = credentialRepository.findAllByPrincipalAndTypeAndUsedFalse(principal, type);
        } else {
            credentials = credentialRepository.findAllByPrincipalAndType(principal, type);
        }

        for (CredentialEntity credential : credentials) {
            String evidence = request.value();
            if (credential.getType() == CredentialType.OWNERSHIP && !StringUtils.hasText(evidence)) {
                evidence = "file-present";
            }
            if (verifier.verify(credential, evidence, null)) {
                if (verifier.consumeOnSuccess()) {
                    credential.setUsed(true);
                    credentialRepository.save(credential);
                }
                return buildSession(principal);
            }
        }
        throw new IllegalArgumentException("Неверный логин или данные");
    }

    public Optional<UserDto> findUserByToken(String rawToken) {
        return Optional.ofNullable(extractToken(rawToken))
            .map(sessions::get)
            .map(this::toDto);
    }

    public Optional<PrincipalEntity> findPrincipalByToken(String rawToken) {
        return Optional.ofNullable(extractToken(rawToken)).map(sessions::get);
    }

    public void logout(String rawToken) {
        Optional.ofNullable(extractToken(rawToken)).ifPresent(sessions::remove);
    }

    public List<CredentialResponse> listCredentials(PrincipalEntity principal) {
        return credentialRepository.findAllByPrincipal(principal).stream()
            .map(cred -> new CredentialResponse(
                cred.getId(),
                cred.getType(),
                cred.getDisplayValue(),
                cred.isUsed(),
                cred.getCreatedAt()
            ))
            .toList();
    }

    public void setPassword(PrincipalEntity principal, PasswordRequest request) {
        if (!StringUtils.hasText(request.password())) {
            throw new IllegalArgumentException("Пароль не может быть пустым");
        }
        credentialRepository.findAllByPrincipalAndType(principal, CredentialType.PASSWORD)
            .forEach(credentialRepository::delete);
        CredentialEntity credential = new CredentialEntity();
        credential.setPrincipal(principal);
        credential.setType(CredentialType.PASSWORD);
        credential.setSecretHash(passwordEncoder.encode(request.password()));
        credential.setDisplayValue(null);
        credentialRepository.save(credential);
    }

    public void deleteCredential(PrincipalEntity principal, Long credentialId) {
        CredentialEntity credential = credentialRepository.findById(credentialId)
            .orElseThrow(() -> new IllegalArgumentException("Способ не найден"));
        if (!credential.getPrincipal().getId().equals(principal.getId())) {
            throw new IllegalArgumentException("Нельзя удалить чужой способ входа");
        }
        if (credential.getType() == CredentialType.OWNERSHIP && credential.getDisplayValue() != null) {
            try {
                java.nio.file.Files.deleteIfExists(java.nio.file.Path.of(credential.getDisplayValue()));
            } catch (Exception ignored) {
            }
        }
        credentialRepository.delete(credential);
    }

    private List<String> generateRecoveryCodes(PrincipalEntity principal) {
        List<String> codes = new ArrayList<>();
        for (int i = 0; i < RECOVERY_CODES_COUNT; i++) {
            String code = generateRecoveryCode();
            codes.add(code);
            CredentialEntity credential = new CredentialEntity();
            credential.setPrincipal(principal);
            credential.setType(CredentialType.RECOVERY);
            credential.setSecretHash(passwordEncoder.encode(code));
            credential.setDisplayValue(code);
            credentialRepository.save(credential);
        }
        return codes;
    }

    private String generateRecoveryCode() {
        byte[] bytes = new byte[RECOVERY_CODE_BYTES];
        secureRandom.nextBytes(bytes);
        return Base64.getUrlEncoder().withoutPadding().encodeToString(bytes);
    }

    private OwnershipFile createOwnershipCredential(PrincipalEntity principal) {
        String token = generateOwnershipToken();
        String baseDir = System.getProperty("user.dir") + "/backend/data/ownership";
        java.io.File dir = new java.io.File(baseDir);
        if (!dir.exists()) {
            dir.mkdirs();
        }
        String fileName = principal.getUsername() + ".txt";
        java.io.File file = new java.io.File(dir, fileName);
        try {
            java.nio.file.Files.writeString(file.toPath(), token);
        } catch (Exception ex) {
            throw new IllegalStateException("Не удалось создать файл права владения", ex);
        }

        CredentialEntity credential = new CredentialEntity();
        credential.setPrincipal(principal);
        credential.setType(CredentialType.OWNERSHIP);
        credential.setSecretHash(passwordEncoder.encode(token));
        credential.setDisplayValue(file.getAbsolutePath());
        credentialRepository.save(credential);
        return new OwnershipFile(file.getAbsolutePath(), token);
    }

    private String generateOwnershipToken() {
        byte[] bytes = new byte[32];
        secureRandom.nextBytes(bytes);
        return Base64.getUrlEncoder().withoutPadding().encodeToString(bytes);
    }

    private boolean isOwnershipType(String credentialType) {
        try {
            return CredentialType.valueOf(credentialType.trim().toUpperCase()) == CredentialType.OWNERSHIP;
        } catch (Exception ex) {
            return false;
        }
    }

    private CredentialType parseCredentialType(String rawType) {
        try {
            return CredentialType.valueOf(rawType.trim().toUpperCase());
        } catch (Exception ex) {
            throw new IllegalArgumentException("Неподдерживаемый тип учетных данных");
        }
    }

    private String extractToken(String rawToken) {
        if (!StringUtils.hasText(rawToken)) {
            return null;
        }
        if (rawToken.startsWith("Bearer ")) {
            return rawToken.substring(7);
        }
        return rawToken;
    }

    private UserDto toDto(PrincipalEntity principal) {
        return new UserDto(principal.getUsername());
    }

    private LoginResponse buildSession(PrincipalEntity principal) {
        String token = UUID.randomUUID().toString();
        sessions.put(token, principal);
        return new LoginResponse(toDto(principal), token);
    }
}
