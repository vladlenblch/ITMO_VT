package org.example.beans;

import org.example.*;
import org.example.entities.*;
import org.example.service.*;

import jakarta.servlet.http.*;
import org.junit.jupiter.api.*;

import java.util.*;

import static org.example.TestBeans.*;
import static org.example.TestFields.*;
import static org.example.TestRequests.*;
import static org.junit.jupiter.api.Assertions.*;

class UserBeanTest {

    @Test
    void newUserBeanHasNullSessionId() {
        UserBean userBean = new UserBean();

        assertNull(userBean.getSessionId());
    }

    @Test
    void getSessionIdReturnsCurrentSessionId() throws Exception {
        UserBean userBean = new UserBean();

        setField(userBean, "sessionId", "user-1");

        assertEquals("user-1", userBean.getSessionId());
    }

    @Test
    void getUserEntityReturnsExistingUserEntity() throws Exception {
        UserBean userBean = new UserBean();
        UserEntity userEntity = new UserEntity();

        setField(userBean, "userEntity", userEntity);

        assertEquals(userEntity, userBean.getUserEntity());
    }

    @Test
    void getUserEntityUsesUserIdCookieAndExistingDatabaseUser() throws Exception {
        UserEntity userEntity = user("user-1", "Firefox");
        UserDatabaseService databaseService = new UserDatabaseService();
        databaseService.user = userEntity;
        UserBean userBean = userBean(databaseService);

        TestFacesContext.set(new TestFacesContext(request(new Cookie[] {
                new Cookie("other", "ignored"),
                new Cookie("userId", "user-1")
        }, "Firefox")));

        assertEquals(userEntity, userBean.getUserEntity());
        assertEquals("user-1", userBean.getSessionId());
    }

    @Test
    void getUserEntityCreatesCookieAndSavesNewUserWhenCookieIsMissing() throws Exception {
        UserDatabaseService databaseService = new UserDatabaseService();
        UserBean userBean = userBean(databaseService);
        TestFacesContext context = new TestFacesContext(request(null, "Safari"));

        TestFacesContext.set(context);

        UserEntity userEntity = userBean.getUserEntity();

        assertTrue(userEntity.getId().startsWith("user_"));
        assertEquals("Safari", userEntity.getUserAgent());
        assertEquals(userEntity, databaseService.savedUser);
        assertEquals("userId", context.externalContext.responseCookieName);
        assertEquals(userEntity.getId(), context.externalContext.responseCookieValue);
    }

    @Test
    void getUserEntityCreatesCookieWhenCookiesDoNotContainUserId() throws Exception {
        UserDatabaseService databaseService = new UserDatabaseService();
        UserBean userBean = userBean(databaseService);
        TestFacesContext context = new TestFacesContext(request(new Cookie[] {
                new Cookie("other", "ignored")
        }, "Safari"));

        TestFacesContext.set(context);

        UserEntity userEntity = userBean.getUserEntity();

        assertTrue(userEntity.getId().startsWith("user_"));
        assertEquals("userId", context.externalContext.responseCookieName);
        assertEquals(userEntity.getId(), context.externalContext.responseCookieValue);
    }

    @Test
    void getUserEntityUsesExistingSessionId() throws Exception {
        UserEntity userEntity = user("user-1", "Firefox");
        UserDatabaseService databaseService = new UserDatabaseService();
        databaseService.user = userEntity;
        UserBean userBean = userBean(databaseService);

        setField(userBean, "sessionId", "user-1");

        assertEquals(userEntity, userBean.getUserEntity());
    }

    @Test
    void getUserEntityThrowsRuntimeExceptionOnSqlException() throws Exception {
        UserDatabaseService databaseService = new UserDatabaseService();
        databaseService.fail = true;
        UserBean userBean = userBean(databaseService);

        setField(userBean, "sessionId", "user-1");

        assertTrue(getUserEntityFails(userBean));
    }

    @Test
    void getResultsHistoryReturnsDatabasePoints() throws Exception {
        PointEntity point = new PointEntity();
        UserEntity userEntity = user("user-1", "Firefox");
        UserDatabaseService databaseService = new UserDatabaseService();
        databaseService.points = List.of(point);
        UserBean userBean = userBean(databaseService);

        setField(userBean, "userEntity", userEntity);
        TestFacesContext.set(new TestFacesContext(request(new Cookie[] {new Cookie("userId", "user-1")}, "Firefox")));

        assertEquals(List.of(point), userBean.getResultsHistory());
        assertEquals("user-1", databaseService.pointsUserId);
    }

    @Test
    void getResultsHistoryCreatesUserEntityWhenItIsMissing() throws Exception {
        PointEntity point = new PointEntity();
        UserEntity userEntity = user("user-1", "Firefox");
        UserDatabaseService databaseService = new UserDatabaseService();
        databaseService.user = userEntity;
        databaseService.points = List.of(point);
        UserBean userBean = userBean(databaseService);

        TestFacesContext.set(new TestFacesContext(request(new Cookie[] {new Cookie("userId", "user-1")}, "Firefox")));

        assertEquals(List.of(point), userBean.getResultsHistory());
    }

    @Test
    void getResultsHistoryReturnsEmptyListOnSqlException() throws Exception {
        UserDatabaseService databaseService = new UserDatabaseService();
        databaseService.fail = true;
        UserBean userBean = userBean(databaseService);

        setField(userBean, "userEntity", user("user-1", "Firefox"));
        TestFacesContext.set(new TestFacesContext(request(new Cookie[] {new Cookie("userId", "user-1")}, "Firefox")));

        assertTrue(userBean.getResultsHistory().isEmpty());
    }

    private static boolean getUserEntityFails(UserBean userBean) {
        try {
            userBean.getUserEntity();
            return false;
        } catch (RuntimeException exception) {
            return true;
        }
    }

}
