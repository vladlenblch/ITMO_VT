package ru.vladlenblch.points;

import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;
import ru.vladlenblch.auth.UserEntity;

public interface PointsRepository extends JpaRepository<PointEntity, Long> {
    List<PointEntity> findAllByUserOrderByTimestampDesc(UserEntity user);
}
