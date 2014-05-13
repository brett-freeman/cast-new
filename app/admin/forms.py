from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

class AnnouncementForm(Form):
	message = StringField('Message', validators=[Required()])
	submit = SubmitField('Submit')