import { z } from 'zod';

export const credentialsSchema = z.object({
    username: z.string()
        .trim()
        .min(1, 'Введите логин')
        .max(50, 'Логин слишком длинный'),
    password: z.string()
        .trim()
        .min(4, 'Пароль должен быть длиной не менее 4 символов')
        .max(100, 'Пароль слишком длинный'),
});

export const loginSchema = z.object({
    username: z.string()
        .trim()
        .min(1, 'Введите логин'),
    credentialType: z.enum(['password', 'recovery', 'ownership'], {
        required_error: 'Выберите тип входа',
        invalid_type_error: 'Некорректный тип входа',
    }),
    value: z.string()
        .trim()
        .max(200, 'Слишком длинное значение'),
});

const ALLOWED_X_VALUES = [-4, -3, -2, -1, 0, 1, 2, 3, 4];
const ALLOWED_R_VALUES = [1, 2, 3, 4];
const X_RANGE = { min: -4, max: 4 };

export const pointSchema = z.object({
    x: z.number({
        required_error: 'Выберите X',
        invalid_type_error: 'Некорректное значение X',
    }).refine((value) => value >= X_RANGE.min && value <= X_RANGE.max, {
        message: 'X должен быть в диапазоне [-4; 4]',
    }),
    y: z.preprocess(
        (value) => {
            if (typeof value === 'string') {
                const replaced = value.replace(',', '.');
                return replaced.trim() === '' ? Number.NaN : Number(replaced);
            }
            return value;
        },
        z.number({
            required_error: 'Введите Y',
            invalid_type_error: 'Y должен быть числом',
        }).gt(-3, 'Y должен быть больше -3')
            .lt(5, 'Y должен быть меньше 5'),
    ),
    r: z.number({
        required_error: 'Выберите R',
        invalid_type_error: 'Некорректное значение R',
    }).refine((value) => ALLOWED_R_VALUES.includes(value), {
        message: 'R должен быть положительным и выбран из списка',
    }),
});

export const validationConstants = {
    ALLOWED_X_VALUES,
    ALLOWED_R_VALUES,
    X_RANGE,
};
