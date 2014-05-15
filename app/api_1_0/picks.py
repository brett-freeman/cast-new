from flask import jsonify, request
from app.extensions import db
from . import api
from ..models import Pick, Cast

@api.route('/picks/', methods=['GET'])
@api.route('/picks/<int:id>/', methods=['GET'])
def api_fetch_picks(id=None):
	if id:
		return jsonify( Pick.query.get_or_404(id).to_json )

	return jsonify( picks=[pick.to_json for pick in Pick.query.all()] )


@api.route('/dj/update_order/<int:cast_number>', methods=['PUT', 'GET'])
def update_order(cast_number):
	picks_order = request.get_json()
	cast = Cast.query.filter_by(cast_number=cast_number).first()
	for pick in cast.picks:
		for pick_order in picks_order:
			if pick.id == pick_order['id'] and pick.dj_list_position != pick_order['position']:
				pick.dj_list_position = pick_order['position']
				db.session.add(pick)
			else:
				pass
	try:
		db.session.commit()
	except Exception as e:
		return 'Yikes %s' % str(e)
		
	return jsonify( picks=[pick.to_json for pick in cast.picks] )