from flask import render_template, redirect, url_for, flash, g, request
from flask.ext.login import login_required, current_user

from app.extensions import db
from . import cast
from .forms import PickForm, CastForm
from ..models import User, Cast, Pick

from datetime import datetime

@cast.before_request
def before_request():
	g.next_cast = Cast.query.order_by(Cast.cast_number.desc()).first()

@cast.route('/')
def index():
	cast = Cast.query.order_by(Cast.cast_number.desc()).first()
	return render_template('cast/index.html', cast=cast)

@cast.route('/pick', methods=['GET', 'POST'])
@login_required
def pick():
	form = PickForm()
	if form.validate_on_submit():
		pick = Pick()

		form.to_model(pick)
		pick.cast = g.next_cast
		pick.author = current_user
		pick.date_added = datetime.utcnow()

		db.session.add(pick)
		db.session.commit()

		flash('Pick added successfully!')
		return redirect(url_for('cast.index'))

	return render_template('cast/pick.html', form=form)

@cast.route('/edit/pick/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_pick(id=None):
	if not id:
		return redirect(url_for('cast.index'))

	pick = Pick.query.get(int(id))
	if not pick or pick.author.id != current_user.id:
		flash('Invalid pick.')
		return redirect(url_for('cast.index'))

	return 'Edit route.'

@cast.route('/create', methods=['GET', 'POST'])
@login_required
def create_cast():
	form = CastForm()
	form.host.choices = [ (user.id, user.username) for user in User.query.all()]

	if form.validate_on_submit():
		cast = Cast()
		form.to_model(cast)

		host = User.query.get(form.host.data)
		cast.host = host

		db.session.add(cast)
		db.session.commit()

		flash('Cast added.')
		return redirect(url_for('cast.index'))
	else:
		form.cast_number.data = g.next_cast.cast_number + 1  if g.next_cast else 1

	return render_template('cast/create.html', form=form)

@cast.route('/user')
@cast.route('/user/<string:username>', endpoint='user', methods=['GET', 'POST'])
def profile(username=None):
	if username:
		user = User.query.filter_by(username=username).first_or_404()
		return render_template('cast/user.html', user=user)

	return redirect(url_for('cast.index'))
