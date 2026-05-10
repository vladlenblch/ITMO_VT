package org.example;

import jakarta.faces.context.*;
import jakarta.servlet.http.*;

import java.util.*;

public class TestExternalContext extends ExternalContextWrapper {

    private final HttpServletRequest request;
    public String responseCookieName;
    public String responseCookieValue;

    public TestExternalContext(HttpServletRequest request) {
        this.request = request;
    }

    @Override
    public ExternalContext getWrapped() {
        return null;
    }

    @Override
    public Object getRequest() {
        return request;
    }

    @Override
    public void addResponseCookie(String name, String value, Map<String, Object> properties) {
        this.responseCookieName = name;
        this.responseCookieValue = value;
    }
}
