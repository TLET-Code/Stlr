import click
import importlib
import os
import sys
from stlr import __version__

@click.group()
def cli():
	"""Stlr - A fast, modular & simple Python web framework."""
	pass

@cli.command()
@click.argument("project")
@click.option("--ip",help="IP Address to bind to",type=str,default="0.0.0.0")
@click.option("--port",help="Port to bind to",type=int,default=8081)
@click.option("--host",help="Host string (a set of IP:PORT)",type=str)
def run(project:str,host:str,ip:str,port:int):
	"""
		Serve a Stlr app in development mode forever.

	PROJECT can be in two forms:
	- main.py        (expects a "site" object)
	- main.py:obj    (imports a custom object instead of "site")
	"""

	if host and (ip or port):
		click.echo("You cannot use --host together with --ip/--port", err=True)
		sys.exit(1)
	
	if ":" in project:
		file_path, obj_name = project.split(":", 1)
	else:
		file_path, obj_name = project, "site"

	if not os.path.exists(file_path):
		click.echo(f"Project file not found: {file_path}", err=True)
		sys.exit(1)

	spec = importlib.util.spec_from_file_location("project_module", file_path)
	module = importlib.util.module_from_spec(spec)
	sys.modules["project_module"] = module
	try:
		spec.loader.exec_module(module)
	except Exception as e:
		click.echo(f"Failed to import {file_path}: {e}", err=True)
		sys.exit(1)

	site = getattr(module, obj_name, None)
	if site is None:
		click.echo(f"Could not find object '{obj_name}' in {file_path}", err=True)
		sys.exit(1)

	try:
		if host:
			site.run(host=host.split(":")[0],port=int(host.split(":")[1]))
		else:
			site.run(host=ip, port=port)
	except Exception as e:
		click.echo(f"Failed to run site: {e}", err=True)
		sys.exit(1)

@cli.command()
def version():
	"""Prints the current version and exits."""
	click.echo(__version__)
