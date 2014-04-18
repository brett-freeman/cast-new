from flask import render_template, redirect, url_for, flash
from flask.ext.login import login_required, current_user
from . import cast
from app import db
from .forms import PickForm, CastForm
from ..models import User, Cast, Pick

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
		cast = Cast.query.order_by(Cast.cast_number.desc()).first()

		form.to_model(pick)
		pick.cast = cast
		pick.author = current_user

		db.session.add(pick)
		db.session.commit()

		flash('Pick added successfully!')
		return redirect(url_for('cast.index'))

	return render_template('cast/pick.html', form=form)

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


	return render_template('cast/create.html', form=form)