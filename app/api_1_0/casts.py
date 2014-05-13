from flask import jsonify
from . import api
from ..models import Cast, Pick

@api.route('/casts/', methods=['GET'])
@api.route('/casts/<int:id>/', methods=['GET'])
def api_fetch_casts(id=None):
	if id:
		return jsonify( cast=Cast.query.get_or_404(id).to_json, 
						picks=[ pick.to_json for pick in Pick.query.filter_by(cast_id=id).all() ])

	return jsonify( casts=[ cast.to_json for cast in Cast.query.all() ])