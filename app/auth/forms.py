from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, EqualTo

class RegisterForm(Form):
	username = StringField('Username', validators=[Required(), Length(1, 64)])
	password = PasswordField('Password', [Required(), Length(1, 128), EqualTo('confirm', message='Passwords must match')])
	confirm = PasswordField('Repeat Password')
	submit = SubmitField('Register')

class LoginForm(Form):
	username = StringField('Username', validators=[Required(), Length(1, 64)])
	password = PasswordField('Password', validators=[Required()])
	remember_me = BooleanField('Keep me logged in')
	submit = SubmitField('Login')