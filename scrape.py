from app.extensions import db
from app.models import Cast, Pick, User

import re
url_finder = re.compile(r'(?u)(?:http|https|ftp)(?:://\S+)')

def parse_picks(file_name, cast_number):
	content = [line.rstrip() for line in open(file_name) if line]
	picks = []

	for l in content:
		if l.startswith('=== '):		
			pick = {}
			if pick is not None:
				pick['cast_number'] = cast_number
				picks.append(pick)

			pick['artist'], pick['album'], pick['song'] = l.strip('=').split('/')
			pick['description'] = ''
		elif l.startswith('Link: '):
			link = re.findall(url_finder, l)
			pick['link'] = link
		elif l.startswith('[[User:'):
			pick['user'] = l.split('|')[0][7:]
		else:
			pick['description'] += l

	return picks

def add_cast(cast_number, file_name='picks.data'):
	picks = parse_picks(file_name, cast_number)
	host = User.query.filter_by(username='brett').first()
	cast = Cast.query.filter_by(cast_number=cast_number).first()

	wikiuser = User.query.filter_by(username='WikiUser').first()
	for pick in picks:
		if 'description' in pick:
			description = pick['description']
		else:
			description = 'No description.'

		if 'link' in pick:
			links = ','.join(pick['link'])
		else:
			links = 'None'

		if 'user' in pick:
			description += '(Original wiki user - ' + pick['user'] + ')'

		new_pick = Pick(artist=pick['artist'], album=pick['album'], song=pick['song'],
						cast_id=cast.id, user_id=wikiuser.id, links=links,
						description=description)
		try:
			db.session.add(new_pick)
			db.session.commit()
		except Exception as e:
			print(e)

		print('Pick added.')