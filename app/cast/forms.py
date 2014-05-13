from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import Required, Length, EqualTo
from datetime import datetime

class PickForm(Form):
	artist = StringField('Artist', validators=[Required()])
	album = StringField('Album', validators=[Required()])
	song = StringField('Song', validators=[Required()])
	description = TextAreaField('Description')
	links = TextAreaField('Download Links (Separate with commas if more than one)')
	picture_url = StringField('Picture URL (optional)')
	submit = SubmitField('Submit!')

	def from_model(self, pick):
		self.artist.data = pick.artist
		self.album.data = pick.album
		self.song.data = pick.song
		self.description.data = pick.description
		self.links.data = pick.links
		self.picture_url.data = pick.picture_url

	def to_model(self, pick):
		pick.artist = self.artist.data
		pick.album = self.album.data
		pick.song = self.song.data
		pick.description = self.description.data
		pick.links = self.links.data
		pick.picture_url = self.picture_url.data

class CastForm(Form):
	cast_number = StringField('Cast Number', validators=[Required()])
	time = StringField('Time', validators=[Required()])
	date = StringField('Date', validators=[Required()])
	host = SelectField('Host', coerce=int, validators=[Required()])
	description = TextAreaField('Description')
	picture_url = StringField('Picture URL (optional)')
	submit = SubmitField('Submit')

	def from_model(self, cast):
		self.time.data = cast.time
		self.date.data = cast.date
		self.description.data = cast.description
		self.picture_url.data = cast.picture_url

	def to_model(self, cast):
		cast.time = self.time.data
		cast.date = self.date.data
		cast.description = self.description.data
		cast.picture_url = self.picture_url.data

class SearchForm(Form):
    search = StringField('Search')
    submit = SubmitField('Submit!')

class DeleteCastForm(Form):
	cast_number = PasswordField('Cast Number', [Required(), Length(1, 128), EqualTo('confirm', message='Numbers must match.')])
	confirm = PasswordField('Repeat Number')
	submit = SubmitField('Delete forever!')