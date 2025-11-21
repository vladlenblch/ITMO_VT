package org.example.model;

import jakarta.servlet.http.HttpServletRequest;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.stream.Collectors;

public class Params {
    private final int x;
    private final double y;
    private final int r;

    public Params(String query) throws ValidationException {
        if (query == null || query.isEmpty()) {
            throw new ValidationException("Отсутствует строка запроса");
        }
        var params = splitQuery(query);
        validateParams(params);
        this.x = Integer.parseInt(params.get("x"));
        this.y = Double.parseDouble(params.get("y"));
        this.r = Integer.parseInt(params.get("r"));
    }

    public static Params fromRequest(HttpServletRequest req) throws ValidationException {
        Map<String, String> params = new HashMap<>();
        params.put("x", req.getParameter("x"));
        params.put("y", req.getParameter("y"));
        params.put("r", req.getParameter("r"));
        validateParams(params);
        int x = Integer.parseInt(params.get("x"));
        double y = Double.parseDouble(params.get("y"));
        int r = Integer.parseInt(params.get("r"));
        return new Params(x, y, r);
    }

    private Params(int x, double y, int r) {
        this.x = x;
        this.y = y;
        this.r = r;
    }

    private static Map<String, String> splitQuery(String query) {
        return Arrays.stream(query.split("&"))
                .map(pair -> pair.split("=", 2))
                .filter(parts -> parts.length >= 1 && parts[0] != null && !parts[0].isEmpty())
                .collect(Collectors.toMap(
                        pairParts -> URLDecoder.decode(pairParts[0], StandardCharsets.UTF_8),
                        pairParts -> pairParts.length == 2 ? URLDecoder.decode(pairParts[1], StandardCharsets.UTF_8) : "",
                        (a, b) -> b,
                        HashMap::new
                ));
    }


    private static void validateParams(Map<String, String> params) throws ValidationException {
        var x = params.get("x");
        if (x == null || x.isEmpty()) {
            throw new ValidationException("X недействителен");
        }

        try {
            var xx = Integer.parseInt(x);
            if (xx < -3 || xx > 5) {
                throw new ValidationException("X - некорректное значение");
            }
        } catch (NumberFormatException e) {
            throw new ValidationException("X не является числом");
        }

        var y = params.get("y");
        if (y == null || y.isEmpty()) {
            throw new ValidationException("Y недействителен");
        }

        try {
            var yy = Double.parseDouble(y);
            if (!(yy > -5 && yy < 3)) {
                throw new ValidationException("Y - некорректное значение");
            }
        } catch (NumberFormatException e) {
            throw new ValidationException("Y не является числом");
        }

        var r = params.get("r");
        if (r == null || r.isEmpty()) {
            throw new ValidationException("R недействителен");
        }

        try {
            var rr = Integer.parseInt(r);
            if (rr < 1 || rr > 5) {
                throw new ValidationException("R - некорректное значение");
            }
        } catch (NumberFormatException e) {
            throw new ValidationException("R не является числом");
        }
    }


    public int getX() {
        return x;
    }

    public double getY() {
        return y;
    }

    public int getR() {
        return r;
    }
}
