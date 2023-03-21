import math
from typing import Optional
from flask_wtf import FlaskForm
from wtforms import IntegerField, Field
from wtforms.validators import InputRequired, ValidationError


def number_length(min: int, max: int, message: Optional[str] = None):
    def _number_length(form: FlaskForm, field: Field):
        data = field.data
        length_data = len(str(data))
        if data is None or math.isnan(data) \
                or length_data < min or length_data > max:
            final_message: str = "Invalid length number." if message is None else message
            raise ValidationError(message=final_message)

    return _number_length


class NumberLength:
    def __init__(self, min: int, max: int, message: Optional[str] = None):
        self.min = min
        self.max = max
        self.message = message

    def __call__(self, form: FlaskForm, field: Field):
        data = field.data
        length_data = len(str(data))
        if data is None or math.isnan(data) \
                or length_data < self.min or length_data > self.max:
            final_message: str = "Invalid length number." if self.message is None else self.message
            raise ValidationError(message=final_message)


number_with_function = IntegerField(validators=[InputRequired(), number_length(min=0, max=100)])
number_with_class = IntegerField(validators=[InputRequired(), NumberLength(min=0, max=100)])
