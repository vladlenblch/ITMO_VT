package org.example.beans;

import org.example.*;
import org.example.entities.*;
import org.junit.jupiter.api.*;

import java.util.*;

import static org.example.TestBeans.*;
import static org.junit.jupiter.api.Assertions.*;

class ResultsBeanTest {

    @Test
    void getAllResultsReturnsDatabasePoints() throws Exception {
        PointEntity point = new PointEntity();
        ResultsBean resultsBean = resultsBean(new ResultsDatabaseService(List.of(point), false));

        assertEquals(List.of(point), resultsBean.getAllResults());
    }

    @Test
    void getAllResultsReturnsEmptyListOnSqlException() throws Exception {
        ResultsBean resultsBean = resultsBean(new ResultsDatabaseService(List.of(), true));

        assertTrue(resultsBean.getAllResults().isEmpty());
    }

    @Test
    void addResultSavesPoint() throws Exception {
        ResultsDatabaseService databaseService = new ResultsDatabaseService(List.of(), false);
        ResultsBean resultsBean = resultsBean(databaseService);
        PointEntity point = new PointEntity();

        resultsBean.addResult(point);

        assertEquals(point, databaseService.savedPoint);
    }

    @Test
    void addResultThrowsRuntimeExceptionOnSqlException() throws Exception {
        ResultsBean resultsBean = resultsBean(new ResultsDatabaseService(List.of(), true));

        assertTrue(addResultFails(resultsBean));
    }

    private static boolean addResultFails(ResultsBean resultsBean) {
        try {
            resultsBean.addResult(new PointEntity());
            return false;
        } catch (RuntimeException exception) {
            return true;
        }
    }

}
