package ru.vladlenblch.points;

import java.util.List;
import org.springframework.stereotype.Service;
import ru.vladlenblch.auth.UserEntity;
import ru.vladlenblch.points.dto.PointRequest;
import ru.vladlenblch.points.dto.PointResponse;

@Service
public class PointsService {

    private final PointsRepository pointsRepository;

    public PointsService(PointsRepository pointsRepository) {
        this.pointsRepository = pointsRepository;
    }

    public List<PointResponse> findAll(UserEntity user) {
        return pointsRepository.findAllByUserOrderByTimestampDesc(user)
            .stream()
            .map(this::toResponse)
            .toList();
    }

    public PointResponse create(UserEntity user, PointRequest request) {
        boolean hit = isHit(request.x(), request.y(), request.r());
        PointEntity entity = new PointEntity();
        entity.setUser(user);
        entity.setX(request.x());
        entity.setY(request.y());
        entity.setR(request.r());
        entity.setHit(hit);
        return toResponse(pointsRepository.save(entity));
    }

    private boolean isHit(double x, double y, double r) {
        if (r <= 0) {
            return false;
        }
        if (x <= 0 && y >= 0) {
            return x >= -r && y <= r / 2 && y <= 0.5 * (x + r);
        }
        if (x <= 0 && y <= 0) {
            return (x * x + y * y) <= (r * r);
        }
        if (x >= 0 && y <= 0) {
            return x <= r && y >= -r;
        }
        return false;
    }

    private PointResponse toResponse(PointEntity entity) {
        return new PointResponse(
            entity.getId(),
            entity.getX(),
            entity.getY(),
            entity.getR(),
            entity.isHit(),
            entity.getTimestamp()
        );
    }
}
