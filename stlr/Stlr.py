from flask import Flask
from flask_spicer import Spicer

from os import getenv


class Stlr:
	def __init__(
			self,
			import_name:str,

			config_folder:str="Web/Config",
			elements_folder:str="Web/Elements",
			robots_folder:str="Web/Robots",
			static_folder:str="Web/Static",
			template_folder:str="Web/Templates",

			*args,
			**kwargs
		) -> None:

		self.__flask:Flask = Flask(
			import_name=import_name,
			static_folder=static_folder,
			template_folder=template_folder,
			*args,
			**kwargs
		)

		self.__spicer:Spicer = Spicer(self.__flask,elements_folder)

		self.route = self.__flask.route
		self.run = self.__flask.run
