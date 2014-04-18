from ..models import User
from wtforms.validators import ValidationError

def check_username(form, field):
	user = User.query.filter_by(username=field.data).first()
	if user is not None:
		raise ValidationError('Username is taken')