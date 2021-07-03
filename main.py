import click
import os
import time
import sys
import traceback

import settings
from tools import utils
from tools import echo

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
		date = time.strftime("%Y-%m-%d", time.localtime())
		file_name = f'{date}-index-db.xml.gz'
		dir = f'./cache/{file_name}'
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


if __name__ == '__main__':
	echo.init_subroutine()
	cli()
