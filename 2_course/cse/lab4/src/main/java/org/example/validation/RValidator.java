package org.example.validation;

import jakarta.faces.application.FacesMessage;
import jakarta.faces.component.UIComponent;
import jakarta.faces.context.FacesContext;
import jakarta.faces.validator.FacesValidator;
import jakarta.faces.validator.Validator;
import jakarta.faces.validator.ValidatorException;

import java.math.BigDecimal;
import java.util.Set;

@FacesValidator("rValidator")
public class RValidator implements Validator<BigDecimal> {

    private static final Set<BigDecimal> VALID_R_VALUES = Set.of(
            BigDecimal.ONE,
            BigDecimal.valueOf(2),
            BigDecimal.valueOf(3),
            BigDecimal.valueOf(4),
            BigDecimal.valueOf(5)
    );

    @Override
    public void validate(FacesContext context, UIComponent component, BigDecimal value) throws ValidatorException {
        if (value == null) {
            throw new ValidatorException(new FacesMessage(FacesMessage.SEVERITY_ERROR,
                    "Ошибка валидации", "R не может быть пустым"));
        }

        if (!VALID_R_VALUES.contains(value)) {
            throw new ValidatorException(new FacesMessage(FacesMessage.SEVERITY_ERROR,
                    "Ошибка валидации", "Неверное значение R. Допустимые значения: 1, 2, 3, 4, 5"));
        }
    }
}
