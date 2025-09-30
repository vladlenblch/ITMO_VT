from pydantic import BaseModel, Field, field_validator
from datetime import datetime

class PointRequest(BaseModel):
    x: int = Field(..., description="Координата X")
    y: float = Field(..., description="Координата Y") 
    r: float = Field(..., description="Радиус R")

    @field_validator('x')
    @classmethod
    def validate_x(cls, v):
        allowed_x = [-4, -3, -2, -1, 0, 1, 2, 3, 4]
        if v not in allowed_x:
            raise ValueError(f"X должен быть одним из: {allowed_x}")
        return v

    @field_validator('y')
    @classmethod
    def validate_y(cls, v):
        if not isinstance(v, (int, float)):
            raise ValueError("Y должен быть числом")
        if v < -3 or v > 3:
            raise ValueError("Y должен быть в диапазоне [-3, 3]")
        return float(v)

    @field_validator('r')
    @classmethod
    def validate_r(cls, v):
        allowed_r = [1.0, 1.5, 2.0, 2.5, 3.0]
        if v not in allowed_r:
            raise ValueError(f"R должен быть одним из: {allowed_r}")
        return float(v)


class PointResponse(BaseModel):
    result: bool = Field(..., description="Результат проверки попадания")
    time: float = Field(..., description="Время выполнения в наносекундах")
    now: datetime = Field(default_factory=datetime.now, description="Время запроса")


class ErrorResponse(BaseModel):
    reason: str = Field(..., description="Причина ошибки")
    now: datetime = Field(default_factory=datetime.now, description="Время ошибки")
