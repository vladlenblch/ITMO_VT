package ru.vladlenblch.auth;

import java.util.Map;
import java.util.Optional;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;
import ru.vladlenblch.auth.dto.LoginRequest;
import ru.vladlenblch.auth.dto.LoginResponse;
import ru.vladlenblch.auth.dto.RegisterRequest;
import ru.vladlenblch.auth.dto.UserDto;

@Service
public class AuthService {
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final Map<String, UserEntity> sessions = new ConcurrentHashMap<>();

    public AuthService(UserRepository userRepository, PasswordEncoder passwordEncoder) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
    }

    public LoginResponse register(RegisterRequest request) {
        if (!StringUtils.hasText(request.username()) || !StringUtils.hasText(request.password())) {
            throw new IllegalArgumentException("Укажите логин и пароль");
        }
        userRepository.findByUsername(request.username()).ifPresent(existing -> {
            throw new IllegalArgumentException("Пользователь уже существует");
        });
        UserEntity user = new UserEntity();
        user.setUsername(request.username().trim());
        user.setPasswordHash(passwordEncoder.encode(request.password()));
        UserEntity saved = userRepository.save(user);
        return buildSession(saved);
    }

    public LoginResponse login(LoginRequest request) {
        if (!StringUtils.hasText(request.username()) || !StringUtils.hasText(request.password())) {
            throw new IllegalArgumentException("Укажите логин и пароль");
        }

        UserEntity user = userRepository.findByUsername(request.username())
            .orElseThrow(() -> new IllegalArgumentException("Неверный логин или пароль"));

        if (!passwordEncoder.matches(request.password(), user.getPasswordHash())) {
            throw new IllegalArgumentException("Неверный логин или пароль");
        }
        return buildSession(user);
    }

    public Optional<UserDto> findUserByToken(String rawToken) {
        return Optional.ofNullable(extractToken(rawToken))
            .map(sessions::get)
            .map(this::toDto);
    }

    public Optional<UserEntity> findUserEntityByToken(String rawToken) {
        return Optional.ofNullable(extractToken(rawToken)).map(sessions::get);
    }

    public void logout(String rawToken) {
        Optional.ofNullable(extractToken(rawToken)).ifPresent(sessions::remove);
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

    private UserDto toDto(UserEntity user) {
        return new UserDto(user.getUsername());
    }

    private LoginResponse buildSession(UserEntity user) {
        String token = UUID.randomUUID().toString();
        sessions.put(token, user);
        return new LoginResponse(toDto(user), token);
    }
}
