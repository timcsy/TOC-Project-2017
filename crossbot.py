from config import *
import telegram
from schedule import *
import pykka

class CrossBot:
	def __init__(self, bot_type):
		self.bot_type = bot_type
		self.queue = []
		if bot_type == 'Telegram':
			self.telegram_bot = telegram.Bot(token=TELEGRAM_API_TOKEN)

	def receive(self, message):
		self.queue.append(message)
		self.bot.send_message(chat_id=message.get_chat(), text=message.get_text())
		self.queue.pop(message)

class MainTask(threading.Thread):
	def __init__(self, bot):
		threading.Thread.__init__(self)
		self.bot = bot
		self.queue = []
		self.scheduler = Scheduler()
	
	def receive(self, message):
		s = message.get_text()

		if s == 'add':
			task_name = input('enter name: ')
			self.scheduler.add(Task(task_name))
			# Scheduler.add_task(Task(task_name))
		elif s == 'list':
			self.scheduler.list_tasks()
		elif s == 'cancel':
			n = input('Please enter the task number: ')
			task_num = int(n)
			self.scheduler.cancel(scheduler.queue[task_num][1])
		elif s == 'receive':
			for message in self.queue:
				print(message.get_text)
		self.bot.send_message(chat_id=message.get_chat(), text=message.get_text())
		# self.queue.pop(message)
	
	def run(self):
		while True:
			s = input('command > ')
			if s == 'exit':
				break
			elif s == 'add':
				task_name = input('enter name: ')
				self.scheduler.add(Task(task_name))
				# Scheduler.add_task(Task(task_name))
			elif s == 'list':
				self.scheduler.list_tasks()
			elif s == 'cancel':
				n = input('Please enter the task number: ')
				task_num = int(n)
				self.scheduler.cancel(scheduler.queue[task_num][1])
			elif s == 'receive':
				for message in self.queue:
					print(message.get_text)
			else:
				self.bot.send_message(chat_id=236304646, text=s)
				self.bot.send_message(chat_id=236304646, text="A two-column menu",
															reply_markup=telegram.InlineKeyboardMarkup(
																inline_keyboard=[
																	[telegram.InlineKeyboardButton("col1", callback_data='col1callbacktest'),
																	telegram.InlineKeyboardButton("col2", callback_data='col2callbacktest')],
																	[telegram.InlineKeyboardButton("row 2", callback_data='row2callbacktest')]
																]
															))
				self.bot.send_message(chat_id=236304646, text='testing custom keyboard',
															reply_markup=telegram.ReplyKeyboardMarkup(
																	keyboard=[
																			['太','初','有','道','，'],
																			['道','就','是','神','，'],
																			['這','道','太','初','與','神','同','在','。']
																	],
																	resize_keyboard=True,
																	one_time_keyboard=True
															))




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