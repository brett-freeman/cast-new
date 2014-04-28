from flask import jsonify
from . import api
from app.models import Link

@api.route('/links/')
def get_links():
	return jsonify(links=[link.json for link in Link.query.order_by(Link.id.desc()).all()])