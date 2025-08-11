from re import findall
from jinja2 import Environment, Template
from os import path, listdir
from typing import Any

from stlr import Stlr
from .Types import Spice

class Spicer:
	def __init__(self,app:Stlr,spicer_folder:str|None="spices",cache:bool=True) -> None:
		self.__app = app
		self.__env = Environment(autoescape=True)
		self.__spicer_folder:str = spicer_folder if spicer_folder is not None else path.join(str(self.__app.template_folder),path.join("..","spices"))
		self.__pattern:str = r"&<([a-zA-Z_][a-zA-Z0-9_]*)\.([a-zA-Z_][a-zA-Z0-9_]*)>" # &<{parent}.{child}>

		self.cache:bool = cache

	def render_template_string(self,template_source:str,**context) -> str:
		"""
		Render a Jinja2 template given as a string.
		Here to replace the Flask functionality so Flask can be fully cut.
		"""
		template:Template = self.__env.from_string(template_source)
		return template.render(**context)

	def get_spices(self,_path:str|None=None) -> list[str]:
		if _path is None: _path = self.__spicer_folder
		if not path.exists(_path): raise Exception("No \"spicer\" folder was found.")
		spices:list[str] = []
		for folder in listdir(_path):
			spices.append(folder)
		return spices

	def load_spice(self,location:str,name:str) -> Spice:
		spice_folder:str = path.join(location,name)
		spice:Spice = Spice(name)
		with open(path.join(spice_folder,".html"),"r") as file:
			spice.HTML_File = file.read()
		if path.exists(path.join(spice_folder,".css")):
			with open(path.join(spice_folder,".css"),"r") as file:
				spice.CSS_File = file.read()
		if path.exists(path.join(spice_folder,".pre.js")):
			with open(path.join(spice_folder,".pre.js"),"r") as file:
				spice.JS_Pre_File = file.read()
		if path.exists(path.join(spice_folder,".aft.js")):
			with open(path.join(spice_folder,".aft.js"),"r") as file:
				spice.JS_Aft_File = file.read()
		return spice

	def render_template(self,template_name:str,**context:Any) -> str:
		"""
		Renders & patches a template.

		:param template_name: The name of the template to render.
		:param context: The variables to make available in the template.
		"""

		template_folder:str = path.join(self.__app.template_folder,template_name)

		with open(path.join(template_folder,".html"),"r") as file:
			text = file.read()
			html_template:str = self.render_template_string(text,**context)
		
		if path.exists(path.join(template_folder,".css")):
			with open(path.join(template_folder,".css"),"r") as file:
				text = file.read()
				html_template = html_template.replace("</head>",f"<style>{text}</style></head>")
		if path.exists(path.join(template_folder,".pre.js")):
			with open(path.join(template_folder,".pre.js"),"r") as file:
				text = file.read()
				html_template = html_template.replace("<body>",f"<body><script>{text}</script>")
		if path.exists(path.join(template_folder,".aft.js")):
			with open(path.join(template_folder,".aft.js"),"r") as file:
				text = file.read()
				html_template = html_template.replace("</body>",f"<script>{text}</script></body>")

		return self.patch(html_template,**context)

	def patch(self,rendered:str,**context:Any) -> str:
		"""
		Patch up an already-rendered template using Spicer.

		:param rendered: The rendered template
		:param context: Any context to pass into the spices
		"""

		constants:list[tuple[str,str]] = findall(self.__pattern,rendered)

		for constant in constants:
			spice:Spice = self.load_spice(*constant)
			spice.HTML_File = self.render_template_string(spice.HTML_File,**context)
			rendered = rendered.replace(f"&<{constant[0]}.{constant[1]}>",spice.HTML_File)
			if spice.CSS_File != None:
				rendered = rendered.replace("</head>",f"<style>{spice.CSS_File}</style></head>")
			if spice.JS_Pre_File != None:
				rendered = rendered.replace("<body>",f"<body><script>{spice.JS_Pre_File}</script>")
			if spice.JS_Aft_File != None:
				rendered = rendered.replace("</body>",f"<script>{spice.JS_Aft_File}</script></body>")

		return rendered