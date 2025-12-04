package ru.vladlenblch.auth.principal;

import java.util.Optional;
import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;

public interface PrincipalRepository extends JpaRepository<PrincipalEntity, UUID> {
    Optional<PrincipalEntity> findByUsername(String username);
}
