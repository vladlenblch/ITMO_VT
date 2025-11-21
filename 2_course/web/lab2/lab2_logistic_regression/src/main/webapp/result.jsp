<%@ page contentType="text/html; charset=UTF-8" language="java" %>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<%@ taglib prefix="fmt" uri="jakarta.tags.fmt" %>
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
            <tr class="${requestScope.result.hit ? 'hit-row' : 'miss-row'}">
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
<c:if test="${not empty requestScope.hitProbability}">
    <div style="margin-top: 20px; padding: 15px; background-color: #2c3e50; border-radius: 8px; border: 1px solid #4A90E2;">
        <h3 style="color: #64B5F6; margin-top: 0;">Прогноз модели</h3>
        <p style="font-size: 1.2rem; color: #e8f4fd;">
            Вероятность попадания при следующем выстреле: 
            <strong style="color: #2ecc71;">
                <fmt:formatNumber value="${requestScope.hitProbability * 100}" maxFractionDigits="1" />%
            </strong>
        </p>
    </div>
</c:if>
<p><a href="<%= request.getContextPath() %>/controller">Вернуться на форму</a></p>
</main>
</body>
</html>