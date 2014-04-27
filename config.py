import os

basedir = os.path.abspath(os.path.dirname(__file__))

sql_urls = {
	'main': '',
	'hashy': ''
}
secret_key = ''

class Config:
	SECRET_KEY = secret_key

class DevelopmentConfig(Config):
	DEBUG = True
	SECRET_KEY = secret_key or '08132yh0of083n801dfhjqseCretKEYyYy'
	SQLALCHEMY_DATABASE_URI = sql_urls['main'] or 'sqlite:///' + os.path.join(basedir, 'main.db')
	SQLALCHEMY_BINDS = {
		'links':	sql_urls['hashy'] or 'sqlite:///' + os.path.join(basedir, 'hashy.db')
	}

class TestingConfig (Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = sql_urls['main'] or 'sqlite:///' + os.path.join(basedir, 'main.db')
	SQLALCHEMY_BINDS = {
		'links':	sql_urls['hashy'] or 'sqlite:///' + os.path.join(basedir, 'hashy.db')
	}

class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = sql_urls['main'] or 'sqlite:///' + os.path.join(basedir, 'main.db')
	SQLALCHEMY_BINDS = {
		'links':	sql_urls['hashy'] or 'sqlite:///' + os.path.join(basedir, 'hashy.db')
	}

config = {
	'development': DevelopmentConfig,
	'testing':	TestingConfig,
	'production': ProductionConfig,

	'default': DevelopmentConfig
}