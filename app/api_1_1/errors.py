from flask import jsonify

def bad_request(message):
	response = jsonify({'status': 'bad request', 'message': message})
	response.status_code = 400
	return response

def unauthorized(message):
	response = jsonify({'status': 'unauthorized', 'message': message})
	response.status_code = 401
	return response

def forbidden(message):
	response = jsonify({'status': 'forbidden', 'message': message})
	response.status_code = 403
	return response

def not_found(message):
	response = jsonify({'status': 'not found', 'message': message})
	response.status_code = 404
	return response