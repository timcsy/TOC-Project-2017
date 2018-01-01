from config import *
import telegram

class CrossBot:
	def __init__(self, type):
		self.type = type

		if type == 'Telegram':
			self.telegram_bot = telegram.Bot(token=TELEGRAM_API_TOKEN)

	def reply_text(self, text):
		if self.type == 'Telegram':
			pass

	