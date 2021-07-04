import click
import os
import time
import sys
import traceback
import gzip
from xml.etree import ElementTree as ET

import settings
from tools import utils
from tools import echo
from database.anidb_database import AniDBDatabase
from database import database_settings as db_settings 

file_dir = None
db = AniDBDatabase(db_settings.CONFIG)


@click.group()
def cli():
	pass


@cli.command()
@click.option('--url', type=str, default=None, help='use other url to download database instead of the one in the configuration file')
@click.option('--ignore_cache', is_flag=True, default=False, help='whether to ignore cache files')
def download(url: str, ignore_cache: bool):
	'''
	download the anidb title index database dump
	'''
	echo.push_subroutine(sys._getframe().f_code.co_name)

	if url == None or url == '': download_url = settings.ANIDB_INDEX_URL
	else: download_url = url

	try:
		dir = get_cache_dir_today()
		if not os.path.exists(dir) or ignore_cache:
			utils.download_file(download_url, dir)
		else:
			echo.csuccess('cache file found')
	except Exception as err:
		echo.cerr(f'error: {repr(err)}')
		traceback.print_exc()
		db.write(table='log', values={
			'time': utils.get_time_str(),
			'content': (
				'exception caught in download cli. \n'
				f' exception info: {repr(err)} \n'
				f' traceback: \n'
				f' {traceback.format_exc()}'
			)
		})
		echo.cexit('FAILED IN DOWNLOAD CLI')
	finally:
		echo.pop_subroutine()


@cli.command()
@click.pass_context
def parse(ctx):
	'''
	download then save the parse and save the result into the database
	'''
	echo.push_subroutine(sys._getframe().f_code.co_name)

	try:
		# download section
		echo.clog('start downloading ...')
		ctx.invoke(download)
		# unzip the cache file
		dir = get_cache_dir_today()
		f = gzip.open(dir, 'rb')
		content = f.read().decode('utf-8')
		# parse xml contents
		root = ET.fromstring(content)
		animes = root.findall('./anime')
		with click.progressbar(label='Parsing animes: ', length=len(animes)) as bar:
			for anime in animes:
				aid = anime.get('aid')
				for title in anime.findall("./title"):
					name = title.text
					res = {
						'aid': aid,
						'name': name
					}
					db.write('anidb_anime_name', values=res)
				bar.update(1)
	except Exception as err:
		echo.cerr(f'error: {repr(err)}')
		traceback.print_exc()
		db.write(table='log', values={
			'time': utils.get_time_str(),
			'content': (
				'exception caught in parse cli. \n'
				f' exception info: {repr(err)} \n'
				f' traceback: \n'
				f' {traceback.format_exc()}'
			)
		})
		echo.cexit('FAILED IN PARSE CLI')
	finally:
		echo.pop_subroutine()


def get_cache_dir_today():
	global file_dir
	if file_dir is not None: return file_dir
	date = time.strftime("%Y-%m-%d", time.localtime())
	file_name = f'{date}-index-db.xml.gz'
	file_dir = f'./cache/{file_name}'
	return file_dir


if __name__ == '__main__':
	echo.init_subroutine()
	cli()
