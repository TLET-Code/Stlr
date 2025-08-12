from http.cookies import SimpleCookie
from os import path
from typing import Callable

from .Enum import HTTP
from .spcr import Spicer
from .router import Router
from .Interfaces.Built import InMemorySessionStore
from .Interfaces.Layouts import SessionStore

class Stlr:
	def __init__(
			self,
			import_name:str,

			# Templating
			web_folder:str="Web",
			config_folder:str="Config",
			elements_folder:str="Elements",
			robots_folder:str="Robots",
			static_folder:str="Static",
			template_folder:str="Templates",
			all_in_web_folder:bool=True,

			cache_templates:bool=True,

			# Session
			session_store:SessionStore=InMemorySessionStore(),

			*args,
			**kwargs
		) -> None:

		if all_in_web_folder:
			config_folder = path.join(web_folder,config_folder)
			elements_folder = path.join(web_folder,elements_folder)
			robots_folder = path.join(web_folder,robots_folder)
			static_folder = path.join(web_folder,static_folder)
			template_folder = path.join(web_folder,template_folder)
		
		self.web_folder:str = web_folder
		self.config_folder:str = config_folder
		self.elements_folder:str = elements_folder
		self.robots_folder:str = robots_folder
		self.static_folder:str = static_folder
		self.template_folder:str = template_folder

		self.__spicer:Spicer = Spicer(self,elements_folder,cache=cache_templates)
		self.__session_store = session_store

		self.__SESSION_COOKIE:str = kwargs["session_cookie"] or "_STLR_SESSION"
		self.__SESSION_COOKIE_EXPIRY:int = kwargs["session_cookie_expiry"] or 3600

		self.render_template = self.__spicer.render_template
		self.render_template_string = self.__spicer.render_template_string
		self.router:Router = Router()

	# imma be honest gang imma not even try to
	# guess what the types for this shit are
	def __call__(self,environ,start_response):
		# cookie goblin
		cookie_header = environ.get("HTTP_COOKIE","")
		cookies = SimpleCookie(cookie_header)
		session_id = cookies.get(self.__SESSION_COOKIE)
		if session_id:
			session_id = session_id.value
		else:
			session_id = None

		session_data = self.__session_store.load(session_id) if session_id else None
		if session_data is None:
			session_id = self.__session_store.generate_session_id()
			session_data = {}
		
		environ["stlr.session"] = session_data
		self.__session_store.save(session_id,environ["stlr.session"],self.__SESSION_COOKIE_EXPIRY)#type:ignore


		# funny handling or something
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
	
	def route(self,path:str,methods:list[HTTP.Method]=[HTTP.Method.GET]) -> Callable:
		def decorator(handler:Callable) -> Callable:
			for method in methods:
				self.router.add_route(path,handler,method)
			return handler
		return decorator

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
