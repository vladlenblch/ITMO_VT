package org.example.entities;

import org.junit.jupiter.api.*;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

class PointEntityTest {

    @Test
    void gettersReturnSetValues() {
        Date currentTime = new Date(1000);
        UserEntity user = new UserEntity();
        PointEntity point = new PointEntity();

        point.setId(1);
        point.setX(1.5);
        point.setY(-2.5);
        point.setR(3.0);
        point.setHit(true);
        point.setCurrentTime(currentTime);
        point.setExecutionTime(42L);
        point.setUser(user);

        assertEquals(1, point.getId());
        assertEquals(1.5, point.getX());
        assertEquals(-2.5, point.getY());
        assertEquals(3.0, point.getR());
        assertEquals(true, point.getHit());
        assertEquals(currentTime, point.getCurrentTime());
        assertEquals(42L, point.getExecutionTime());
        assertEquals(user, point.getUser());
    }

    @Test
    void pointsWithSameIdAreEqual() {
        PointEntity first = point(1);
        PointEntity second = point(1);

        assertEquals(first, second);
    }

    @Test
    void pointsWithDifferentIdsAreNotEqual() {
        assertNotEquals(point(1), point(2));
    }

    @Test
    void pointIsEqualToItself() {
        PointEntity point = point(1);

        assertEquals(point, point);
    }

    @Test
    void pointIsNotEqualToNull() {
        assertNotEquals(point(1), null);
    }

    @Test
    void pointIsNotEqualToOtherClass() {
        assertNotEquals(point(1), "1");
    }

    @Test
    void pointsWithNullIdsAreNotEqual() {
        assertNotEquals(point(null), point(null));
    }

    @Test
    void pointWithIdHasIdHashCode() {
        PointEntity point = point(1);

        assertEquals(Integer.valueOf(1).hashCode(), point.hashCode());
    }

    @Test
    void pointWithNullIdHasZeroHashCode() {
        assertEquals(0, point(null).hashCode());
    }

    private static PointEntity point(Integer id) {
        PointEntity point = new PointEntity();
        point.setId(id);
        return point;
    }
}
