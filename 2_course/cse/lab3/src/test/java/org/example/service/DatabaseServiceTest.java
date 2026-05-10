package org.example.service;

import org.example.*;
import org.example.entities.*;
import org.junit.jupiter.api.*;

import java.sql.*;
import java.util.*;

import static org.example.TestDatabase.*;
import static org.example.TestFields.*;
import static org.junit.jupiter.api.Assertions.*;

class DatabaseServiceTest {

    private static FakeDriver driver;

    @BeforeAll
    static void registerDriver() throws Exception {
        driver = new FakeDriver();
        DriverManager.registerDriver(driver);
    }

    @AfterAll
    static void deregisterDriver() throws Exception {
        DriverManager.deregisterDriver(driver);
    }

    @BeforeEach
    void resetDriver() {
        driver.connections.clear();
    }

    @Test
    void initLoadsConfigConnectsAndCreatesTables() throws Exception {
        DatabaseService service = new DatabaseService();

        service.init();

        FakeConnection connection = driver.lastConnection();
        assertEquals("jdbc:postgresql://localhost:5432/vlad", getField(service, "dbUrl"));
        assertEquals("postgres", getField(service, "dbUser"));
        assertEquals("postgres", getField(service, "dbPassword"));
        assertSame(connection.proxy, getField(service, "connection"));
        assertEquals(2, connection.statements.size());
        assertTrue(connection.statements.get(0).contains("CREATE TABLE IF NOT EXISTS users"));
        assertTrue(connection.statements.get(1).contains("CREATE TABLE IF NOT EXISTS results"));
    }

    @Test
    void destroyClosesOpenConnection() throws Exception {
        DatabaseService service = new DatabaseService();
        FakeConnection connection = new FakeConnection();
        setField(service, "connection", connection.proxy);

        service.destroy();

        assertTrue(connection.closed);
    }

    @Test
    void getConnectionReturnsExistingOpenConnection() throws Exception {
        DatabaseService service = new DatabaseService();
        FakeConnection connection = new FakeConnection();
        setField(service, "connection", connection.proxy);

        Connection result = service.getConnection();

        assertSame(connection.proxy, result);
        assertTrue(driver.connections.isEmpty());
    }

    @Test
    void getConnectionReconnectsWhenConnectionIsClosed() throws Exception {
        DatabaseService service = new DatabaseService();
        FakeConnection oldConnection = new FakeConnection();
        oldConnection.closed = true;
        setField(service, "connection", oldConnection.proxy);

        Connection result = service.getConnection();

        FakeConnection newConnection = driver.lastConnection();
        assertSame(newConnection.proxy, result);
        assertEquals(2, newConnection.statements.size());
    }

    @Test
    void saveUserExecutesInsert() throws Exception {
        DatabaseService service = serviceWithConnection();
        FakeConnection connection = (FakeConnection) getField(service, "connectionHandler");
        UserEntity user = new UserEntity();
        user.setId("u1");
        user.setUserAgent("agent");

        service.saveUser(user);

        FakePreparedStatement statement = connection.preparedStatements.get(0);
        assertTrue(statement.sql.contains("INSERT INTO users"));
        assertEquals("u1", statement.params.get(1));
        assertEquals("agent", statement.params.get(2));
    }

    @Test
    void findUserReturnsUserWhenRowExists() throws Exception {
        DatabaseService service = serviceWithConnection();
        FakeConnection connection = (FakeConnection) getField(service, "connectionHandler");
        connection.queryRows.add(List.of(row("id", "u1", "useragent", "agent")));

        UserEntity user = service.findUser("u1");

        FakePreparedStatement statement = connection.preparedStatements.get(0);
        assertEquals("u1", statement.params.get(1));
        assertEquals("u1", user.getId());
        assertEquals("agent", user.getUserAgent());
    }

    @Test
    void findUserReturnsNullWhenRowIsMissing() throws Exception {
        DatabaseService service = serviceWithConnection();
        FakeConnection connection = (FakeConnection) getField(service, "connectionHandler");
        connection.queryRows.add(List.of());

        UserEntity user = service.findUser("u1");

        assertNull(user);
    }

    @Test
    void savePointExecutesInsertAndSetsGeneratedId() throws Exception {
        DatabaseService service = serviceWithConnection();
        FakeConnection connection = (FakeConnection) getField(service, "connectionHandler");
        connection.generatedKeyRows.add(row(1, 10));
        PointEntity point = point();

        service.savePoint(point);

        FakePreparedStatement statement = connection.preparedStatements.get(0);
        assertTrue(statement.sql.contains("INSERT INTO results"));
        assertEquals(1.5, statement.params.get(1));
        assertEquals(-2.5, statement.params.get(2));
        assertEquals(3.0, statement.params.get(3));
        assertEquals(true, statement.params.get(4));
        assertEquals(15L, statement.params.get(6));
        assertEquals("u1", statement.params.get(7));
        assertEquals(10, point.getId());
    }

    @Test
    void getPointsByUserReturnsUserPoints() throws Exception {
        DatabaseService service = serviceWithConnection();
        FakeConnection connection = (FakeConnection) getField(service, "connectionHandler");
        connection.queryRows.add(List.of(pointRow()));

        List<PointEntity> points = service.getPointsByUser("u1");

        assertEquals(1, points.size());
        assertEquals(7, points.get(0).getId());
        assertEquals(1.5, points.get(0).getX());
        assertEquals(-2.5, points.get(0).getY());
        assertEquals(3.0, points.get(0).getR());
        assertTrue(points.get(0).getHit());
        assertEquals(15L, points.get(0).getExecutionTime());
        assertEquals("u1", points.get(0).getUser().getId());
    }

}
