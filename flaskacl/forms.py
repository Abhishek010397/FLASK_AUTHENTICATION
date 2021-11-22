from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flaskacl.models import User

class RegistrationForm(FlaskForm):
    username=StringField(validators=[InputRequired(),Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
    submit=SubmitField("Register")

    def validate_username(self,username):
        existing_username=User.query.filter_by(username=username.data).first()
        if existing_username:
            raise ValidationError("Username Already Exists!")

class LoginForm(FlaskForm):
    username=StringField(validators=[InputRequired(),Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
    submit=SubmitField("Submit")
