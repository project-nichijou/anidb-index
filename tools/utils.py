'''
Codes in this file first appear in another project of mine.
https://github.com/JeffersonQin/typexo-cli/blob/master/lib/utils.py
'''

import sys
import requests
import unicodedata
import re
import click
import traceback
import time

from tools import echo
from tools import utils
from database.anidb_database import AniDBDatabase
from database import database_settings as db_settings 


def download_file(url, dir):
	echo.push_subroutine(sys._getframe().f_code.co_name)

	echo.clog(f'start downloading: {url} => {dir}')
	try:
		# define request headers
		headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.59'}
		# start and block request
		r = requests.get(url, stream=True, headers=headers)
		# start writing
		f = open(dir, 'wb+')
		try:
			# obtain content length
			length = int(r.headers['content-length'])
			echo.clog(f'file size: {size_description(length)}')
			# show in progressbar
			with click.progressbar(label="Downloading from remote: ", length=length) as bar:
				for chunk in r.iter_content(chunk_size = 512):
					if chunk:
						f.write(chunk)
						bar.update(len(chunk))
		except:
			for chunk in r.iter_content(chunk_size = 512):
				if chunk:
					f.write(chunk)
		echo.csuccess('Download Complete.')
		f.close()
	except Exception as err:
		echo.cerr(f'error: {repr(err)}')
		traceback.print_exc()
		db = AniDBDatabase(db_settings.CONFIG)
		db.write(table='log', values={
			'time': utils.get_time_str(),
			'content': (
				'exception caught in download_file. \n'
				f' exception info: {repr(err)} \n'
				f' traceback: \n'
				f' {traceback.format_exc()}'
			)
		})
		echo.cexit('DOWNLOAD FAILED')
	finally:
		echo.pop_subroutine()


def size_description(size):
	'''
	Taken and modified from https://blog.csdn.net/wskzgz/article/details/99293181
	'''
	def strofsize(integer, remainder, level):
		if integer >= 1024:
			remainder = integer % 1024
			integer //= 1024
			level += 1
			return strofsize(integer, remainder, level)
		else:
			return integer, remainder, level

	units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
	integer, remainder, level = strofsize(size, 0, 0)
	if level + 1 > len(units):
		level = -1
	return ( '{}.{:>03d} {}'.format(integer, remainder, units[level]) )


def slugify(value, allow_unicode=True):
	'''
	Taken and modified from django/utils/text.py
	Copyright (c) Django Software Foundation and individual contributors.
	All rights reserved.
	Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
	dashes to single dashes. Remove characters that aren't alphanumerics,
	underscores, or hyphens. Convert to lowercase. Also strip leading and
	trailing whitespace, dashes, and underscores.
	'''
	value = str(value)
	if allow_unicode:
		value = unicodedata.normalize('NFKC', value)
	else:
		value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
	value = re.sub(r'[^\w\s-]', '', value)
	return re.sub(r'[-\s]+', '-', value).strip('-_')


def get_time_str():
	return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
