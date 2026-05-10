package org.example.entities;

import org.junit.jupiter.api.*;

import static org.junit.jupiter.api.Assertions.*;

class UserEntityTest {

    @Test
    void gettersReturnSetValues() {
        UserEntity user = new UserEntity();

        user.setId("user-1");
        user.setUserAgent("Firefox");

        assertEquals("user-1", user.getId());
        assertEquals("Firefox", user.getUserAgent());
    }

    @Test
    void usersWithSameIdAreEqual() {
        UserEntity first = user("user-1");
        UserEntity second = user("user-1");

        assertEquals(first, second);
    }

    @Test
    void usersWithDifferentIdsAreNotEqual() {
        assertNotEquals(user("user-1"), user("user-2"));
    }

    @Test
    void userIsEqualToItself() {
        UserEntity user = user("user-1");

        assertEquals(user, user);
    }

    @Test
    void userIsNotEqualToNull() {
        assertNotEquals(user("user-1"), null);
    }

    @Test
    void userIsNotEqualToOtherClass() {
        assertNotEquals(user("user-1"), "user-1");
    }

    @Test
    void usersWithNullIdsAreNotEqual() {
        assertNotEquals(user(null), user(null));
    }

    @Test
    void userWithIdHasIdHashCode() {
        UserEntity user = user("user-1");

        assertEquals("user-1".hashCode(), user.hashCode());
    }

    @Test
    void userWithNullIdHasZeroHashCode() {
        assertEquals(0, user(null).hashCode());
    }

    @Test
    void toStringContainsIdAndUserAgent() {
        UserEntity user = new UserEntity();

        user.setId("user-1");
        user.setUserAgent("Firefox");

        assertEquals("user-1 | Firefox", user.toString());
    }

    private static UserEntity user(String id) {
        UserEntity user = new UserEntity();
        user.setId(id);
        return user;
    }
}
