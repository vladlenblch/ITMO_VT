package org.example.servlets;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.example.model.Result;

import java.io.IOException;

@WebServlet(name = "ResultServlet", urlPatterns = {"/result"})
public class ResultServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        Object obj = req.getSession().getAttribute("lastResult");
        if (obj instanceof Result) {
            req.setAttribute("result", obj);
            req.getRequestDispatcher("/result.jsp").forward(req, resp);
        } else {
            resp.sendRedirect(req.getContextPath() + "/controller");
        }
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        doGet(req, resp);
    }
}
