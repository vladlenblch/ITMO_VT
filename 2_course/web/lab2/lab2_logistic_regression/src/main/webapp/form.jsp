<%@ page contentType="text/html; charset=UTF-8" language="java" %>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<%@ taglib prefix="fmt" uri="jakarta.tags.fmt" %>
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8" />
    <title>lab2</title>
    <link rel="stylesheet" href="style.css" />
</head>
<body>
<nav class="navbar">
    <div id="info">
        Ларионов Владислав Васильевич<br/>P3209, 745
    </div>
</nav>
<main class="container">
    <section class="top-section">
        <div class="input-panel">
            <form id="data-form" action="<%= request.getContextPath() %>/controller" method="GET" novalidate>
                <div id="xs">
                    <label>Выберите X:</label>
                    <div class="checkbox-group">
                        <c:set var="selX" value="${param.x != null ? param.x : requestScope.x}" />
                        <label><input type="checkbox" name="x" value="-3" <c:if test="${selX == '-3'}">checked</c:if> > -3</label>
                        <label><input type="checkbox" name="x" value="-2" <c:if test="${selX == '-2'}">checked</c:if> > -2</label>
                        <label><input type="checkbox" name="x" value="-1" <c:if test="${selX == '-1'}">checked</c:if> > -1</label>
                        <label><input type="checkbox" name="x" value="0"  <c:if test="${selX == '0'}">checked</c:if> > 0</label>
                        <label><input type="checkbox" name="x" value="1"  <c:if test="${selX == '1'}">checked</c:if> > 1</label>
                        <label><input type="checkbox" name="x" value="2"  <c:if test="${selX == '2'}">checked</c:if> > 2</label>
                        <label><input type="checkbox" name="x" value="3"  <c:if test="${selX == '3'}">checked</c:if> > 3</label>
                        <label><input type="checkbox" name="x" value="4"  <c:if test="${selX == '4'}">checked</c:if> > 4</label>
                        <label><input type="checkbox" name="x" value="5"  <c:if test="${selX == '5'}">checked</c:if> > 5</label>
                    </div>
                </div>

                <label for="y">Введите Y:</label>
                <input type="text" id="y" name="y" placeholder="(-5, 3)" value="${param.y != null ? param.y : requestScope.y}" />

                <label for="r">Выберите R:</label>
                <c:set var="selR" value="${param.r != null ? param.r : requestScope.r != null ? requestScope.r : '1'}" />
                <div id="r" class="r-radio-group">
                    <label><input type="radio" name="r" value="1" <c:if test="${selR == '1'}">checked</c:if> > <span>1</span></label>
                    <label><input type="radio" name="r" value="2" <c:if test="${selR == '2'}">checked</c:if> > <span>2</span></label>
                    <label><input type="radio" name="r" value="3" <c:if test="${selR == '3'}">checked</c:if> > <span>3</span></label>
                    <label><input type="radio" name="r" value="4" <c:if test="${selR == '4'}">checked</c:if> > <span>4</span></label>
                    <label><input type="radio" name="r" value="5" <c:if test="${selR == '5'}">checked</c:if> > <span>5</span></label>
                </div>

                <button type="submit">Проверить</button>
                <div id="error" class="error-text" ${not empty requestScope.error ? '' : 'hidden'}>
                    <c:out value="${requestScope.error}" />
                </div>
                <c:if test="${not empty requestScope.predictedProbability}">
                    <div style="margin-top: 15px; padding: 12px; background-color: #2c3e50; border-radius: 8px; border: 1px solid #4A90E2;">
                        <p style="font-size: 1rem; color: #e8f4fd; margin: 0;">
                            Вероятность попадания: 
                            <strong style="color: #2ecc71;">
                                <fmt:formatNumber value="${requestScope.predictedProbability * 100}" maxFractionDigits="1" />%
                            </strong>
                        </p>
                    </div>
                </c:if>
            </form>
        </div>
        <div class="graph-panel">
            <canvas id="graph" width="400" height="400"></canvas>
        </div>
    </section>
    <section class="table-section">
        <table id="result-table">
            <tr>
                <th>X</th><th>Y</th><th>R</th><th>Время</th><th>Результат</th>
            </tr>
            <c:if test="${not empty resultsBean}">
                <c:forEach items="${resultsBean.results}" var="r">
                    <tr class="${r.hit ? 'hit-row' : 'miss-row'}">
                        <td><c:out value="${r.x}" /></td>
                        <td><c:out value="${r.y}" /></td>
                        <td><c:out value="${r.r}" /></td>
                        <td><c:out value="${r.formattedTime}" /></td>
                        <td><c:out value="${r.hit ? 'Попадание' : 'Промах'}" /></td>
                    </tr>
                </c:forEach>
            </c:if>
        </table>
    </section>
</main>
<script src="index.js" defer></script>
</body>
</html>