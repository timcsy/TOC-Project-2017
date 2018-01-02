from config import *
import pykka
from schedule import *

class ScheduleActor(pykka.ThreadingActor):
	def __init__(self, bot):
		super(ScheduleActor, self).__init__()
		self.bot = bot
		self.scheduler = Scheduler()
		self.state = 'start'

	def on_receive(self, message):
		msg = message['msg']
		if self.state == 'start':
			if msg == 'add':
				self.state = 'add'
				self.bot.send_text('enter interval: ')
			elif msg == 'list':
				list = self.scheduler.list_tasks()
				s = ''
				for i in range(len(list)):
					s += str(i) + ': ' + str(list[i][1].interval) + '\n'
				self.bot.send_text(s)
			elif msg == 'cancel':
				self.state = 'cancel'
				self.bot.send_text('Please enter the task number: ')
			elif msg == 'exit':
				self.scheduler.queue.clear()
				self.bot.send_text('Restart')
		elif self.state == 'add':
			interval = int(msg)
			self.scheduler.add(Task(self.bot, interval))
			self.state = 'start'
		elif self.state == 'cancel':
			task_num = int(msg)
			self.scheduler.cancel(self.scheduler.queue[task_num][1])
			self.state = 'start'

# class MainTask(pykka.ThreadingActor):
# 	def __init__(self, bot):
# 		threading.Thread.__init__(self)
# 		self.bot = bot
# 		self.queue = []
# 		self.scheduler = Scheduler()
	
# 	def on_receive(self, message):
# 		s = message.text

# 		if s == 'add':
# 			task_name = input('enter name: ')
# 			self.scheduler.add(Task(task_name))
# 			# Scheduler.add_task(Task(task_name))
# 		elif s == 'list':
# 			self.scheduler.list_tasks()
# 		elif s == 'cancel':
# 			n = input('Please enter the task number: ')
# 			task_num = int(n)
# 			self.scheduler.cancel(scheduler.queue[task_num][1])
# 		elif s == 'receive':
# 			for message in self.queue:
# 				print(message.get_text)
# 		self.bot.send_message(chat_id=message.get_chat(), text=message.get_text())
# 		# self.queue.pop(message)
	
# 	def run(self):
# 		while True:
# 			s = input('command > ')
# 			if s == 'exit':
# 				break
# 			elif s == 'add':
# 				task_name = input('enter name: ')
# 				self.scheduler.add(Task(task_name))
# 				# Scheduler.add_task(Task(task_name))
# 			elif s == 'list':
# 				self.scheduler.list_tasks()
# 			elif s == 'cancel':
# 				n = input('Please enter the task number: ')
# 				task_num = int(n)
# 				self.scheduler.cancel(scheduler.queue[task_num][1])
# 			elif s == 'receive':
# 				for message in self.queue:
# 					print(message.get_text)
# 			else:
# 				self.bot.send_message(chat_id=236304646, text=s)
# 				self.bot.send_message(chat_id=236304646, text="A two-column menu",
# 															reply_markup=telegram.InlineKeyboardMarkup(
# 																inline_keyboard=[
# 																	[telegram.InlineKeyboardButton("col1", callback_data='col1callbacktest'),
# 																	telegram.InlineKeyboardButton("col2", callback_data='col2callbacktest')],
# 																	[telegram.InlineKeyboardButton("row 2", callback_data='row2callbacktest')]
# 																]
# 															))
# 				self.bot.send_message(chat_id=236304646, text='testing custom keyboard',
# 															reply_markup=telegram.ReplyKeyboardMarkup(
# 																	keyboard=[
# 																			['太','初','有','道','，'],
# 																			['道','就','是','神','，'],
# 																			['這','道','太','初','與','神','同','在','。']
# 																	],
# 																	resize_keyboard=True,
# 																	one_time_keyboard=True
# 															))