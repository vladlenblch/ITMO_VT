package org.example.beans;

import org.example.entities.PointEntity;
import org.example.entities.UserEntity;
import org.example.service.AreaChecker;
import org.example.service.Messages;

import jakarta.enterprise.context.SessionScoped;
import jakarta.faces.application.FacesMessage;
import jakarta.faces.context.FacesContext;
import jakarta.inject.Inject;
import jakarta.inject.Named;

import java.io.Serializable;
import java.util.Date;
import java.util.Set;

@Named
@SessionScoped
public class PointBean implements Serializable {

    private static final long serialVersionUID = 1L;

    private Double x;
    private Double y;
    private Double r;
    private String status;

    @Inject
    private UserBean userBean;

    @Inject
    private ResultsBean resultsBean;

    public Double getX() {
        return x;
    }

    public void setX(Double x) {
        this.x = x;
    }

    public Double getY() {
        return y;
    }

    public void setY(Double y) {
        this.y = y;
    }

    public Double getR() {
        return r;
    }

    public void setR(Double r) {
        this.r = r;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public Double getR1Value() {
        return 1.0;
    }

    public Double getR2Value() {
        return 2.0;
    }

    public Double getR3Value() {
        return 3.0;
    }

    public Double getR4Value() {
        return 4.0;
    }

    public Double getR5Value() {
        return 5.0;
    }

    public String selectR1() {
        this.r = 1.0;
        return null;
    }
    
    public String selectR2() {
        this.r = 2.0;
        return null;
    }
    
    public String selectR3() {
        this.r = 3.0;
        return null;
    }
    
    public String selectR4() {
        this.r = 4.0;
        return null;
    }
    
    public String selectR5() {
        this.r = 5.0;
        return null;
    }

    public boolean isR1Selected() {
        return isSelectedR(1.0);
    }

    public boolean isR2Selected() {
        return isSelectedR(2.0);
    }

    public boolean isR3Selected() {
        return isSelectedR(3.0);
    }

    public boolean isR4Selected() {
        return isSelectedR(4.0);
    }

    public boolean isR5Selected() {
        return isSelectedR(5.0);
    }

    public void checkPoint() {
        FacesContext context = FacesContext.getCurrentInstance();

        if (this.x == null || this.y == null || this.r == null) {
            context.addMessage(null, new FacesMessage(FacesMessage.SEVERITY_ERROR,
                    Messages.get("point.error"), Messages.get("point.required")));
            this.status = Messages.get("point.status.required");
            return;
        }

        Set<Double> validRValues = Set.of(1.0, 2.0, 3.0, 4.0, 5.0);
        if (!validRValues.contains(this.r)) {
            context.addMessage(null, new FacesMessage(FacesMessage.SEVERITY_ERROR,
                    Messages.get("validation.error"), Messages.get("validation.r.invalid")));
            this.status = Messages.get("point.status.invalid_r");
            return;
        }

        this.x = AreaChecker.round3(this.x);
        this.y = AreaChecker.round3(this.y);
        this.r = AreaChecker.round3(this.r);

        long timeNow = System.currentTimeMillis();
        boolean hit = AreaChecker.checkHit(this.x, this.y, this.r);
        long endTime = System.currentTimeMillis();

        PointEntity pointEntity = new PointEntity();
        pointEntity.setX(this.x);
        pointEntity.setY(this.y);
        pointEntity.setR(this.r);
        pointEntity.setHit(hit);
        pointEntity.setCurrentTime(new Date());
        pointEntity.setExecutionTime(endTime - timeNow);

        try {
            UserEntity user = userBean.getUserEntity();
            if (user != null) {
                pointEntity.setUser(user);
                resultsBean.addResult(pointEntity);
                this.status = Messages.get("point.status.saved");
                context.addMessage(null, new FacesMessage(FacesMessage.SEVERITY_INFO,
                        Messages.get("point.saved_title"), Messages.get("point.saved")));
                this.x = null;
                this.y = null;
                this.r = null;
            } else {
                this.status = Messages.get("point.status.user_not_found");
                context.addMessage(null, new FacesMessage(FacesMessage.SEVERITY_ERROR,
                        Messages.get("point.error"), Messages.get("point.user_not_found")));
            }
        } catch (Exception e) {
            this.status = Messages.get("point.error") + ": " + e.getMessage();
            context.addMessage(null, new FacesMessage(FacesMessage.SEVERITY_ERROR,
                    Messages.get("point.error"), Messages.format("point.save_failed", e.getMessage())));
            e.printStackTrace();
        }
    }

    public void onRChange() {
    }

    private boolean isSelectedR(double value) {
        return this.r != null && Double.compare(this.r, value) == 0;
    }
}
