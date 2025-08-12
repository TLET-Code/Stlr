import abc

class SessionStore(abc.ABC):
	@abc.abstractmethod
	def load(self,session_id:str) -> dict|None:
		...

	@abc.abstractmethod
	def save(self,session_id:str,data:dict,expiry:int) -> None:
		...
	
	@abc.abstractmethod
	def generate_session_id(self) -> str:
		...
