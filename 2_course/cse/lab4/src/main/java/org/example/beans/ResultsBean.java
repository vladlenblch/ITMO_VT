package org.example.beans;

import org.example.entities.PointEntity;
import org.example.service.DatabaseService;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.inject.Named;

import java.io.Serializable;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

@Named("resultsBean")
@ApplicationScoped
public class ResultsBean implements Serializable {

    private static final long serialVersionUID = 1L;

    @Inject
    private DatabaseService databaseService;

    public List<PointEntity> getAllResults() {
        try {
            return databaseService.getAllPoints();
        } catch (SQLException e) {
            e.printStackTrace();
            return new ArrayList<>();
        }
    }

    public void addResult(PointEntity point) {
        try {
            databaseService.savePoint(point);
        } catch (SQLException e) {
            throw new RuntimeException("Failed to add result", e);
        }
    }
}
