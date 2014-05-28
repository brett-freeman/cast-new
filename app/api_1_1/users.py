from flask import jsonify, request
from . import api_1_1 as api
from ..models import User

@api.route('/users/', methods=['GET', 'POST'])
def users():
	if request.method == 'GET':
		return jsonify( users=[ user.to_json for user in User.query.all() ] )

	if request.method == 'POST':
		return request.data