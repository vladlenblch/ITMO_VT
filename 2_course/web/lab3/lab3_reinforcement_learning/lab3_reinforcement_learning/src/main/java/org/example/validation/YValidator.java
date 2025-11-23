package org.example.validation;

import jakarta.faces.application.FacesMessage;
import jakarta.faces.component.UIComponent;
import jakarta.faces.context.FacesContext;
import jakarta.faces.validator.FacesValidator;
import jakarta.faces.validator.Validator;
import jakarta.faces.validator.ValidatorException;

import java.math.BigDecimal;

@FacesValidator("yValidator")
public class YValidator implements Validator<BigDecimal> {

    private static final BigDecimal MIN_Y = new BigDecimal("-5");
    private static final BigDecimal MAX_Y = new BigDecimal("5");

    @Override
    public void validate(FacesContext context, UIComponent component, BigDecimal value) throws ValidatorException {
        if (value == null) {
            throw new ValidatorException(new FacesMessage(FacesMessage.SEVERITY_ERROR,
                    "Ошибка валидации", "Y не может быть пустым"));
        }

        if (value.compareTo(MIN_Y) <= 0 || value.compareTo(MAX_Y) >= 0) {
            throw new ValidatorException(new FacesMessage(FacesMessage.SEVERITY_ERROR,
                    "Ошибка валидации", "Y должен быть в диапазоне (-5, 5). Текущее значение: " + value));
        }
    }
}
