package ru.vladlenblch.auth;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;
import ru.vladlenblch.auth.dto.LoginRequest;
import ru.vladlenblch.auth.dto.LoginResponse;
import ru.vladlenblch.auth.dto.RegisterRequest;
import ru.vladlenblch.auth.dto.RegisterResponse;
import ru.vladlenblch.auth.dto.UserDto;
import ru.vladlenblch.auth.dto.CredentialResponse;
import ru.vladlenblch.auth.dto.PasswordRequest;

import java.util.List;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    private final AuthService authService;

    public AuthController(AuthService authService) {
        this.authService = authService;
    }

    @PostMapping("/register")
    public ResponseEntity<RegisterResponse> register(@RequestBody RegisterRequest registerRequest) {
        try {
            return ResponseEntity.ok(authService.register(registerRequest));
        } catch (IllegalArgumentException ex) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, ex.getMessage());
        }
    }

    @PostMapping("/login")
    public ResponseEntity<LoginResponse> login(@RequestBody LoginRequest loginRequest) {
        try {
            return ResponseEntity.ok(authService.login(loginRequest));
        } catch (IllegalArgumentException ex) {
            throw new ResponseStatusException(HttpStatus.UNAUTHORIZED, ex.getMessage());
        }
    }

    @PostMapping("/logout")
    public ResponseEntity<Void> logout(@RequestHeader(value = "Authorization", required = false) String token) {
        authService.logout(token);
        return ResponseEntity.noContent().build();
    }

    @GetMapping("/me")
    public UserDto currentUser(@RequestHeader(value = "Authorization", required = false) String token) {
        return authService.findUserByToken(token)
            .orElseThrow(() -> new ResponseStatusException(HttpStatus.UNAUTHORIZED, "Требуется авторизация"));
    }

    @GetMapping("/credentials")
    public List<CredentialResponse> listCredentials(
        @RequestHeader(value = "Authorization", required = false) String token
    ) {
        var principal = authService.findPrincipalByToken(token)
            .orElseThrow(() -> new ResponseStatusException(HttpStatus.UNAUTHORIZED, "Требуется авторизация"));
        return authService.listCredentials(principal);
    }

    @PostMapping("/credentials/password")
    public ResponseEntity<Void> setPassword(
        @RequestHeader(value = "Authorization", required = false) String token,
        @RequestBody PasswordRequest passwordRequest
    ) {
        var principal = authService.findPrincipalByToken(token)
            .orElseThrow(() -> new ResponseStatusException(HttpStatus.UNAUTHORIZED, "Требуется авторизация"));
        try {
            authService.setPassword(principal, passwordRequest);
            return ResponseEntity.noContent().build();
        } catch (IllegalArgumentException ex) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, ex.getMessage());
        }
    }

    @DeleteMapping("/credentials/{id}")
    public ResponseEntity<Void> deleteCredential(
        @RequestHeader(value = "Authorization", required = false) String token,
        @PathVariable Long id
    ) {
        var principal = authService.findPrincipalByToken(token)
            .orElseThrow(() -> new ResponseStatusException(HttpStatus.UNAUTHORIZED, "Требуется авторизация"));
        try {
            authService.deleteCredential(principal, id);
            return ResponseEntity.noContent().build();
        } catch (IllegalArgumentException ex) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, ex.getMessage());
        }
    }
}
