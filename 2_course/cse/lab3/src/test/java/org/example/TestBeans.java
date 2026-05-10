package org.example;

import org.example.beans.*;
import org.example.entities.*;
import org.example.service.*;

import java.sql.*;
import java.util.*;

import static org.example.TestFields.*;

public final class TestBeans {

    private TestBeans() {
    }

    public static PointBean pointBean(UserBean userBean, ResultsBean resultsBean) throws Exception {
        PointBean pointBean = new PointBean();
        setField(pointBean, "userBean", userBean);
        setField(pointBean, "resultsBean", resultsBean);
        return pointBean;
    }

    public static ResultsBean resultsBean(DatabaseService databaseService) throws Exception {
        ResultsBean resultsBean = new ResultsBean();
        setField(resultsBean, "databaseService", databaseService);
        return resultsBean;
    }

    public static UserBean userBean(DatabaseService databaseService) throws Exception {
        UserBean userBean = new UserBean();
        setField(userBean, "databaseService", databaseService);
        return userBean;
    }

    public static UserEntity user(String id, String userAgent) {
        UserEntity user = new UserEntity();
        user.setId(id);
        user.setUserAgent(userAgent);
        return user;
    }

    public static class FakeUserBean extends UserBean {

        private final UserEntity user;

        public FakeUserBean(UserEntity user) {
            this.user = user;
        }

        @Override
        public UserEntity getUserEntity() {
            return user;
        }
    }

    public static class FakeResultsBean extends ResultsBean {

        public PointEntity savedPoint;
        public boolean fail;

        @Override
        public void addResult(PointEntity point) {
            if (fail) {
                throw new RuntimeException("fail");
            }
            this.savedPoint = point;
        }
    }

    public static class ResultsDatabaseService extends DatabaseService {

        private final List<PointEntity> points;
        private final boolean fail;
        public PointEntity savedPoint;

        public ResultsDatabaseService(List<PointEntity> points, boolean fail) {
            this.points = points;
            this.fail = fail;
        }

        @Override
        public List<PointEntity> getAllPoints() throws SQLException {
            if (fail) {
                throw new SQLException("fail");
            }
            return points;
        }

        @Override
        public void savePoint(PointEntity point) throws SQLException {
            if (fail) {
                throw new SQLException("fail");
            }
            this.savedPoint = point;
        }
    }

    public static class UserDatabaseService extends DatabaseService {

        public UserEntity user;
        public UserEntity savedUser;
        public List<PointEntity> points = List.of();
        public String pointsUserId;
        public boolean fail;

        @Override
        public UserEntity findUser(String userId) throws SQLException {
            if (fail) {
                throw new SQLException("fail");
            }
            return user;
        }

        @Override
        public void saveUser(UserEntity user) throws SQLException {
            if (fail) {
                throw new SQLException("fail");
            }
            this.savedUser = user;
        }

        @Override
        public List<PointEntity> getPointsByUser(String userId) throws SQLException {
            if (fail) {
                throw new SQLException("fail");
            }
            this.pointsUserId = userId;
            return points;
        }
    }
}
