import requests
import click


@click.group()
def cli():
	pass


@cli.command()
@click.option('--url', type=str, default=None, help='use other url to download database instead of the one in configuration file')
def download(url: str):
	pass


if __name__ == '__main__':
	cli()
