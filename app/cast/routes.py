from flask import render_template
from . import cast
from .forms import PickForm

@cast.route('/')
def index():
	return render_template('cast/index.html')

@cast.route('/pick', methods=['GET', 'POST'])
def pick():
	form = PickForm()

	return render_template('cast/pick.html', form=form)