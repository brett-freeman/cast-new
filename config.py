import os

basedir = os.path.abspath(os.path.dirname(__file__))
links_url = os.environ.get('HASHY_DATABASE_URL') if os.environ.get('HASHY_DATABASE_URL') else 'sqlite:////home/vagrant/am.db'

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY')

class DevelopmentConfig(Config):
	DEBUG = True
	SECRET_KEY = os.environ.get('SECRET_KEY') or '08132yh0of083n801dfhjqseCretKEYyYy'
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
	SQLALCHEMY_BINDS = {
		'links':	links_url
	}

class TestingConfig (Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
	SQLALCHEMY_BINDS = {
		'links':	links_url
	}

class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = os.environ.get('CAST_DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'data.sqlite')
	SQLALCHEMY_BINDS = {
		'links':	links_url
	}

config = {
	'development': DevelopmentConfig,
	'testing':	TestingConfig,
	'production': ProductionConfig,

	'default': DevelopmentConfig
}