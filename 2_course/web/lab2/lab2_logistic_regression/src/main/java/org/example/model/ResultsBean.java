package org.example.model;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Named;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

@Named("resultsBean")
@ApplicationScoped
public class ResultsBean {
    private final List<Result> results = new ArrayList<>();

    public synchronized void addResult(Result r) {
        results.add(0, r);
        if (results.size() > 100) results.remove(results.size() - 1);
    }

    public synchronized List<Result> getResults() {
        return Collections.unmodifiableList(new ArrayList<>(results));
    }

    public synchronized void clear() {
        results.clear();
    }
}
