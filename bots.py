from config import *
import pykka
import telegram
import sys
import threading

class TelegramBot(pykka.ThreadingActor):
	def __init__(self, bot, main_actor):
		super(TelegramBot, self).__init__()
		self.main_actor = main_actor
		self.bot = bot
		self.chats = {}
		self._set_webhook()

	def _set_webhook(self):
		status = self.bot.set_webhook(TELEGRAM_WEBHOOK_URL)
		if not status:
			print('Webhook setup failed')
			sys.exit(1)
		else:
			print('Your webhook URL has been set to "{}"'.format(TELEGRAM_WEBHOOK_URL))
	
	def update(self, update):
		chat_id = update.message.chat.id
		if chat_id in self.chats:
			self.chats[chat_id].update(update)
		else:
			chat_actor = TelegramChatActor.start(self, chat_id, self.main_actor).proxy()
			self.chats[chat_id] = chat_actor
			self.main_actor.register(chat_actor).get()
			# chat_actor.update(update)
		print(update)
	
	def send_text(self, chat_id, message):
		print('parent send text ' + message)
		self.bot.send_message(chat_id, message)


class TelegramChatActor(pykka.ThreadingActor):
	def __init__(self, parent, id, main_actor):
		super(TelegramChatActor, self).__init__()
		self.parent = parent
		self.main_actor = main_actor
		self.id = id
		self.updated = threading.Event()
		self.updated.clear()
		self.buffer = None

	def update(self, update):
		text = update.message.text
		chat_id = update.message.chat.id
		self.buffer = {'id': chat_id, 'text': text}
		print(self.buffer)
		self.updated.set()
	
	def send_text(self, message):
		print('children send ' + message)
		self.parent.send_text(self.id, message)

	def get_id(self):
		return self.id
	
	def wait(self):
		print('waiting')
		self.updated.wait()
		print('finish waiting')
		print(self.buffer)
		self.updated.clear()
		return self.buffer