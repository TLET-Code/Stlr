class Spice:
	def __init__(self,name:str) -> None:
		self.Name:str = name
		self.HTML_File:str=""
		self.CSS_File:str|None=None
		self.JS_Pre_File:str|None=None
		self.JS_Aft_File:str|None=None