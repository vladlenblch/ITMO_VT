package org.example.beans;

import org.example.entities.PointEntity;
import org.example.entities.UserEntity;
import org.example.service.DatabaseService;

import jakarta.enterprise.context.SessionScoped;
import jakarta.faces.context.FacesContext;
import jakarta.inject.Inject;
import jakarta.inject.Named;
import jakarta.servlet.http.Cookie;
import jakarta.servlet.http.HttpServletRequest;

import java.io.Serializable;
import java.sql.SQLException;
import java.util.List;
import java.util.UUID;

@Named
@SessionScoped
public class UserBean implements Serializable {

    private static final long serialVersionUID = 1L;
    private String sessionId;
    private UserEntity userEntity;

    @Inject
    private DatabaseService databaseService;

    public String getSessionId() {
        return this.sessionId;
    }

    public UserEntity getUserEntity() {
        if (this.userEntity == null) {
            if (this.sessionId == null) {
                this.sessionId = getOrCreateUserId();
            }
            this.userEntity = findOrCreateUserEntity();
        }
        return this.userEntity;
    }

    private String getOrCreateUserId() {
        HttpServletRequest request = (HttpServletRequest) FacesContext.getCurrentInstance().getExternalContext().getRequest();
        Cookie[] cookies = request.getCookies();

        if (cookies != null) {
            for (Cookie cookie : cookies) {
                if ("userId".equals(cookie.getName())) {
                    return cookie.getValue();
                }
            }
        }

        String newUserId = "user_" + UUID.randomUUID().toString();

        FacesContext.getCurrentInstance()
                .getExternalContext().addResponseCookie("userId", newUserId, null);

        return newUserId;
    }

    private UserEntity findOrCreateUserEntity() {
        try {
            UserEntity user = databaseService.findUser(sessionId);
            if (user == null) {
                user = new UserEntity();
                user.setId(sessionId);
                HttpServletRequest request = (HttpServletRequest) FacesContext.getCurrentInstance().getExternalContext().getRequest();
                user.setUserAgent(request.getHeader("User-Agent"));
                databaseService.saveUser(user);
            }
            return user;
        } catch (SQLException e) {
            throw new RuntimeException("Failed to load UserInfo", e);
        }
    }

    public List<PointEntity> getResultsHistory() {
        this.sessionId = getOrCreateUserId();
        if (userEntity == null) {
            this.userEntity = findOrCreateUserEntity();
        }
        try {
            return databaseService.getPointsByUser(userEntity.getId());
        } catch (SQLException e) {
            e.printStackTrace();
            return List.of();
        }
    }
}
