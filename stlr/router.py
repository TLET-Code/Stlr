from typing import Callable

from .Enum.HTTP import Method

class Router:
	def __init__(self) -> None:
		self.routes:dict[str,dict[Method,Callable]] = {}
	
	def add_route(self,path:str,handler:Callable,method:Method=Method.GET) -> None:
		path = path.strip("/")
		self.routes[path] = {
			method: handler
		}
	
	def match(self,path:str,method:Method) -> Callable|None:
		path = path.strip("/")
		if self.routes.get(path) is None:
			return
		return self.routes[path].get(method)
