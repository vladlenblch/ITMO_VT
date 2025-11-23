package org.example.beans;

import org.example.entities.PointEntity;
import org.example.service.DatabaseService;
import org.example.service.KafkaService;

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
    private int shotCounter = 0;

    @Inject
    private DatabaseService databaseService;

    @Inject
    private KafkaService kafkaService;

    public List<PointEntity> getAllResults() {
        try {
            return databaseService.getAllPoints();
        } catch (SQLException e) {
            e.printStackTrace();
            return new ArrayList<>();
        }
    }

    public int getRequestsPerMinute() {
        return databaseService.getDbRequestsLastMinute();
    }

    public void addResult(PointEntity point) {
        try {
            databaseService.savePoint(point);
            shotCounter++;
            if (shotCounter % 5 == 0) {
                int hitsLast10 = databaseService.countHitsLast(10);
                kafkaService.sendState(hitsLast10, point.getR());
            }
        } catch (SQLException e) {
            throw new RuntimeException("Failed to add result", e);
        }
    }
}
