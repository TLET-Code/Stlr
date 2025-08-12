import time
import secrets

from ..Layouts import SessionStore

class InMemorySessionStore(SessionStore):
	def __init__(self) -> None:
		self.__store:dict[str,tuple[dict,float]] = {}

	def load(self,session_id:str) -> dict|None:
		record = self.__store.get(session_id)
		if not record:
			return
		data,expiry = record
		if expiry < time.time():
			del self.__store[session_id]
			return
		return data
	
	def save(self,session_id:str,data:dict,expiry:int) -> None:
		expiry_timestamp = time.time()+expiry
		self.__store[session_id] = (data,expiry_timestamp)

	def generate_session_id(self) -> str:
		return secrets.token_urlsafe(32)
