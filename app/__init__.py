from flask import Flask, send_from_directory, g, flash
from config import config
from app.extensions import bootstrap, login_manager, moment
from app.models import Pick, Announcement, Cast
import flask.ext.whooshalchemy as whooshalchemy
import os

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])

	# Register our blueprints
	from .cast import cast as cast_blueprint
	from .auth import auth as auth_blueprint
	from .api_1_0 import api as api_blueprint
	from .admin import admin as admin_blueprint
	app.register_blueprint(cast_blueprint)
	app.register_blueprint(auth_blueprint, url_prefix='/auth')
	app.register_blueprint(api_blueprint, url_prefix='/api/1.0')
	app.register_blueprint(admin_blueprint, url_prefix='/admin')

	# Initialize any extensions we are using
	bootstrap.init_app(app)
	login_manager.init_app(app)
	moment.init_app(app)
	def nl2br(value):
		return value.replace('\n','<br>\n')
	app.jinja_env.filters['nl2br'] = nl2br

	@app.route('/robots.txt')
	def robots_from_static():
		return send_from_directory(os.path.join(app.root_path, 'static'), 'robots.txt')

	@app.before_request
	def before_request():
		g.next_cast = Cast.query.order_by(Cast.cast_number.desc()).first()
		msgs = Announcement.query.all()
		if msgs:
			for msg in msgs:
				flash('%s' % msg.message, '%sannouncement' % msg.id)

	whooshalchemy.whoosh_index(app, Pick)
	return app