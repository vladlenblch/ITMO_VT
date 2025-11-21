package org.example.ml;

import org.tribuo.Model;
import org.tribuo.Prediction;
import org.tribuo.classification.Label;
import org.tribuo.classification.LabelFactory;
import org.tribuo.classification.sgd.linear.LogisticRegressionTrainer;
import org.tribuo.impl.ArrayExample;
import org.tribuo.MutableDataset;
import org.tribuo.Example;
import org.tribuo.datasource.ListDataSource;
import org.tribuo.provenance.DataSourceProvenance;
import org.tribuo.provenance.SimpleDataSourceProvenance;
import org.example.model.Result;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

public class ModelManager {
    private static final String MODEL_FILE_NAME = "hit_prediction.model";
    private static final String DATA_FILE_NAME = "training_data.csv";
    private static final LabelFactory labelFactory = new LabelFactory();
    
    private Model<Label> model;
    private String modelPath;
    private String dataPath;
    
    public ModelManager() {
        this.modelPath = "src/main/resources/" + MODEL_FILE_NAME;
        this.dataPath = DATA_FILE_NAME;
    }
    
    public void setPaths(String modelPath, String dataPath) {
        this.modelPath = modelPath;
        this.dataPath = dataPath;
    }
    
    @SuppressWarnings("unchecked")
    public void loadOrCreateModel() throws IOException {
        Path modelFilePath = Paths.get(modelPath);
        
        if (Files.exists(modelFilePath)) {
            try (ObjectInputStream ois = new ObjectInputStream(
                    new FileInputStream(modelFilePath.toFile()))) {
                model = (Model<Label>) ois.readObject();
            } catch (ClassNotFoundException | ClassCastException e) {
                System.err.println("Ошибка при загрузке модели: " + e.getMessage());
                model = null;
            }
        } else {
            trainModel();
        }
    }
    
    public void trainModel() throws IOException {
        List<Result> trainingData = loadTrainingData();
        
        if (trainingData.size() < 10) {
            model = null;
            return;
        }
        
        List<Example<Label>> examples = new ArrayList<>();
        for (Result result : trainingData) {
            double[] featureValues = new double[]{result.getX(), result.getY(), result.getR()};
            String[] featureNames = new String[]{"x", "y", "r"};
            Label label = new Label(result.isHit() ? "HIT" : "MISS");
            examples.add(new ArrayExample<>(label, featureNames, featureValues));
        }
        
        if (examples.isEmpty()) {
            model = null;
            return;
        }
        
        DataSourceProvenance provenance = new SimpleDataSourceProvenance("training", labelFactory);
        ListDataSource<Label> dataSource = new ListDataSource<Label>(examples, labelFactory, provenance);
        MutableDataset<Label> dataset = new MutableDataset<Label>(dataSource);
        
        long hitCount = trainingData.stream().filter(Result::isHit).count();
        long missCount = trainingData.size() - hitCount;
        
        if (hitCount == 0 || missCount == 0) {
            System.err.println("Ошибка: в данных только один класс (HIT: " + hitCount + ", MISS: " + missCount + "). Нужны примеры обоих классов.");
            model = null;
            return;
        }
        
        LogisticRegressionTrainer trainer = new LogisticRegressionTrainer();
        model = trainer.train(dataset);
    }
    
    public void saveModel() throws IOException {
        if (model == null) {
            return;
        }
        
        Path modelFilePath = Paths.get(modelPath);
        Path parentDir = modelFilePath.getParent();
        
        if (parentDir != null && !Files.exists(parentDir)) {
            Files.createDirectories(parentDir);
        }
        
        try (ObjectOutputStream oos = new ObjectOutputStream(
                new FileOutputStream(modelFilePath.toFile()))) {
            oos.writeObject(model);
        } catch (Exception e) {
            System.err.println("Ошибка при сохранении модели: " + e.getMessage());
            throw new IOException("Ошибка при сохранении модели", e);
        }
    }
    
    public double predictHitProbability(int x, double y, int r) {
        if (model == null) {
            return 0.5;
        }
        
        try {
            double[] featureValues = new double[]{x, y, r};
            String[] featureNames = new String[]{"x", "y", "r"};
            Label tempLabel = new Label("HIT");
            ArrayExample<Label> example = new ArrayExample<>(tempLabel, featureNames, featureValues);
            
            Prediction<Label> prediction = model.predict(example);
            var scoreMap = prediction.getOutputScores();
            
            Label hitLabel = scoreMap.get("HIT");
            if (hitLabel != null) {
                return hitLabel.getScore();
            }
            
            if (scoreMap.size() == 1) {
                System.err.println("Ошибка: модель обучена только на одном классе");
                return 0.5;
            }
            
            Label predicted = prediction.getOutput();
            return predicted.getLabel().equals("HIT") ? 1.0 : 0.0;
        } catch (Exception e) {
            System.err.println("Ошибка при предсказании: " + e.getMessage());
            return 0.5;
        }
    }
    
    private List<Result> loadTrainingData() throws IOException {
        List<Result> results = new ArrayList<>();
        File dataFile = new File(dataPath);
        
        if (!dataFile.exists()) {
            return results;
        }
        
        try (BufferedReader reader = new BufferedReader(new FileReader(dataFile))) {
            String line;
            while ((line = reader.readLine()) != null) {
                if (line.trim().isEmpty() || line.startsWith("#")) {
                    continue;
                }
                
                String[] parts = line.split(",");
                if (parts.length >= 4) {
                    try {
                        int x = Integer.parseInt(parts[0].trim());
                        double y = Double.parseDouble(parts[1].trim().replace(',', '.'));
                        int r = Integer.parseInt(parts[2].trim());
                        boolean hit = Boolean.parseBoolean(parts[3].trim());
                        results.add(new Result(x, y, r, hit, java.time.LocalDateTime.now()));
                    } catch (NumberFormatException e) {
                        System.err.println("Ошибка: неверный формат строки в данных: " + line);
                    }
                }
            }
        }
        
        if (!results.isEmpty()) {
            System.out.println("Загружено " + results.size() + " записей из файла данных");
        }
        
        return results;
    }
    
    public void saveTrainingData(Result result) throws IOException {
        File dataFile = new File(dataPath);
        File parentDir = dataFile.getParentFile();
        if (parentDir != null && !parentDir.exists()) {
            parentDir.mkdirs();
        }
        
        try (FileWriter writer = new FileWriter(dataFile, true)) {
            writer.append(String.format(Locale.US, "%d,%.6f,%d,%b\n",
                result.getX(), result.getY(), result.getR(), result.isHit()));
        } catch (IOException e) {
            System.err.println("Ошибка при сохранении данных: " + e.getMessage());
            throw e;
        }
        
        try {
            List<Result> currentData = loadTrainingData();
            if (currentData.size() >= 10) {
                long hitCount = currentData.stream().filter(Result::isHit).count();
                long missCount = currentData.size() - hitCount;
                
                boolean shouldRetrain = model == null || 
                                      currentData.size() % 10 == 0 ||
                                      (hitCount > 0 && missCount > 0 && (hitCount == 1 || missCount == 1));
                
                if (shouldRetrain) {
                    System.out.println("Переобучение модели на " + currentData.size() + " записях (HIT: " + hitCount + ", MISS: " + missCount + ")");
                    retrainModel();
                }
            }
        } catch (IOException e) {
            System.err.println("Ошибка при переобучении модели: " + e.getMessage());
        }
    }
    
    public void retrainModel() throws IOException {
        trainModel();
        if (model != null) {
            saveModel();
        }
    }
}
