from flask import Blueprint, render_template
api = Blueprint('api', __name__)
from . import casts, picks, users, links, errors

@api.route('/')
def index():
	return render_template('api_1_0/index.html')