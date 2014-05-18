from flask import jsonify, request
from flask.ext.login import current_user
from app.extensions import db
from . import api
from .decorators import admin_required
from ..models import Pick, Cast

@api.route('/picks/', methods=['GET'])
@api.route('/picks/<int:id>/', methods=['GET'])
def api_fetch_picks(id=None):
	if id:
		return jsonify( Pick.query.get_or_404(id).to_json )

	return jsonify( picks=[pick.to_json for pick in Pick.query.all()] )


@api.route('/dj/update_order/<int:cast_number>', methods=['PUT'])
def update_order(cast_number):
	if current_user.is_anonymous():
		return 'Must be logged in to edit pick order'
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
		return 'Uh oh, something went wrong. Send this to Brett: %s' % str(e)

	return 'Pick status for cast %s saved.' % str(cast.cast_number);

@api.route('/dj/update_played/<int:pick_id>', methods=['PUT'])
def updated_played(pick_id):
	if current_user.is_anonymous():
		return 'Must be logged in to edit play status'
		
	pick = Pick.query.get(pick_id)
	pick.played = not pick.played
	db.session.add(pick)

	try:
		db.session.commit()
	except Exception as e:
		return 'Yikes %s' % str(e)

	return 'Play status updated.'