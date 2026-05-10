package org.example.validation;

import org.example.service.Messages;

import jakarta.faces.application.FacesMessage;
import jakarta.faces.component.UIComponent;
import jakarta.faces.context.FacesContext;
import jakarta.faces.validator.FacesValidator;
import jakarta.faces.validator.Validator;
import jakarta.faces.validator.ValidatorException;

import java.util.Set;

@FacesValidator("rValidator")
public class RValidator implements Validator<Double> {

    private static final Set<Double> VALID_R_VALUES = Set.of(1.0, 2.0, 3.0, 4.0, 5.0);

    @Override
    public void validate(FacesContext context, UIComponent component, Double value) throws ValidatorException {
        if (value == null) {
            throw new ValidatorException(new FacesMessage(FacesMessage.SEVERITY_ERROR,
                    Messages.get("validation.error"), Messages.get("validation.r.required")));
        }

        if (!VALID_R_VALUES.contains(value)) {
            throw new ValidatorException(new FacesMessage(FacesMessage.SEVERITY_ERROR,
                    Messages.get("validation.error"), Messages.get("validation.r.invalid")));
        }
    }
}
