package org.example.servlets;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.inject.Inject;
import org.example.model.ResultsBean;

import java.io.IOException;

@WebServlet(name = "ControllerServlet", urlPatterns = {"/controller"})
public class ControllerServlet extends HttpServlet {

    @Inject
    private ResultsBean resultsBean;

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String x = req.getParameter("x");
        String y = req.getParameter("y");
        String r = req.getParameter("r");

        if (x != null && y != null && r != null && !x.isEmpty() && !y.isEmpty() && !r.isEmpty()) {
            req.getRequestDispatcher("/area").forward(req, resp);
        } else {
            ResultsBean usedBean = resultsBean;
            if (usedBean == null) {
                usedBean = getResultsBeanFallback(req);
            }
            if (usedBean != null) {
                req.setAttribute("resultsBean", usedBean);
            }
            req.getRequestDispatcher("/form.jsp").forward(req, resp);
        }
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        doGet(req, resp);
    }

    private ResultsBean getResultsBeanFallback(HttpServletRequest req) {
        Object attr = req.getServletContext().getAttribute("resultsBean");
        if (attr instanceof ResultsBean) return (ResultsBean) attr;

        ResultsBean newBean = new ResultsBean();
        req.getServletContext().setAttribute("resultsBean", newBean);
        return newBean;
    }
}
