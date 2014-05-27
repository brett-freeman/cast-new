from . import admin
from flask import render_template, redirect, url_for, flash
from flask.ext.login import login_required, current_user
from app.extensions import db
from .decorators import admin_required
from .forms import AnnouncementForm, PickUserForm
from ..models import Announcement, User

@admin.before_request
@login_required
@admin_required
def admin_before_request():
	pass

@admin.route('/', methods=['GET', 'POST'])
def index():
	announcement_form = AnnouncementForm()
	pick_user_form = PickUserForm()
	pick_user_form.user.choices = [ (user.id, user.username) for user in User.query.all()]

	if announcement_form.validate_on_submit():
		msg = Announcement(message=announcement_form.message.data)
		db.session.add(msg)
		db.session.commit()
		flash('Announcement created.')
		return redirect(url_for('admin.index'))

	if pick_user_form.validate_on_submit():
		user = User.query.get(pick_user_form.user.data)
		return redirect(url_for('auth.edit_user', username=user.username))

	return render_template('admin/index.html', announcement_form=announcement_form, pick_user_form=pick_user_form)

@admin.route('/announcement/<int:id>/delete')
def delete_announcement(id):
	msg = Announcement.query.get(id)
	if not msg:
		flash('No such announcement.')
		return redirect(url_for('admin.index'))
	db.session.delete(msg)
	db.session.commit()
	flash('Announcement deleted')
	return redirect(url_for('cast.index'))

@admin.route('/new/', methods=['GET', 'POST'])
def new_index():
	return render_template('admin/new_index.html')