from flask import jsonify
from . import api
from ..models import Pick

@api.route('/picks/', methods=['GET'])
@api.route('/picks/<int:id>/', methods=['GET'])
def api_fetch_picks(id=None):
	if id:
		return jsonify( Pick.query.get_or_404(id).to_json )

	return jsonify( picks=[pick.to_json for pick in Pick.query.all()] )