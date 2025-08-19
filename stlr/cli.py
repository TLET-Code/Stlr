import click
from stlr import __version__

@click.group()
def cli():
	"""Stlr - A fast, modular & simple Python web framework."""
	pass

@cli.command()
def run():
	"""Serve a Stlr app in development mode forever."""
	click.echo("...")

@cli.command()
def version():
	"""Prints the current version and exits."""
	click.echo(__version__)
