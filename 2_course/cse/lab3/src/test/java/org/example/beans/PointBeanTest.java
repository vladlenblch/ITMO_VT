package org.example.beans;

import org.example.*;
import org.example.entities.*;
import org.example.service.*;
import org.junit.jupiter.api.*;

import static org.example.TestBeans.*;
import static org.example.TestFields.*;
import static org.junit.jupiter.api.Assertions.*;

class PointBeanTest {

    @Test
    void gettersReturnSetValues() {
        PointBean pointBean = new PointBean();

        pointBean.setX(1.5);
        pointBean.setY(-2.5);
        pointBean.setR(3.0);
        pointBean.setStatus("saved");

        assertEquals(1.5, pointBean.getX());
        assertEquals(-2.5, pointBean.getY());
        assertEquals(3.0, pointBean.getR());
        assertEquals("saved", pointBean.getStatus());
    }

    @Test
    void rValueGettersReturnFixedValues() {
        PointBean pointBean = new PointBean();

        assertEquals(1.0, pointBean.getR1Value());
        assertEquals(2.0, pointBean.getR2Value());
        assertEquals(3.0, pointBean.getR3Value());
        assertEquals(4.0, pointBean.getR4Value());
        assertEquals(5.0, pointBean.getR5Value());
    }

    @Test
    void selectRMethodsSetRAndReturnNull() {
        PointBean pointBean = new PointBean();

        assertNull(pointBean.selectR1());
        assertEquals(1.0, pointBean.getR());
        assertNull(pointBean.selectR2());
        assertEquals(2.0, pointBean.getR());
        assertNull(pointBean.selectR3());
        assertEquals(3.0, pointBean.getR());
        assertNull(pointBean.selectR4());
        assertEquals(4.0, pointBean.getR());
        assertNull(pointBean.selectR5());
        assertEquals(5.0, pointBean.getR());
    }

    @Test
    void selectedRMethodsReturnTrueOnlyForCurrentR() {
        PointBean pointBean = new PointBean();

        pointBean.setR(3.0);

        assertFalse(pointBean.isR1Selected());
        assertFalse(pointBean.isR2Selected());
        assertTrue(pointBean.isR3Selected());
        assertFalse(pointBean.isR4Selected());
        assertFalse(pointBean.isR5Selected());
    }

    @Test
    void selectedRMethodsReturnFalseWhenRIsNull() {
        PointBean pointBean = new PointBean();

        assertFalse(pointBean.isR1Selected());
        assertFalse(pointBean.isR2Selected());
        assertFalse(pointBean.isR3Selected());
        assertFalse(pointBean.isR4Selected());
        assertFalse(pointBean.isR5Selected());
    }

    @Test
    void onRChangeDoesNotChangeR() {
        PointBean pointBean = new PointBean();

        pointBean.setR(4.0);
        pointBean.onRChange();

        assertEquals(4.0, pointBean.getR());
    }

    @Test
    void checkPointRequiresAllFields() {
        PointBean pointBean = new PointBean();
        TestFacesContext context = new TestFacesContext();

        TestFacesContext.set(context);
        pointBean.checkPoint();

        assertEquals(Messages.get("point.status.required"), pointBean.getStatus());
        assertEquals(1, context.messages.size());
    }

    @Test
    void checkPointRequiresY() {
        PointBean pointBean = new PointBean();
        TestFacesContext context = new TestFacesContext();

        TestFacesContext.set(context);
        pointBean.setX(1.0);
        pointBean.setR(4.0);

        pointBean.checkPoint();

        assertEquals(Messages.get("point.status.required"), pointBean.getStatus());
        assertEquals(1, context.messages.size());
    }

    @Test
    void checkPointRequiresR() {
        PointBean pointBean = new PointBean();
        TestFacesContext context = new TestFacesContext();

        TestFacesContext.set(context);
        pointBean.setX(1.0);
        pointBean.setY(1.0);

        pointBean.checkPoint();

        assertEquals(Messages.get("point.status.required"), pointBean.getStatus());
        assertEquals(1, context.messages.size());
    }

    @Test
    void checkPointRejectsInvalidR() {
        PointBean pointBean = new PointBean();
        TestFacesContext context = new TestFacesContext();

        TestFacesContext.set(context);
        pointBean.setX(1.0);
        pointBean.setY(1.0);
        pointBean.setR(6.0);

        pointBean.checkPoint();

        assertEquals(Messages.get("point.status.invalid_r"), pointBean.getStatus());
        assertEquals(1, context.messages.size());
    }

    @Test
    void checkPointSavesPointWhenUserExists() throws Exception {
        UserEntity user = new UserEntity();
        FakeResultsBean resultsBean = new FakeResultsBean();
        PointBean pointBean = pointBean(new FakeUserBean(user), resultsBean);
        TestFacesContext context = new TestFacesContext();

        TestFacesContext.set(context);
        pointBean.setX(1.23456);
        pointBean.setY(-1.23456);
        pointBean.setR(4.0);

        pointBean.checkPoint();

        assertEquals(Messages.get("point.status.saved"), pointBean.getStatus());
        assertNull(pointBean.getX());
        assertNull(pointBean.getY());
        assertNull(pointBean.getR());
        assertEquals(1.235, resultsBean.savedPoint.getX());
        assertEquals(-1.235, resultsBean.savedPoint.getY());
        assertEquals(4.0, resultsBean.savedPoint.getR());
        assertTrue(resultsBean.savedPoint.getHit());
        assertEquals(user, resultsBean.savedPoint.getUser());
        assertNotNull(resultsBean.savedPoint.getCurrentTime());
        assertNotNull(resultsBean.savedPoint.getExecutionTime());
        assertEquals(1, context.messages.size());
    }

    @Test
    void checkPointShowsErrorWhenUserIsMissing() throws Exception {
        PointBean pointBean = pointBean(new FakeUserBean(null), new FakeResultsBean());
        TestFacesContext context = new TestFacesContext();

        TestFacesContext.set(context);
        pointBean.setX(1.0);
        pointBean.setY(-1.0);
        pointBean.setR(4.0);

        pointBean.checkPoint();

        assertEquals(Messages.get("point.status.user_not_found"), pointBean.getStatus());
        assertEquals(1, context.messages.size());
    }

    @Test
    void checkPointShowsErrorWhenSaveFails() throws Exception {
        UserEntity user = new UserEntity();
        FakeResultsBean resultsBean = new FakeResultsBean();
        PointBean pointBean = pointBean(new FakeUserBean(user), resultsBean);
        TestFacesContext context = new TestFacesContext();

        resultsBean.fail = true;
        TestFacesContext.set(context);
        pointBean.setX(1.0);
        pointBean.setY(-1.0);
        pointBean.setR(4.0);

        pointBean.checkPoint();

        assertEquals(Messages.get("point.error") + ": fail", pointBean.getStatus());
        assertEquals(1, context.messages.size());
    }

}
