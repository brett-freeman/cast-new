from flask import render_template, redirect, request, url_for, flash, abort
from flask.ext.login import login_user, logout_user, login_required
from app.extensions import db
from sqlalchemy.exc import IntegrityError
from . import auth
from .forms import RegisterForm, LoginForm
from ..models import User

@auth.route('/login', methods=['GET', 'POST'])
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

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been logged out.')
	return redirect(url_for('cast.index'))

@auth.route('/register', methods=['GET', 'POST'])
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