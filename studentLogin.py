from flask_wtf import FlaskForm
from wtforms import (
    IntegerField,
    PasswordField,
    SubmitField,
)
from wtforms.validators import DataRequired, Length, NumberRange


class LoginForm(FlaskForm):
    
    contact = IntegerField(
        "Mobile No",
        validators=[
            DataRequired(),
            NumberRange(min=1000000000, max=9999999999, message="Invalid mobile number")
        ],
    )
    
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=2, max=8)
        ],
    )
    
    submit = SubmitField("Login")
