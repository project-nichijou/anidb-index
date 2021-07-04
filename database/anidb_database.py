import traceback
import mysql.connector
import copy


from database import anidb_database_command as db_commands
from tools import utils


class AniDBDatabase(object):
	
	def __init__(self, config):
		self.config = config
		self.check_database()
		self.database = mysql.connector.connect(**config)
		self.check_tables()

	def check_database(self):
		t_config = copy.deepcopy(self.config)
		if 'database' in t_config.keys():
			t_config.pop('database')
		db = mysql.connector.connect(**t_config)
		cursor = db.cursor()
		cursor.execute(f'CREATE DATABASE IF NOT EXISTS `{self.config["database"]}`')
		cursor.close()

	def check_tables(self):
		cursor = self.database.cursor()
		cursor.execute(db_commands.CREATE_TABLE_ANIME_NAME)
		cursor.execute(db_commands.CREATE_TABLE_LOG)
		cursor.close()

	def write(self, table: str, values: dict):
		try:
			keys = values.keys()
			
			cmd_line_table = f'INSERT INTO {table} '
			cmd_line_keys = f'({", ".join(f"`{key}`" for key in keys)}) '
			cmd_line_values = f'VALUES ({", ".join(f"%({key})s" for key in keys)}) '
			cmd_line_update = f'ON DUPLICATE KEY UPDATE {", ".join(f"`{key}` = %({key})s" for key in keys)}'
			
			command = '\n'.join([cmd_line_table, cmd_line_keys, cmd_line_values, cmd_line_update])
			
			cursor = self.database.cursor()
			cursor.execute(command, values)

			self.database.commit()
			cursor.close()
		except Exception as e:
			self.write(table='log', values={
				'time': utils.get_time_str(),
				'content': (
					'exception caught when writing to database. \n'
					f' table: {table} \n'
					f' values: {repr(values)}'
					f' exception info: {repr(e)} \n'
					f' traceback: \n'
					f' {traceback.format_exc()}'
				)
			})

	def del_log_all(self):
		try:
			cursor = self.database.cursor()

			delete = 'TRUNCATE `log`'
			cursor.execute(delete)
			
			self.database.commit()
			cursor.close()
		except Exception as e:
			self.write(table='log', values={
				'time': utils.get_time_str(),
				'content': (
					'exception caught when deleting all loggings. \n'
					f' exception info: {repr(e)} \n'
					f' traceback: \n'
					f' {traceback.format_exc()}'
				)
			})
	
	def del_log_till(self, time: str):
		try:
			cursor = self.database.cursor()

			delete = f'DELETE FROM `log` WHERE `time` <= {repr(time)}'
			cursor.execute(delete)
			
			self.database.commit()
			cursor.close()
		except Exception as e:
			self.write(table='log', values={
				'time': utils.get_time_str(),
				'content': (
					'exception caught when deleting loggings before exact time. \n'
					f' time: {time} \n'
					f' exception info: {repr(e)} \n'
					f' traceback: \n'
					f' {traceback.format_exc()}'
				)
			})

	def close(self):
		self.database.close()
