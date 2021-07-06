import json

from tools import utils

from database.anidb_database import AniDBDatabase
from database import database_settings as db_settings

db = AniDBDatabase(db_settings.CONFIG)

cursor = db.database.cursor(dictionary=True)
query = 'SELECT * FROM `anidb_anime_name`'
cursor.execute(query)
db_res = cursor.fetchall()

cursor.close()

res = {
	'time': utils.get_time_str(),
	'data': {}
}

for item in db_res:
	id_key = str(item['aid'])
	if id_key not in res['data'].keys():
		res['data'][id_key] = {
			'id': item['aid'],
			'matches': {
				'anidb': item['aid']
			},
			'names': [
				item['name']
			]
		}
	else: res['data'][id_key]['names'].append(item['name'])

with open('./data.json', 'w+', encoding='utf-8', ) as f:
    json.dump(res, f, sort_keys=True, indent='\t', ensure_ascii=False, separators=(',', ': '))
