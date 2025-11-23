package org.example.beans;

import org.example.entities.PointEntity;
import org.example.service.KafkaService;

import jakarta.enterprise.context.SessionScoped;
import jakarta.faces.application.FacesMessage;
import jakarta.faces.context.FacesContext;
import jakarta.inject.Inject;
import jakarta.inject.Named;

import java.io.Serializable;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.Date;

@Named
@SessionScoped
public class PointBean implements Serializable {

    private static final long serialVersionUID = 1L;

    private BigDecimal x;
    private BigDecimal y;
    private BigDecimal r;
    private String status;

    @Inject
    private ResultsBean resultsBean;

    @Inject
    private KafkaService kafkaService;

    @jakarta.annotation.PostConstruct
    public void init() {
        this.r = kafkaService.getRecommendedRadius();
    }

    public BigDecimal getX() {
        return x;
    }

    public void setX(BigDecimal x) {
        this.x = x;
    }

    public BigDecimal getY() {
        return y;
    }

    public void setY(BigDecimal y) {
        this.y = y;
    }

    public BigDecimal getR() {
        return r;
    }

    public void setR(BigDecimal r) {
        this.r = r;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public BigDecimal getR1Value() {
        return BigDecimal.ONE;
    }

    public BigDecimal getR2Value() {
        return BigDecimal.valueOf(2);
    }

    public BigDecimal getR3Value() {
        return BigDecimal.valueOf(3);
    }

    public BigDecimal getR4Value() {
        return BigDecimal.valueOf(4);
    }

    public BigDecimal getR5Value() {
        return BigDecimal.valueOf(5);
    }

    public String selectR1() {
        this.r = BigDecimal.ONE;
        return null;
    }
    
    public String selectR2() {
        this.r = BigDecimal.valueOf(2);
        return null;
    }
    
    public String selectR3() {
        this.r = BigDecimal.valueOf(3);
        return null;
    }
    
    public String selectR4() {
        this.r = BigDecimal.valueOf(4);
        return null;
    }
    
    public String selectR5() {
        this.r = BigDecimal.valueOf(5);
        return null;
    }

    public void checkPoint() {
        FacesContext context = FacesContext.getCurrentInstance();

        if (this.r == null) {
            this.r = kafkaService.getRecommendedRadius();
        }

        if (this.x == null || this.y == null || this.r == null) {
            context.addMessage(null, new FacesMessage(FacesMessage.SEVERITY_ERROR,
                    "Ошибка", "Все поля должны быть заполнены"));
            this.status = "Ошибка: заполните все поля";
            return;
        }

        java.util.Set<BigDecimal> validRValues = java.util.Set.of(
                BigDecimal.ONE,
                BigDecimal.valueOf(2),
                BigDecimal.valueOf(3),
                BigDecimal.valueOf(4),
                BigDecimal.valueOf(5)
        );
        if (!validRValues.contains(this.r)) {
            context.addMessage(null, new FacesMessage(FacesMessage.SEVERITY_ERROR,
                    "Ошибка валидации", "Неверное значение R. Допустимые значения: 1, 2, 3, 4, 5"));
            this.status = "Ошибка: неверное значение R";
            return;
        }

        long timeNow = System.currentTimeMillis();
        boolean hit = checkHit(this.x, this.y, this.r);
        long endTime = System.currentTimeMillis();

        PointEntity pointEntity = new PointEntity();
        pointEntity.setX(this.x);
        pointEntity.setY(this.y);
        pointEntity.setR(this.r);
        pointEntity.setHit(hit);
        pointEntity.setCurrentTime(new Date());
        pointEntity.setExecutionTime(endTime - timeNow);

        try {
            resultsBean.addResult(pointEntity);
            this.status = "Point added successfully!";
            context.addMessage(null, new FacesMessage(FacesMessage.SEVERITY_INFO,
                    "Успех", "Точка успешно добавлена"));
            this.x = null;
            this.y = null;
            this.r = kafkaService.getRecommendedRadius();
        } catch (Exception e) {
            this.status = "Ошибка: " + e.getMessage();
            context.addMessage(null, new FacesMessage(FacesMessage.SEVERITY_ERROR,
                    "Ошибка", "Произошла ошибка при сохранении точки: " + e.getMessage()));
            e.printStackTrace();
        }
    }

    private boolean checkHit(BigDecimal x, BigDecimal y, BigDecimal r) {
        BigDecimal zero = BigDecimal.ZERO;
        BigDecimal halfR = r.divide(BigDecimal.valueOf(2), 10, RoundingMode.HALF_UP);

        if (x.compareTo(zero) <= 0 && y.compareTo(zero) >= 0) {
            BigDecimal minusHalfR = halfR.negate();
            if (x.compareTo(minusHalfR) >= 0) {
                BigDecimal lineY = x.multiply(BigDecimal.valueOf(2)).add(r);
                if (y.compareTo(lineY) <= 0 && y.compareTo(zero) >= 0) {
                    return true;
                }
            }
        }

        if (x.compareTo(zero) <= 0 && y.compareTo(zero) <= 0) {
            BigDecimal minusR = r.negate();
            if (x.compareTo(minusR) >= 0 && y.compareTo(minusR) >= 0) {
                return true;
            }
        }

        if (x.compareTo(zero) >= 0 && y.compareTo(zero) <= 0) {
            BigDecimal xSquared = x.multiply(x);
            BigDecimal ySquared = y.multiply(y);
            BigDecimal rSquared = r.multiply(r);
            BigDecimal sumSquares = xSquared.add(ySquared);
            if (sumSquares.compareTo(rSquared) <= 0) {
                return true;
            }
        }

        return false;
    }
    
    public void onRChange() {
    }
}
