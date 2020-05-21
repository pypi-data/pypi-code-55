from cerberus.model.AbstractModelResource import AbstractModelResource
from cerberus.entities.entities import KsmSession

class KsmSessionModel(AbstractModelResource):
	"""docstring for KsmSessionModel"""
	def __init__(self, url):
		super(KsmSessionModel, self).__init__(url)
		self.url = url

	def add(self, id, active, connection_id, user_id, authentication_type_id, created_at, updated_at):
		ksmSession = KsmSession(id, active, connection_id, user_id, authentication_type_id, created_at, updated_at)
		self.insert(ksmSession)
		return ksmSession

	def get(self, id):
		ksmSession = self.session.query(KsmSession).filter(KsmSession.id == token).first()
		return ksmSession