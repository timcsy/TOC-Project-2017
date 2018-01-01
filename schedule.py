import threading, sched
import heapq
import time, sys
from datetime import datetime
import telegram

queue = []


def handle_task(task):
	# task = queue.pop(0)
	print('Task' + task.name)
	# scheduler.enter(5, 0, handle_task, argument=(task,))
	# threading.Timer(5, handle_task).start()
	# queue.append(task)

class Task:
	def __init__(self, name):
		self.name = name
		self.canceled = False

	def next_time(self):
		return 5

	def start(self):
		print("Task " + self.name)
	
	# def handle(self, scheduler):
	# 	scheduler.enter(5, 0, self.handle, argument=(scheduler,))
	# 	print('Task' + self.name)


class Scheduler:
	def __init__(self):
		self.queue = []
		
	def add(self, task):
		now = time.time()
		next_time = task.next_time()
		heapq.heappush(self.queue, (now + next_time, task))
		if len(self.queue) == 1:
			threading.Timer(next_time, self.run).start()

	def cancel(self, task):
		task.canceled = True
	
	def run(self):
		timestamp, task = heapq.heappop(self.queue)
		while len(self.queue) > 0 and self.queue[0][1].canceled == True:
			heapq.heappop(self.queue)
		if len(self.queue) > 0:
			now = time.time()
			next_time = 0
			if self.queue[0][0] > now:
				next_time = self.queue[0][0] - now
			threading.Timer(next_time, self.run).start()
		task.start()
		if task.canceled != True:
			self.add(task)
	
	def list_tasks(self):
		for i in range(len(self.queue)):
			print(str(i) + ': ' + self.queue[i][1].name)
		# threading.Timer(5, handle_task).start()

class MainTask(threading.Thread):
	def __init__(self, bot):
		threading.Thread.__init__(self)
		self.bot = bot
	
	def run(self):
		scheduler = Scheduler()
		while True:
			s = input('sent to client > ')
			if s == '/exit':
				break
			elif s == '/add':
				task_name = input('enter name: ')
				scheduler.add(Task(task_name))
				# Scheduler.add_task(Task(task_name))
			elif s == '/list':
				scheduler.list_tasks()
			elif s == '/cancel':
				n = input('Please enter the task number: ')
				task_num = int(n)
				scheduler.cancel(scheduler.queue[task_num][1])
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