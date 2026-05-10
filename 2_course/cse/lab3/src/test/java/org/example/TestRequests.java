package org.example;

import jakarta.servlet.http.*;

import java.lang.reflect.*;

public final class TestRequests {

    private TestRequests() {
    }

    public static HttpServletRequest request(Cookie[] cookies, String userAgent) {
        return (HttpServletRequest) Proxy.newProxyInstance(
                HttpServletRequest.class.getClassLoader(),
                new Class<?>[] {HttpServletRequest.class},
                new InvocationHandler() {
                    @Override
                    public Object invoke(Object proxy, Method method, Object[] args) {
                        if ("getCookies".equals(method.getName())) {
                            return cookies;
                        }
                        if ("getHeader".equals(method.getName())) {
                            return userAgent;
                        }
                        if ("toString".equals(method.getName())) {
                            return "request";
                        }
                        if (method.getReturnType() == boolean.class) {
                            return false;
                        }
                        if (method.getReturnType() == int.class) {
                            return 0;
                        }
                        if (method.getReturnType() == long.class) {
                            return 0L;
                        }
                        return null;
                    }
                }
        );
    }
}
