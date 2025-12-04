package ru.vladlenblch.auth.credential;

import java.util.List;
import java.util.Optional;
import ru.vladlenblch.auth.principal.PrincipalEntity;
import org.springframework.data.jpa.repository.JpaRepository;

public interface CredentialRepository extends JpaRepository<CredentialEntity, Long> {
    List<CredentialEntity> findAllByPrincipal(PrincipalEntity principal);
    List<CredentialEntity> findAllByPrincipalAndType(PrincipalEntity principal, CredentialType type);
    List<CredentialEntity> findAllByPrincipalAndTypeAndUsedFalse(PrincipalEntity principal, CredentialType type);
}
