from flask import jsonify
from . import api
from ..models import User

@api.route('/users/', methods=['GET'])
@api.route('/users/<string:username>/', methods=['GET'])
@api.route('/users/<int:user_id>/', methods=['GET'])
def api_fetch_users(username=None, user_id=None):
	if username:
		return jsonify( User.query.filter_by(username=username).first_or_404().to_json )
	if user_id:
		return jsonify( User.query.get_or_404(user_id).to_json )

	return jsonify( users=[user.to_json for user in User.query.all()] )