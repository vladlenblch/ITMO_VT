package org.example.entities;

import java.io.Serializable;
import java.math.BigDecimal;
import java.util.Date;

public class PointEntity implements Serializable {

    private static final long serialVersionUID = 1L;

    private Integer id;
    private BigDecimal x;
    private BigDecimal y;
    private BigDecimal r;
    private Boolean hit;
    private Date currentTime;
    private Long executionTime;
    private UserEntity user;

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
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

    public Boolean getHit() {
        return hit;
    }

    public void setHit(Boolean hit) {
        this.hit = hit;
    }

    public Date getCurrentTime() {
        return currentTime;
    }

    public void setCurrentTime(Date currentTime) {
        this.currentTime = currentTime;
    }

    public Long getExecutionTime() {
        return executionTime;
    }

    public void setExecutionTime(Long executionTime) {
        this.executionTime = executionTime;
    }

    public UserEntity getUser() {
        return user;
    }

    public void setUser(UserEntity user) {
        this.user = user;
    }

    public PointEntity() {
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        PointEntity point = (PointEntity) o;
        return id != null && id.equals(point.getId());
    }

    @Override
    public int hashCode() {
        return id != null ? id.hashCode() : 0;
    }
}
