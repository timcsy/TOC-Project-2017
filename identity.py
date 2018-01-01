from mongodb import db

class Identity:
	@staticmethod
	def add(type, info):
		return db.identities.insert_one({
			'type': type,
			'info': info
		})

	@staticmethod
	def view(query):
		return db.identities.find(query)

	@staticmethod
	def edit(query):
		return db.identities.update_one(query)

	@staticmethod
	def remove(query):
		return db.identities.delete_one(query)