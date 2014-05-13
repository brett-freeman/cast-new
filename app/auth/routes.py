from flask import render_template, redirect, request, url_for, flash, abort
from flask.ext.login import login_user, logout_user, login_required, current_user
from app.extensions import db
from sqlalchemy.exc import IntegrityError
from . import auth
from .forms import RegisterForm, LoginForm, ChangePasswordForm, ChangeAvatarForm
from ..models import User

@auth.route('/login/', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.verify_password(form.password.data):
			flash('Invalid username or password.')
			return redirect(url_for('auth.login'))
		login_user(user, form.remember_me.data)
		return redirect(request.args.get('next') or url_for('cast.index'))
	return render_template('auth/login.html', form=form)

@auth.route('/logout/')
@login_required
def logout():
	logout_user()
	flash('You have been logged out.')
	return redirect(url_for('cast.index'))

@auth.route('/register/', methods=['GET', 'POST'])
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		new_user = User(username=form.username.data, password=form.password.data)
		try:
			db.session.add(new_user)
			db.session.commit()
		except IntegrityError:
			flash ('Username already exists.')
			return redirect(url_for('auth.register'))

		flash('User created successfully, you may now login.')
		return redirect(url_for('auth.login'))

	return render_template('auth/register.html', form=form)

@auth.route('/settings/', endpoint='settings', methods=['GET', 'POST'])
@auth.route('/settings/<string:username>', endpoint='edit_user', methods=['GET', 'POST'])
def settings(username=None):
	password_form = ChangePasswordForm()
	avatar_form = ChangeAvatarForm()
	if username and not current_user.is_admin:
		flash('Incorrect permissions')
		return redirect(url_for('cast.index'))
	if avatar_form.validate_on_submit():
		if username:
			user = User.query.filter_by(username=username).first_or_404()
		else:
			user = User.query.get(current_user.id)
		if user:
			user.avatar_url = avatar_form.avatar_url.data
			try:
				db.session.add(user)
				db.session.commit()
			except:
				flash('Error changing your avatar url.')

			flash('Avatar url changed.')
			if username:
				return redirect(url_for('auth.edit_user', username=username))
			else:
				return redirect(url_for('auth.settings'))
		else:
			flash('Weird, no user found...')

	if password_form.validate_on_submit():
		if username:
			user = User.query.filter_by(username=username).first_or_404()
		else:
			user = User.query.get(current_user.id)
		if user and user.verify_password(password_form.password.data):
			user.password = password_form.new_password.data
			try:
				db.session.add(user)
				db.session.commit()
			except:
				flash('Error changing your password.')

			flash('Password changed')
			return redirect(url_for('auth.settings'))
		else:
			flash('Incorrect current password, try again.')
	if username:
		user = User.query.filter_by(username=username).first()
		if user.avatar_url:
			avatar_form.avatar_url.data = user.avatar_url
	elif current_user.avatar_url:
		user = current_user
		avatar_form.avatar_url.data = user.avatar_url
	else:
		user = current_user

	return render_template('auth/settings.html', password_form=password_form, avatar_form=avatar_form, user=user)