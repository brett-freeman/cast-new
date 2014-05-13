from . import admin
from flask import render_template, redirect, url_for, flash
from flask.ext.login import login_required, current_user
from app.extensions import db
from .decorators import admin_required
from .forms import AnnouncementForm
from ..models import Announcement

@admin.route('/', methods=['GET', 'POST'])
@login_required
@admin_required
def index():
	announcement_form = AnnouncementForm()
	if announcement_form.validate_on_submit():
		msg = Announcement(message=announcement_form.message.data)
		db.session.add(msg)
		db.session.commit()
		flash('Announcement created.')
		return redirect(url_for('admin.index'))

	return render_template('admin/index.html', announcement_form=announcement_form)

@admin.route('/announcement/<int:id>/delete')
@login_required
@admin_required
def delete_announcement(id):
	msg = Announcement.query.get(id)
	if not msg:
		flash('No such announcement.')
		return redirect(url_for('admin.index'))
	db.session.delete(msg)
	db.session.commit()
	flash('Announcement deleted')
	return redirect(url_for('cast.index'))