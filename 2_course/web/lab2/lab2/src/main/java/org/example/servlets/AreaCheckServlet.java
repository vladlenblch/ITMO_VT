package org.example.servlets;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.example.model.ResultsBean;
import org.example.model.Result;
import org.example.model.AreaChecker;
import org.example.model.Params;
import org.example.model.ValidationException;
import jakarta.inject.Inject;

import java.io.IOException;
import java.time.LocalDateTime;

@WebServlet(name = "AreaCheckServlet", urlPatterns = {"/area"})
public class AreaCheckServlet extends HttpServlet {

    @Inject
    private ResultsBean bean;

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        try {
            Params params = Params.fromRequest(req);
            int x = params.getX();
            double y = params.getY();
            int r = params.getR();

            boolean hit = AreaChecker.isInside(x, y, r);

            Result result = new Result(x, y, r, hit, LocalDateTime.now());

            ResultsBean usedBean = bean;
            if (usedBean == null) {
                usedBean = getResultsBeanFallback(req);
            }
            usedBean.addResult(result);

            req.getSession().setAttribute("lastResult", result);
            resp.sendRedirect(req.getContextPath() + "/result");
        } catch (ValidationException e) {
            req.setAttribute("error", e.getMessage());
            req.getRequestDispatcher("/form.jsp").forward(req, resp);
        }
    }

    private ResultsBean getResultsBeanFallback(HttpServletRequest req) {
        Object attr = req.getServletContext().getAttribute("resultsBean");
        if (attr instanceof ResultsBean) {
            return (ResultsBean) attr;
        }

        ResultsBean newBean = new ResultsBean();
        req.getServletContext().setAttribute("resultsBean", newBean);
        return newBean;
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        doGet(req, resp);
    }
}
