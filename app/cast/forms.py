from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import Required, Length, EqualTo

class PickForm(Form):
	artist = StringField('Artist', validators=[Required()])
	album = StringField('Album', validators=[Required()])
	song = StringField('Song', validators=[Required()])
	description = TextAreaField('Description')
	submit = SubmitField('Pick!')
