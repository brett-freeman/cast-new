import requests
from app.models import User, Cast, Pick
from app.extensions import db

def load_users():
	r = requests.get('http://localhost:8000/api/users/')
	users = r.json()
	for index, user in enumerate(users['users']):
		new_user = User(id=user['id'], username=user['username'], password='weed')
		try:
			db.session.add(new_user)
			db.session.commit()
			print('Adding user ' + user['username'] + ' successful')
		except:
			print('Error adding user ' + user['username'])

def load_data():
	r = requests.get('http://localhost:8000/api/casts/')
	data = r.json()
	casts = data['casts']
	for cast in casts:
		new_cast = Cast(id=int(cast['id']),
						time=cast['time'], date=cast['date'], 
						cast_number=int(cast['bongcast_number']),
						description=cast['desc'], 
						picture_url=cast['picture_url'], 
						host_id=int(cast['host_id']))
		try:
			db.session.add(new_cast)
			db.session.commit()
			print('Adding cast ' + str(cast['bongcast_number']) + ' successful')
		except Exception as e:
			print(e)

		for pick in cast['picks']:
			build_links = [pick['waffles_link'], pick['what_link'], pick['other_link']]
			new_pick = Pick(id=int(pick['id']),
							cast_id=int(cast['id']),
							user_id=int(pick['user_id']),
							artist=pick['artist'],
							album=pick['album'],
							song=pick['song'],
							description=pick['desc'],
							date_added=pick['date_added'],
							picture_url=pick['picture_url'],
							links=','.join(build_links))
			try:
				db.session.add(new_pick)
				db.session.commit()
			except Exception as e:
				print(e)