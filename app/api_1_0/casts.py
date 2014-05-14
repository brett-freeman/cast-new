from flask import jsonify
from . import api
from ..models import Cast, Pick

@api.route('/casts/', methods=['GET'])
@api.route('/casts/<int:cast_number>/', methods=['GET'])
def api_fetch_casts(cast_number=None):
	if cast_number:
		return jsonify( cast=Cast.query.filter_by(cast_number=cast_number).first_or_404().to_json, 
					picks=[ pick.to_json for pick in \
					Pick.query.join(Pick.cast) \
					.filter(Cast.cast_number==cast_number).all() 
					])

	return jsonify( casts=[ cast.to_json for cast in Cast.query.all() ])