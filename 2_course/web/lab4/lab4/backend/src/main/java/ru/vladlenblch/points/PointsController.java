package ru.vladlenblch.points;

import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;
import ru.vladlenblch.auth.AuthService;
import ru.vladlenblch.auth.UserEntity;
import ru.vladlenblch.points.dto.PointRequest;
import ru.vladlenblch.points.dto.PointResponse;

@RestController
@RequestMapping("/api/points")
public class PointsController {

    private final PointsService pointsService;
    private final AuthService authService;

    public PointsController(PointsService pointsService, AuthService authService) {
        this.pointsService = pointsService;
        this.authService = authService;
    }

    @GetMapping
    public List<PointResponse> findAll(@RequestHeader(value = "Authorization", required = false) String token) {
        UserEntity user = requireUser(token);
        return pointsService.findAll(user);
    }

    @PostMapping
    public PointResponse submitPoint(
        @RequestHeader(value = "Authorization", required = false) String token,
        @RequestBody PointRequest request
    ) {
        UserEntity user = requireUser(token);
        return pointsService.create(user, request);
    }

    private UserEntity requireUser(String token) {
        return authService.findUserEntityByToken(token)
            .orElseThrow(() -> new ResponseStatusException(HttpStatus.UNAUTHORIZED, "Требуется авторизация"));
    }
}
