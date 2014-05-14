from flask import render_template
from . import dj

@dj.route('/')
def index():
	return render_template('dj/index.html')