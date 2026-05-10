package org.example;

import org.example.entities.*;
import org.example.service.*;

import java.lang.reflect.*;
import java.sql.*;
import java.util.*;
import java.util.logging.*;

import static org.example.TestFields.*;

public final class TestDatabase {

    private TestDatabase() {
    }

    public static DatabaseService serviceWithConnection() throws Exception {
        DatabaseService service = new DatabaseServiceWithConnectionField();
        FakeConnection connection = new FakeConnection();
        setField(service, "connection", connection.proxy);
        setField(service, "connectionHandler", connection);
        return service;
    }

    public static PointEntity point() {
        UserEntity user = new UserEntity();
        user.setId("u1");
        PointEntity point = new PointEntity();
        point.setX(1.5);
        point.setY(-2.5);
        point.setR(3.0);
        point.setHit(true);
        point.setCurrentTime(new java.util.Date(1000));
        point.setExecutionTime(15L);
        point.setUser(user);
        return point;
    }

    public static Map<Object, Object> pointRow() {
        return row(
                "id", 7,
                "x", 1.5,
                "y", -2.5,
                "r", 3.0,
                "hit", true,
                "request_time", new Timestamp(1000),
                "execution_time", 15L
        );
    }

    public static Map<Object, Object> row(Object... values) {
        Map<Object, Object> row = new HashMap<>();
        int index = 0;
        while (index < values.length) {
            row.put(values[index], values[index + 1]);
            index += 2;
        }
        return row;
    }

    private static Object defaultValue(Class<?> type) {
        if (type == boolean.class) {
            return false;
        }
        if (type == int.class) {
            return 0;
        }
        if (type == long.class) {
            return 0L;
        }
        if (type == double.class) {
            return 0.0;
        }
        return null;
    }

    public static class DatabaseServiceWithConnectionField extends DatabaseService {
        public FakeConnection connectionHandler;
    }

    public static class FakeDriver implements Driver {

        public final List<FakeConnection> connections = new ArrayList<>();

        @Override
        public Connection connect(String url, Properties info) throws SQLException {
            if (!acceptsURL(url)) {
                return null;
            }
            FakeConnection connection = new FakeConnection();
            connections.add(connection);
            return connection.proxy;
        }

        @Override
        public boolean acceptsURL(String url) {
            return url != null && url.startsWith("jdbc:postgresql:");
        }

        @Override
        public DriverPropertyInfo[] getPropertyInfo(String url, Properties info) {
            return new DriverPropertyInfo[0];
        }

        @Override
        public int getMajorVersion() {
            return 1;
        }

        @Override
        public int getMinorVersion() {
            return 0;
        }

        @Override
        public boolean jdbcCompliant() {
            return false;
        }

        @Override
        public Logger getParentLogger() {
            return Logger.getGlobal();
        }

        public FakeConnection lastConnection() {
            return connections.get(connections.size() - 1);
        }
    }

    public static class FakeConnection implements InvocationHandler {

        public final List<String> statements = new ArrayList<>();
        public final List<FakePreparedStatement> preparedStatements = new ArrayList<>();
        public final Queue<List<Map<Object, Object>>> queryRows = new ArrayDeque<>();
        public final List<Map<Object, Object>> generatedKeyRows = new ArrayList<>();
        public final Connection proxy;
        public boolean closed;

        public FakeConnection() {
            this.proxy = (Connection) Proxy.newProxyInstance(
                    Connection.class.getClassLoader(),
                    new Class[]{Connection.class},
                    this
            );
        }

        @Override
        public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
            String name = method.getName();
            if ("createStatement".equals(name)) {
                return Proxy.newProxyInstance(
                        Statement.class.getClassLoader(),
                        new Class[]{Statement.class},
                        new FakeStatement(this)
                );
            }
            if ("prepareStatement".equals(name)) {
                FakePreparedStatement statement = new FakePreparedStatement(this, (String) args[0]);
                preparedStatements.add(statement);
                return Proxy.newProxyInstance(
                        PreparedStatement.class.getClassLoader(),
                        new Class[]{PreparedStatement.class},
                        statement
                );
            }
            if ("isClosed".equals(name)) {
                return closed;
            }
            if ("close".equals(name)) {
                closed = true;
                return null;
            }
            if ("toString".equals(name)) {
                return "FakeConnection";
            }
            return defaultValue(method.getReturnType());
        }
    }

    public static class FakePreparedStatement implements InvocationHandler {

        public final FakeConnection connection;
        public final String sql;
        public final Map<Integer, Object> params = new HashMap<>();

        public FakePreparedStatement(FakeConnection connection, String sql) {
            this.connection = connection;
            this.sql = sql;
        }

        @Override
        public Object invoke(Object proxy, Method method, Object[] args) {
            String name = method.getName();
            if (name.startsWith("set")) {
                params.put((Integer) args[0], args[1]);
                return null;
            }
            if ("executeUpdate".equals(name)) {
                return 1;
            }
            if ("executeQuery".equals(name)) {
                List<Map<Object, Object>> rows = connection.queryRows.poll();
                if (rows == null) {
                    rows = List.of();
                }
                return resultSet(rows);
            }
            if ("getGeneratedKeys".equals(name)) {
                return resultSet(connection.generatedKeyRows);
            }
            return defaultValue(method.getReturnType());
        }
    }

    public static class FakeStatement implements InvocationHandler {

        private final FakeConnection connection;

        public FakeStatement(FakeConnection connection) {
            this.connection = connection;
        }

        @Override
        public Object invoke(Object proxy, Method method, Object[] args) {
            if ("execute".equals(method.getName())) {
                connection.statements.add((String) args[0]);
                return false;
            }
            return defaultValue(method.getReturnType());
        }
    }

    public static ResultSet resultSet(List<Map<Object, Object>> rows) {
        return (ResultSet) Proxy.newProxyInstance(
                ResultSet.class.getClassLoader(),
                new Class[]{ResultSet.class},
                new FakeResultSet(rows)
        );
    }

    public static class FakeResultSet implements InvocationHandler {

        private final List<Map<Object, Object>> rows;
        private int index = -1;

        public FakeResultSet(List<Map<Object, Object>> rows) {
            this.rows = rows;
        }

        @Override
        public Object invoke(Object proxy, Method method, Object[] args) {
            String name = method.getName();
            if ("next".equals(name)) {
                index++;
                return index < rows.size();
            }
            if ("getString".equals(name)) {
                return value(args[0]);
            }
            if ("getInt".equals(name)) {
                return ((Number) value(args[0])).intValue();
            }
            if ("getDouble".equals(name)) {
                return ((Number) value(args[0])).doubleValue();
            }
            if ("getBoolean".equals(name)) {
                return value(args[0]);
            }
            if ("getTimestamp".equals(name)) {
                return value(args[0]);
            }
            if ("getLong".equals(name)) {
                return ((Number) value(args[0])).longValue();
            }
            return defaultValue(method.getReturnType());
        }

        private Object value(Object key) {
            return rows.get(index).get(key);
        }
    }
}
