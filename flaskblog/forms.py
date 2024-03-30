from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms  import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.db_models import User

# -- Registration Form
class RegistrationForm(FlaskForm):
  username = StringField('Username', 
                         validators= [DataRequired('Enter an username'), Length(min=3, max=15)])
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired(), Length(min=3, max=20)])
  confirm_password = PasswordField('Comfirm Password', 
                                   validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Sign Up')
  
  # Custom validations
  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user:
      raise ValidationError('Username taken. Please choose a different one.')
    
  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user:
      raise ValidationError('The email already exist. Please use a different one.')

# -- Login Form
class LoginForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired('Enter your e-mail'), Email()])
  password = PasswordField('Password', 
                           validators=[DataRequired('Enter your password'), Length(min=3, max=20)])
  remember = BooleanField('Remember Me')
  submit = SubmitField('Log In')

# -- Update Form
class UpdateAccountForm(FlaskForm):
  username = StringField('Username', 
                         validators= [DataRequired('Enter an username'), Length(min=3, max=15)])
  email = StringField('Email', validators=[DataRequired(), Email()])
  picture = FileField('Update profile picture', validators=[FileAllowed(['jpg','jpeg', 'png'])])
  
  submit = SubmitField('Save')
  
  # Custom validations
  def validate_username(self, username):
    if username.data != current_user.username:
      user = User.query.filter_by(username=username.data).first()
      if user:
        raise ValidationError('Username taken. Please choose a different one.')
    
  def validate_email(self, email):
    if email.data != current_user.email:
      user = User.query.filter_by(email=email.data).first()
      if user:
        raise ValidationError('The email already exist. Please choose a different one.')