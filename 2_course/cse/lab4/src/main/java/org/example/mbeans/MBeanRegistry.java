package org.example.mbeans;

import org.example.entities.PointEntity;
import org.example.mbeans.interfaces.AreaCalculatorMBean;
import org.example.mbeans.interfaces.PointStatisticsMBean;

import jakarta.annotation.PostConstruct;
import jakarta.annotation.PreDestroy;
import jakarta.enterprise.context.Initialized;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.enterprise.event.Observes;

import java.io.Serializable;
import java.lang.management.ManagementFactory;
import java.math.BigDecimal;
import javax.management.MBeanServer;
import javax.management.ObjectName;
import javax.management.StandardEmitterMBean;
import javax.management.StandardMBean;

@ApplicationScoped
public class MBeanRegistry implements Serializable {

    private static final long serialVersionUID = 1L;
    private static final String POINT_STATISTICS_NAME = "org.example.lab4:type=PointStatistics";
    private static final String AREA_CALCULATOR_NAME = "org.example.lab4:type=AreaCalculator";

    private final PointStatistics pointStatistics = new PointStatistics();
    private final AreaCalculator areaCalculator = new AreaCalculator();
    private transient MBeanServer mBeanServer;
    private transient ObjectName pointStatisticsObjectName;
    private transient ObjectName areaCalculatorObjectName;

    @PostConstruct
    public void init() {
        try {
            mBeanServer = ManagementFactory.getPlatformMBeanServer();
            pointStatisticsObjectName = new ObjectName(POINT_STATISTICS_NAME);
            areaCalculatorObjectName = new ObjectName(AREA_CALCULATOR_NAME);

            register(pointStatistics, pointStatisticsObjectName);
            register(areaCalculator, areaCalculatorObjectName);
        } catch (Exception e) {
            throw new IllegalStateException("Failed to register application MBeans", e);
        }
    }

    public void onApplicationStart(@Observes @Initialized(ApplicationScoped.class) Object event) {
        // skip
    }

    @PreDestroy
    public void destroy() {
        unregister(pointStatisticsObjectName);
        unregister(areaCalculatorObjectName);
    }

    public void recordPoint(PointEntity point) {
        pointStatistics.recordPoint(point.getX(), point.getY(), Boolean.TRUE.equals(point.getHit()));
        updateRadius(point.getR());
    }

    public void updateRadius(BigDecimal radius) {
        if (radius != null) {
            areaCalculator.setRadius(radius.doubleValue());
        }
    }

    private void register(Object mBean, ObjectName objectName) throws Exception {
        if (mBeanServer.isRegistered(objectName)) {
            mBeanServer.unregisterMBean(objectName);
        }
        if (mBean instanceof PointStatistics pointStatistics) {
            mBeanServer.registerMBean(new StandardEmitterMBean(
                    pointStatistics,
                    PointStatisticsMBean.class,
                    pointStatistics
            ), objectName);
        } else if (mBean instanceof AreaCalculator areaCalculator) {
            mBeanServer.registerMBean(new StandardMBean(areaCalculator, AreaCalculatorMBean.class), objectName);
        }
    }

    private void unregister(ObjectName objectName) {
        try {
            if (mBeanServer != null && objectName != null && mBeanServer.isRegistered(objectName)) {
                mBeanServer.unregisterMBean(objectName);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
