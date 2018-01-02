from config import *
import pykka
import telegram
import sys

class TelegramBot(pykka.ThreadingActor):
	def __init__(self):
		super(TelegramBot, self).__init__()
		self.bot = telegram.Bot(token=TELEGRAM_API_TOKEN)
		self._set_webhook()

	def _set_webhook(self):
		status = self.bot.set_webhook(TELEGRAM_WEBHOOK_URL)
		if not status:
			print('Webhook setup failed')
			sys.exit(1)
		else:
			print('Your webhook URL has been set to "{}"'.format(TELEGRAM_WEBHOOK_URL))
	
	def on_receive(self, message):
		print(message)