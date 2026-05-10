package org.example.validation;

import org.example.service.Messages;

import jakarta.faces.application.FacesMessage;
import jakarta.faces.component.UIComponent;
import jakarta.faces.context.FacesContext;
import jakarta.faces.validator.FacesValidator;
import jakarta.faces.validator.Validator;
import jakarta.faces.validator.ValidatorException;

@FacesValidator("yValidator")
public class YValidator implements Validator<Double> {

    private static final double MIN_Y = -5.0;
    private static final double MAX_Y = 5.0;

    @Override
    public void validate(FacesContext context, UIComponent component, Double value) throws ValidatorException {
        if (value == null) {
            throw new ValidatorException(new FacesMessage(FacesMessage.SEVERITY_ERROR,
                    Messages.get("validation.error"), Messages.get("validation.y.required")));
        }

        if (value <= MIN_Y || value >= MAX_Y) {
            throw new ValidatorException(new FacesMessage(FacesMessage.SEVERITY_ERROR,
                    Messages.get("validation.error"), Messages.format("validation.y.range", value)));
        }
    }
}
