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


file_dir = None


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
		for anime in root.findall('./anime'):
			aid = anime.get('aid')
			for title_element in anime.findall("./title"):
				title = title_element.text
				res = {
					'aid': aid,
					'title': title
				}
				
	except Exception as err:
		echo.cerr(f'error: {repr(err)}')
		traceback.print_exc()
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
