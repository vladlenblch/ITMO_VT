package org.example.servlets;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.inject.Inject;
import org.example.model.ResultsBean;
import org.example.ml.ModelManager;

import java.io.IOException;

@WebServlet(name = "ControllerServlet", urlPatterns = {"/controller"})
public class ControllerServlet extends HttpServlet {

    @Inject
    private ResultsBean resultsBean;
    
    private ModelManager modelManager;
    
    @Override
    public void init() throws ServletException {
        super.init();
        try {
            modelManager = new ModelManager();
            String basePath = getStoragePath();
            modelManager.setPaths(basePath + "/hit_prediction.model", basePath + "/training_data.csv");
            modelManager.loadOrCreateModel();
        } catch (IOException e) {
            System.err.println("Ошибка при инициализации модели: " + e.getMessage());
            modelManager = null;
        }
    }
    
    private String getStoragePath() {
        String jbossHome = System.getProperty("jboss.server.data.dir");
        if (jbossHome != null) {
            String appName = getServletContext().getContextPath().replace("/", "");
            if (appName.isEmpty()) appName = "lab2_logistic_regression";
            return jbossHome + "/" + appName;
        }
        
        String realPath = getServletContext().getRealPath("/WEB-INF/data");
        if (realPath != null) {
            return realPath;
        }
        
        String tmpDir = System.getProperty("java.io.tmpdir");
        String appName = getServletContext().getContextPath().replace("/", "");
        if (appName.isEmpty()) appName = "lab2_logistic_regression";
        return tmpDir + "/" + appName;
    }

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
            
            if (modelManager != null && x != null && y != null && r != null && 
                !x.isEmpty() && !y.isEmpty() && !r.isEmpty()) {
                try {
                    double probability = modelManager.predictHitProbability(
                        Integer.parseInt(x), Double.parseDouble(y), Integer.parseInt(r));
                    req.setAttribute("predictedProbability", probability);
                } catch (NumberFormatException e) {
                    // игнорируем ошибки парсинга
                }
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
