package ru.vladlenblch.points;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.PrePersist;
import jakarta.persistence.Table;
import java.time.Instant;
import lombok.Getter;
import lombok.Setter;

import ru.vladlenblch.auth.UserEntity;

@Getter
@Entity
@Table(name = "points")
public class PointEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Setter
    @Column(nullable = false)
    private double x;

    @Setter
    @Column(nullable = false)
    private double y;

    @Setter
    @Column(nullable = false)
    private double r;

    @Setter
    @Column(nullable = false)
    private boolean hit;

    @Setter
    @Column(nullable = false)
    private Instant timestamp;

    @Setter
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private UserEntity user;

    @PrePersist
    public void onPersist() {
        if (timestamp == null) {
            timestamp = Instant.now();
        }
    }
}
