import time
import secrets
import redis
from json import loads, dumps

from ..Layouts import SessionStore

class RedisSessionStore(SessionStore):
	def __init__(self,redis:redis.Redis,expiry_seconds:int=3600) -> None:
		self.__redis = redis
		self.__expiry = expiry_seconds

	def load(self,session_id:str) -> dict|None:
		record = self.__redis.get(session_id)
		if not record:
			return
		return loads(record)#type:ignore
	
	def save(self,session_id:str,data:dict,expiry:int) -> None:
		self.__redis.setex(session_id,expiry,dumps(data))

	def generate_session_id(self) -> str:
		return secrets.token_urlsafe(32)
