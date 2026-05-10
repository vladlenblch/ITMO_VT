package org.example.validation;

import org.example.service.Messages;

import jakarta.faces.application.FacesMessage;
import jakarta.faces.component.UIComponent;
import jakarta.faces.context.FacesContext;
import jakarta.faces.validator.FacesValidator;
import jakarta.faces.validator.Validator;
import jakarta.faces.validator.ValidatorException;

@FacesValidator("xValidator")
public class XValidator implements Validator<Double> {

    private static final double MIN_X = -5.0;
    private static final double MAX_X = 5.0;

    @Override
    public void validate(FacesContext context, UIComponent component, Double value) throws ValidatorException {
        if (value == null) {
            throw new ValidatorException(new FacesMessage(FacesMessage.SEVERITY_ERROR,
                    Messages.get("validation.error"), Messages.get("validation.x.required")));
        }

        if (value <= MIN_X || value >= MAX_X) {
            throw new ValidatorException(new FacesMessage(FacesMessage.SEVERITY_ERROR,
                    Messages.get("validation.error"), Messages.format("validation.x.range", value)));
        }
    }
}
