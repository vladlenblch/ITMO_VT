package org.example.mbeans;

import org.example.mbeans.interfaces.PointStatisticsMBean;

import java.math.BigDecimal;
import javax.management.MBeanNotificationInfo;
import javax.management.Notification;
import javax.management.NotificationBroadcasterSupport;

public class PointStatistics extends NotificationBroadcasterSupport implements PointStatisticsMBean {

    private static final BigDecimal NOTIFICATION_LIMIT = BigDecimal.valueOf(6.6);
    private static final String OUT_OF_BOUNDS_NOTIFICATION = "org.example.lab4.point.outOfBounds";
    private static final String POINT_STATISTICS_NAME = "org.example.lab4:type=PointStatistics";

    private int totalPoints;
    private int missPoints;
    private long notificationSequence;

    public void recordPoint(BigDecimal x, BigDecimal y, boolean hit) {
        totalPoints++;
        if (!hit) {
            missPoints++;
        }

        if (isOutOfVisibleArea(x) || isOutOfVisibleArea(y)) {
            sendOutOfBoundsNotification(x, y);
        }
    }

    @Override
    public int getTotalPoints() {
        return totalPoints;
    }

    @Override
    public int getMissPoints() {
        return missPoints;
    }

    @Override
    public MBeanNotificationInfo[] getNotificationInfo() {
        String[] types = {OUT_OF_BOUNDS_NOTIFICATION};
        return new MBeanNotificationInfo[] {
                new MBeanNotificationInfo(types, Notification.class.getName(),
                        "Point coordinates are outside the visible coordinate plane")
        };
    }

    private boolean isOutOfVisibleArea(BigDecimal coordinate) {
        return coordinate.abs().compareTo(NOTIFICATION_LIMIT) >= 0;
    }

    private void sendOutOfBoundsNotification(BigDecimal x, BigDecimal y) {
        Notification notification = new Notification(
                OUT_OF_BOUNDS_NOTIFICATION,
                POINT_STATISTICS_NAME,
                ++notificationSequence,
                System.currentTimeMillis(),
                "Point is outside visible coordinate plane: x=" + x + ", y=" + y
        );
        sendNotification(notification);
    }
}
