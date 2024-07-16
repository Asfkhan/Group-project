from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    PasswordField,
    TextAreaField,
    FileField,
    SubmitField,
)
from wtforms.validators import DataRequired, Length, NumberRange
from flask_wtf.file import FileField, FileAllowed, FileRequired


class SignupForm(FlaskForm):
    fullname = StringField(
        "Full Name",
        validators=[
            DataRequired(),
            Length(min=4, max=25),
        ],
    )
    contact = IntegerField(
        "Contact",
        validators=[
            DataRequired(),
            NumberRange(min=1000000000, max=9999999999, message="Invalid mobile number"),
        ],
    )
    address = TextAreaField(
        "Address",
        validators=[
            DataRequired(),
            Length(min=6, max=20),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=2, max=8)],
    )
    upload = FileField(
        "Upload Profile Image",
        validators=[FileRequired(), FileAllowed(["jpg", "png"], "Images only!")],
    )
    submit = SubmitField("SignUp")
