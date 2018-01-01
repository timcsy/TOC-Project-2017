import threading, time, sys
from datetime import datetime
import sched
import telegram



def handle_task():
	scheduler.enter(5, 0, handle_task)
	task = queue.pop(0)
	print('Task' + task.name)
	queue.append(task)

class Task:
	def __init__(self, name):
		self.name = name
	
	def handle(self, scheduler):
		scheduler.enter(5, 0, self.handle, argument=(scheduler,))
		print('Task' + self.name)


class Scheduler:
		def __init__(self):
				scheduler = sched.scheduler(time.time, time.sleep)
				queue = []
		
		def add_task(self, task):
			queue.append(task)
			handle_task()

class MainTask(threading.Thread):
	def __init__(self, bot):
		threading.Thread.__init__(self)
		self.bot = bot
	
	def run(self):
		scheduler = Scheduler()
		scheduler.run()
		while True:
			s = input('sent to client > ')
			if s == '/exit':
				break
			elif s == '/add':
				task_name = input('enter name: ')
				scheduler.add_task(Task(task_name))
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