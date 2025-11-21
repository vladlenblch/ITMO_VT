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
import org.example.ml.ModelManager;
import jakarta.inject.Inject;

import java.io.IOException;
import java.time.LocalDateTime;

@WebServlet(name = "AreaCheckServlet", urlPatterns = {"/area"})
public class AreaCheckServlet extends HttpServlet {

    @Inject
    private ResultsBean bean;
    
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
        try {
            Params params = Params.fromRequest(req);
            int x = params.getX();
            double y = params.getY();
            int r = params.getR();

            double hitProbability = 0.5;
            if (modelManager != null) {
                hitProbability = modelManager.predictHitProbability(x, y, r);
            }

            boolean hit = AreaChecker.isInside(x, y, r);

            Result result = new Result(x, y, r, hit, LocalDateTime.now());

            ResultsBean usedBean = bean;
            if (usedBean == null) {
                usedBean = getResultsBeanFallback(req);
            }
            usedBean.addResult(result);
            
            if (modelManager != null) {
                try {
                    modelManager.saveTrainingData(result);
                } catch (IOException e) {
                    System.err.println("Ошибка при сохранении данных: " + e.getMessage());
                }
            }

            req.getSession().setAttribute("lastResult", result);
            req.getSession().setAttribute("hitProbability", hitProbability);
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
