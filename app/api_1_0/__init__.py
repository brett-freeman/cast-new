from flask import Blueprint
api = Blueprint('api', __name__)
from . import casts, picks, users, links, errors