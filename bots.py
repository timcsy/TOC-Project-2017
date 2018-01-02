from config import *
import pykka
import telegram
import sys
import threading
from actors import *

class TelegramBot(pykka.ThreadingActor):
	def __init__(self, bot):
		super(TelegramBot, self).__init__()
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
		if not chat_id in self.chats:
			self.chats[chat_id] = TelegramChatActor.start(self, chat_id).proxy()
			print('TelegramChatActor created for chat: ' + str(chat_id))
		self.chats[chat_id].update(update).get()
		print(update)
	
	def send_text(self, chat_id, message):
		print('parent send text ' + message)
		self.bot.send_message(chat_id, message)


class TelegramChatActor(pykka.ThreadingActor):
	def __init__(self, tele_bot, id):
		super(TelegramChatActor, self).__init__()
		self.tele_bot = tele_bot
		self.id = id
		self.state = 'start'
	
	def update(self, update):
		text = update.message.text
		if self.state == 'start':
			if text == '/schedule':
				self.schedule_actor = ScheduleActor.start(self)
				print('ScheduleActor created')
				self.state = 'schedule'
		elif self.state == 'schedule':
			print('TelegramChatActor received: ' + text)
			s = self.schedule_actor.ask({'msg': text})
			print(s)

	def send_text(self, message):
		print('children send ' + message)
		self.tele_bot.send_text(self.id, message)