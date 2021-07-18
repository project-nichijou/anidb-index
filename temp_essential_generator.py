import json

from tools import utils

from database.anidb_database import AniDBDatabase

db_res = AniDBDatabase().read_all('anime_name', ['*'])

res = {
	'time': utils.get_time_str(),
	'data': {}
}

sorted(db_res, key=lambda x: x['id'])
id_arr = []
inc_id = 0

for item in db_res:
	if item['id'] not in id_arr:
		id_arr.append(item['id'])
		inc_id += 1
		res['data'][str(inc_id)] = [
			item['name']
		]
	else: res['data'][str(inc_id)].append(item['name'])

with open('./data.json', 'w+', encoding='utf-8', ) as f:
    json.dump(res, f, sort_keys=True, indent='\t', ensure_ascii=False, separators=(',', ': '))