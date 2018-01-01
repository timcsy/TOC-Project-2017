class Message:
	def __init__(self, bot_type, message):
		self.bot_type = bot_type
		self.message = message

	def get_text(self):
		if self.bot_type == 'Telegram':
			return self.message.text
	
	def get_chat(self):
		if self.bot_type == 'Telegram':
			return self.message.message.chat.id