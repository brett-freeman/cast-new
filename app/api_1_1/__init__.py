from flask import Blueprint, render_template
api_1_1 = Blueprint('api_1_1', __name__)
from . import casts, picks, users, links, errors

@api_1_1.route('/')
def index():
	return render_template('api_1_1/index.html')