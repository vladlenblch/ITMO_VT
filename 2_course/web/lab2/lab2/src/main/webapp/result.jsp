<%@ page contentType="text/html; charset=UTF-8" language="java" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%
%>
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8" />
    <title>Результат проверки</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/style.css" />
</head>
<body>
<nav class="navbar">
    <div id="info">
        Ларионов Владислав Васильевич<br/>P3209, 466468
    </div>
</nav>
<main class="container">

<table id="result-table">
    <thead>
    <tr>
        <th>X</th>
        <th>Y</th>
        <th>R</th>
        <th>Время</th>
        <th>Результат</th>
    </tr>
    </thead>
    <tbody>
    <c:choose>
        <c:when test="${not empty requestScope.result}">
            <tr>
                <td><c:out value="${requestScope.result.x}" /></td>
                <td><c:out value="${requestScope.result.y}" /></td>
                <td><c:out value="${requestScope.result.r}" /></td>
                <td><c:out value="${requestScope.result.formattedTime}" /></td>
                <td><c:out value="${requestScope.result.hit ? 'Попадание' : 'Промах'}" /></td>
            </tr>
        </c:when>
        <c:otherwise>
            <tr>
                <td colspan="5">Результат не найден. Вернитесь на форму и отправьте запрос.</td>
            </tr>
        </c:otherwise>
    </c:choose>
    </tbody>
</table>
<p><a href="<%= request.getContextPath() %>/controller">Вернуться на форму</a></p>
</main>
</body>
</html>