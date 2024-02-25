from flask_wtf import FlaskForm
from wtforms  import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
  username = StringField('Username', 
                         validators= [DataRequired('Enter an username'), Length(min=3, max=15)])
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired(), Length(min=3, max=20)])
  confirm_password = PasswordField('Comfirm Password', 
                                   validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired('Enter your e-mail'), Email()])
  password = PasswordField('Password', 
                           validators=[DataRequired('Enter your password'), Length(min=3, max=20)])
  remember = BooleanField('Remember Me')
  submit = SubmitField('Log In')