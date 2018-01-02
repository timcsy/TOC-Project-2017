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
			chat_actor = TelegramChatActor.start(self.actor_ref.proxy(), chat_id, self.main_actor).proxy()
			self.main_actor.register(chat_actor)
			self.chats[chat_id] = chat_actor
			chat_actor.update(update)
		print(update)
	
	def send_text(self, chat_id, message):
		self.bot.send_message(chat_id, message)


class TelegramChatActor(pykka.ThreadingActor):
	def __init__(self, parent, id, main_actor):
		super(TelegramChatActor, self).__init__()
		self.parent = parent
		self.main_actor = main_actor
		self.id = id
		self.updated = threading.Event()
		self.buffer = None

	def update(self, update):
		text = update.message.text
		chat_id = update.message.chat.id
		self.buffer = {'id': chat_id, 'text': text}
		self.updated.set()
	
	def send_text(self, message):
		self.parent.send_message(self.id, message)

	def get_id(self):
		return id
	
	def wait(self):
		self.updated.wait()
		self.updated.clear()
		return self.buffer