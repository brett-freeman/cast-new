import os
from app import create_app
from flask.ext.script import Manager
from app.extensions import db

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
db.init_app(app)
manager = Manager(app)

if __name__ == '__main__':
	manager.run()