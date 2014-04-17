from flask import Blueprint
cast = Blueprint('cast', __name__)
from . import routes