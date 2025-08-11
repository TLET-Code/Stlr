from flask import Flask
from flask_spicer import Spicer

from os import path

from typing import Callable

from .Enum import HTTP
from .router import Router

class Stlr:
	def __init__(
			self,
			import_name:str,

			web_folder:str="Web",
			config_folder:str="Config",
			elements_folder:str="Elements",
			robots_folder:str="Robots",
			static_folder:str="Static",
			template_folder:str="Templates",
			all_in_web_folder:bool=True,

			*args,
			**kwargs
		) -> None:

		if all_in_web_folder:
			config_folder = path.join(web_folder,config_folder)
			elements_folder = path.join(web_folder,elements_folder)
			robots_folder = path.join(web_folder,robots_folder)
			static_folder = path.join(web_folder,static_folder)
			template_folder = path.join(web_folder,template_folder)

		# TODO: Implement Spicer-like templating with Flask templates.
		# TODO: Fully remove Flask.
		self.__flask:Flask = Flask(
			import_name=import_name,
			static_folder=static_folder,
			template_folder=template_folder,
			*args,
			**kwargs
		)
		self.__spicer:Spicer = Spicer(self.__flask,elements_folder)

		self.router:Router = Router()
	
	def route(self,path:str,methods:list[HTTP.Method]=[HTTP.Method.GET]) -> Callable:
		def decorator(handler:Callable) -> Callable:
			for method in methods:
				self.router.add_route(path,handler,method)
			return handler
		return decorator

	# imma be honest gang imma not even try to
	# guess what the types for this shit are
	def __call__(self,environ,start_response):
		method = environ["REQUEST_METHOD"]
		path = environ["PATH_INFO"]

		handler:Callable|None = self.router.match(path,method)
		if handler:
			response_body = handler()
			status = "200 OK"
			headers = [("Content-Type","text/html")]
			start_response(status,headers)
			return [response_body.encode("UTF-8")]
		status = "404 Not Found"
		headers = [("Content-Type","text/plain")]
		start_response(status,headers)
		return [b"Not Found"]

	def run(self,host:str,port:int=80) -> None:
		"""
		Serves forever. ONLY for development use.
		"""
		from wsgiref.simple_server import make_server
		with make_server(host,port,self) as httpd:
			print(f"Serving on port {port}...")
			try:
				httpd.serve_forever()
			except KeyboardInterrupt:
				print("Server terminated.")
