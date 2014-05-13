from flask import render_template, redirect, url_for, flash, g, request
from flask.ext.login import login_required, current_user

from app.extensions import db
from . import cast
from .forms import PickForm, CastForm, SearchForm, DeleteCastForm
from .decorators import admin_required
from ..models import User, Cast, Pick

from datetime import datetime

@cast.route('/', endpoint='index')
@cast.route('/cast/', endpoint='view_next_cast')
@cast.route('/cast/<int:cast_number>', endpoint='view_cast')
@cast.route('/cast/<string:view_all>', endpoint='view_all_casts')
def index(cast_number=None, view_all=None):
	if cast_number:
		cast = Cast.query.filter_by(cast_number=int(cast_number)).first_or_404()
		return render_template('cast/cast.html', cast=cast)
	elif view_all == 'all':
		casts = Cast.query.all()
		return render_template('cast/view_all.html', casts=casts)

	cast = Cast.query.order_by(Cast.cast_number.desc()).first()
	return render_template('cast/index.html', cast=cast)

@cast.route('/pick/', methods=['GET', 'POST'])
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

@cast.route('/pick/<int:id>/edit/', methods=['GET', 'POST'])
@login_required
def edit_pick(id=None):
	if not id:
		return redirect(url_for('cast.index'))

	pick = Pick.query.get(int(id))
	if not pick:
		flash('Invalid pick.')
		return redirect(url_for('cast.index'))
	if current_user.is_admin or pick.author.id == current_user.id:
		form = PickForm()
		if form.validate_on_submit():
			form.to_model(pick)
			pick.last_edited = datetime.utcnow()
			try:
				db.session.add(pick)
				db.session.commit()
			except:
				db.session.rollback()
				flash('Unknown error adding pick')
				return redirect(url_for('cast.index'))
			flash('Pick edited successfully.')
			return redirect(url_for('cast.index'))
		form.from_model(pick)
		return render_template('cast/edit_pick.html', form=form, pick=pick)
	else:
		flash('Invalid permissions.')
		return redirect(url_for('cast.index'))
	return redirect(url_for('cast.index'))

@cast.route('/pick/<int:id>/delete/', methods=['GET', 'POST'])
@login_required
def delete_pick(id=None):
	if not id:
		return redirect(url_for('cast.index'))

	pick = Pick.query.get(int(id))
	if not pick:
		flash('Invalid pick.')
		return redirect(url_for('cast.index'))
	if current_user.is_admin or pick.author.id == current_user.id:
		try:
			db.session.delete(pick)
			db.session.commit()
		except:
			flash('Couldn\'t delete pick')
		flash('Pick deleted')
	return redirect(url_for('cast.index'))	

@cast.route('/cast/<int:id>/delete/', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_cast(id=None):
	if not id:
		return redirect(url_for('cast.index'))
	cast = Cast.query.get(id)
	if not cast:
		flash('Invalid cast.')
		return redirect(url_for('cast.index'))

	form = DeleteCastForm()

	if form.validate_on_submit():
		if current_user.is_admin and int(form.confirm.data) == int(cast.cast_number):		
			for pick in cast.picks:
				db.session.delete(pick)
			db.session.delete(cast)
			try:
				db.session.commit()
			except Exception as e:
				print(e)
			flash('Cast deleted')
			return redirect(url_for('cast.index'))
		else:
			flash('Wrong cast number')

	return render_template('cast/delete.html', form=form, cast=cast)

@cast.route('/create/', methods=['GET', 'POST'])
@login_required
@admin_required
def create_cast():
	form = CastForm()
	form.host.choices = [ (user.id, user.username) for user in User.query.all()]

	if form.validate_on_submit():
		cast = Cast()
		form.to_model(cast)
		cast.host = User.query.get(form.host.data)
		cast.cast_number = form.cast_number.data

		db.session.add(cast)
		db.session.commit()

		flash('Cast added.')
		return redirect(url_for('cast.view_cast', cast_number=cast.cast_number))
	else:
		form.cast_number.data = g.next_cast.cast_number + 1  if g.next_cast else 1

	return render_template('cast/create.html', form=form)

@cast.route('/cast/<int:id>/edit/', methods=['GET', 'POST'])
@login_required
def edit_cast(id=None):
	if not id:
		return redirect(url_for('cast.index'))

	cast = Cast.query.get(int(id))
	if not cast:
		flash('Invalid cast')
		return redirect(url_for('cast.index'))

	if current_user.is_admin or cast.host.id == current_user.id:
		form = CastForm()
		form.host.choices = [ (user.id, user.username) for user in User.query.all()]
		form.host.choices.insert(0, (cast.host.id, cast.host.username))

		del form.cast_number
		if form.validate_on_submit():
			form.to_model(cast)
			cast.host = User.query.get(form.host.data)
			try:
				db.session.add(cast)
				db.session.commit()
			except:
				flash('Unknown error editing cast!')
				return redirect(url_for('cast.index'))
			flash('Cast edited')
			return redirect(url_for('cast.view_cast', cast_number=cast.cast_number))
		form.from_model(cast)
		return render_template('/cast/edit_cast.html', form=form, cast=cast)
	else:
		flash('Invalid permissions')
		return redirect(url_for('cast.index'))
	return redirect(url_for('cast.index'))

@cast.route('/user/<string:username>', endpoint='user', methods=['GET', 'POST'])
def profile(username=None):
	user = User.query.filter_by(username=username).first_or_404()
	return render_template('cast/user.html', user=user)

@cast.route('/search/', endpoint='search_redirect', methods=['GET', 'POST'])
@cast.route('/search/<string:query>', endpoint='search')
def search(query=None):
	search_form = SearchForm(request.form)
	if search_form.search.data:
		return redirect(url_for('cast.search', query=search_form.search.data))

	results = None
	if query:
		results = Pick.query.whoosh_search(query).all()
	return render_template('cast/search.html', results=results)
