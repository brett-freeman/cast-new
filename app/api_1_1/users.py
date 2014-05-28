from flask import jsonify, request
from . import api_1_1 as api
from ..models import User

@api.route('/users/', methods=['GET', 'POST'])
def users():
	'''
	API Method for fetching a list of all users
	'''
	if request.method == 'GET':
		return jsonify( users=[ user.to_json for user in User.query.all() ] )

	if request.method == 'POST':
		return request.data

@api.route('/users/<string:username>', methods=['GET', 'PUT'])
def user(username):
	'''
	API Method for fetching an individual user by username, or editing
	a user's data by username
	'''
	if request.method == 'GET':
		return jsonify( User.query.filter_by(username=username).first_or_404().to_json )
