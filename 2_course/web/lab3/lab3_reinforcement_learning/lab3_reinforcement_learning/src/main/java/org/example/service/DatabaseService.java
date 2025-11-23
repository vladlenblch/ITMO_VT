package org.example.service;

import org.example.entities.PointEntity;
import jakarta.annotation.PostConstruct;
import jakarta.annotation.PreDestroy;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Named;

import java.io.InputStream;
import java.io.Serializable;
import java.sql.*;
import java.util.ArrayList;
import java.util.ArrayDeque;
import java.util.Deque;
import java.util.List;
import java.util.Properties;

@Named("databaseService")
@ApplicationScoped
public class DatabaseService implements Serializable {

    private static final long serialVersionUID = 1L;
    private Connection connection;
    private String dbUrl;
    private String dbUser;
    private String dbPassword;
    private final Deque<Long> requestTimestamps = new ArrayDeque<>();

    @PostConstruct
    public void init() {
        try {
            loadDatabaseConfig();
            Class.forName("org.postgresql.Driver");
            connection = DriverManager.getConnection(dbUrl, dbUser, dbPassword);
            createTablesIfNotExist();
            System.out.println("DatabaseService initialized successfully. URL: " + dbUrl);
        } catch (Exception e) {
            System.err.println("Failed to initialize database connection: " + e.getMessage());
            e.printStackTrace();

        }
    }

    private void loadDatabaseConfig() {
        try (InputStream input = getClass().getClassLoader().getResourceAsStream("db.cfg")) {
            if (input == null) {
                dbUrl = "jdbc:postgresql://localhost:5432/studs";
                dbUser = "postgres";
                dbPassword = "postgres";
                return;
            }
            
            Properties props = new Properties();
            props.load(input);
            
            dbUrl = props.getProperty("db.url", "jdbc:postgresql://localhost:5432/studs");
            dbUser = props.getProperty("db.user", "postgres");
            dbPassword = props.getProperty("db.password", "postgres");
        } catch (Exception e) {
            dbUrl = "jdbc:postgresql://localhost:5432/studs";
            dbUser = "postgres";
            dbPassword = "postgres";
        }
    }

    @PreDestroy
    public void destroy() {
        try {
            if (connection != null && !connection.isClosed()) {
                connection.close();
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    private void createTablesIfNotExist() throws SQLException {
        try (Statement stmt = connection.createStatement()) {
            stmt.execute("""
                CREATE TABLE IF NOT EXISTS results (
                    id SERIAL PRIMARY KEY,
                    x NUMERIC(10, 3) NOT NULL,
                    y NUMERIC(10, 3) NOT NULL,
                    r NUMERIC(10, 3) NOT NULL,
                    hit BOOLEAN NOT NULL,
                    request_time TIMESTAMP NOT NULL,
                    execution_time BIGINT NOT NULL
                )
            """);
        }
    }

    public Connection getConnection() {
        try {
            if (connection == null || connection.isClosed()) {
                loadDatabaseConfig();
                Class.forName("org.postgresql.Driver");
                connection = DriverManager.getConnection(dbUrl, dbUser, dbPassword);
                createTablesIfNotExist();
            }
        } catch (Exception e) {
            System.err.println("Database connection error: " + e.getMessage());
            e.printStackTrace();
            throw new RuntimeException("Database connection error", e);
        }
        return connection;
    }

    public void savePoint(PointEntity point) throws SQLException {
        registerDbAccess();
        String sql = "INSERT INTO results (x, y, r, hit, request_time, execution_time) VALUES (?, ?, ?, ?, ?, ?)";
        try (PreparedStatement pstmt = getConnection().prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
            pstmt.setBigDecimal(1, point.getX());
            pstmt.setBigDecimal(2, point.getY());
            pstmt.setBigDecimal(3, point.getR());
            pstmt.setBoolean(4, point.getHit());
            pstmt.setTimestamp(5, new Timestamp(point.getCurrentTime().getTime()));
            pstmt.setLong(6, point.getExecutionTime());
            pstmt.executeUpdate();
            
            try (ResultSet rs = pstmt.getGeneratedKeys()) {
                if (rs.next()) {
                    point.setId(rs.getInt(1));
                }
            }
        }
    }

    public List<PointEntity> getAllPoints() throws SQLException {
        registerDbAccess();
        String sql = "SELECT id, x, y, r, hit, request_time, execution_time FROM results ORDER BY request_time DESC";
        List<PointEntity> points = new ArrayList<>();
        try (PreparedStatement pstmt = getConnection().prepareStatement(sql)) {
            try (ResultSet rs = pstmt.executeQuery()) {
                while (rs.next()) {
                    PointEntity point = new PointEntity();
                    point.setId(rs.getInt("id"));
                    point.setX(rs.getBigDecimal("x"));
                    point.setY(rs.getBigDecimal("y"));
                    point.setR(rs.getBigDecimal("r"));
                    point.setHit(rs.getBoolean("hit"));
                    point.setCurrentTime(new java.util.Date(rs.getTimestamp("request_time").getTime()));
                    point.setExecutionTime(rs.getLong("execution_time"));
                    points.add(point);
                }
            }
        }
        return points;
    }

    public int countHitsLast(int limit) throws SQLException {
        registerDbAccess();
        String sql = "SELECT hit FROM results ORDER BY request_time DESC LIMIT ?";
        int hits = 0;
        try (PreparedStatement pstmt = getConnection().prepareStatement(sql)) {
            pstmt.setInt(1, limit);
            try (ResultSet rs = pstmt.executeQuery()) {
                while (rs.next()) {
                    if (rs.getBoolean("hit")) {
                        hits++;
                    }
                }
            }
        }
        return hits;
    }

    public int getDbRequestsLastMinute() {
        long now = System.currentTimeMillis();
        cleanupOldRequests(now);
        synchronized (requestTimestamps) {
            return requestTimestamps.size();
        }
    }

    private void registerDbAccess() {
        long now = System.currentTimeMillis();
        synchronized (requestTimestamps) {
            requestTimestamps.addLast(now);
            cleanupOldRequests(now);
        }
    }

    private void cleanupOldRequests(long now) {
        long threshold = now - 60_000;
        synchronized (requestTimestamps) {
            while (!requestTimestamps.isEmpty() && requestTimestamps.peekFirst() < threshold) {
                requestTimestamps.removeFirst();
            }
        }
    }
}
