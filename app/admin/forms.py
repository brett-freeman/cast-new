from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Required

class AnnouncementForm(Form):
	message = StringField('Message', validators=[Required()])
	submit = SubmitField('Submit')

class PickUserForm(Form):
	user = SelectField('User', coerce=int, validators=[Required()])
	submit = SubmitField('Edit')
