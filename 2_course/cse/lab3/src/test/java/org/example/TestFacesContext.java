package org.example;

import jakarta.faces.application.*;
import jakarta.faces.component.*;
import jakarta.faces.context.*;
import jakarta.faces.render.*;
import jakarta.servlet.http.*;

import java.util.*;

public class TestFacesContext extends FacesContext {

    public final List<FacesMessage> messages = new ArrayList<>();
    public final TestExternalContext externalContext;

    public TestFacesContext() {
        this(null);
    }

    public TestFacesContext(HttpServletRequest request) {
        this.externalContext = new TestExternalContext(request);
    }

    public static void set(TestFacesContext context) {
        FacesContext.setCurrentInstance(context);
    }

    @Override
    public Application getApplication() {
        return null;
    }

    @Override
    public Iterator<String> getClientIdsWithMessages() {
        return Collections.emptyIterator();
    }

    @Override
    public ExternalContext getExternalContext() {
        return externalContext;
    }

    @Override
    public FacesMessage.Severity getMaximumSeverity() {
        return null;
    }

    @Override
    public Iterator<FacesMessage> getMessages() {
        return messages.iterator();
    }

    @Override
    public Iterator<FacesMessage> getMessages(String clientId) {
        return messages.iterator();
    }

    @Override
    public RenderKit getRenderKit() {
        return null;
    }

    @Override
    public boolean getRenderResponse() {
        return false;
    }

    @Override
    public boolean getResponseComplete() {
        return false;
    }

    @Override
    public ResponseStream getResponseStream() {
        return null;
    }

    @Override
    public void setResponseStream(ResponseStream responseStream) {
    }

    @Override
    public ResponseWriter getResponseWriter() {
        return null;
    }

    @Override
    public void setResponseWriter(ResponseWriter responseWriter) {
    }

    @Override
    public UIViewRoot getViewRoot() {
        return null;
    }

    @Override
    public void setViewRoot(UIViewRoot viewRoot) {
    }

    @Override
    public void addMessage(String clientId, FacesMessage message) {
        messages.add(message);
    }

    @Override
    public void release() {
        FacesContext.setCurrentInstance(null);
    }

    @Override
    public void renderResponse() {
    }

    @Override
    public void responseComplete() {
    }
}
