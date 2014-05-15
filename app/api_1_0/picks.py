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


@api.route('/dj/update_order/<int:cast_number>', methods=['POST', 'GET'])
def update_order(cast_number):
	picks_order = request.get_json()
	picks = Pick.query.join(Pick.cast).filter(Cast.cast_number==cast_number).order_by(Pick.dj_list_position.desc()).all()
	for pick in picks:
		for pick_order in picks_order:
			if pick.id == pick_order['id']:
				pick.dj_list_position = pick_order['position']
				try:
					db.session.add(pick)
					db.session.commit()
				except Exception as e:
					return 'Yikes'
	return jsonify( picks=[pick.to_json for pick in picks] )