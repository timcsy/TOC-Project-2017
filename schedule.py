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
	
	# def handle(self, scheduler):
	# 	scheduler.enter(5, 0, self.handle, argument=(scheduler,))
	# 	print('Task' + self.name)


class Scheduler:
		def __init__(self):
			pass
		
		def add_task(task, interval):
			pass
			# heapq.heappush(queue)
			
			# threading.Timer(5, handle_task).start()

class MainTask(threading.Thread):
	def __init__(self, bot):
		threading.Thread.__init__(self)
		self.bot = bot
	
	def run(self):
		self.scheduler = sched.scheduler(time.time, time.sleep)
		
		while True:
			s = input('sent to client > ')
			if s == '/exit':
				break
			elif s == '/add':
				task_name = input('enter name: ')
				self.scheduler.enter(5, 0, handle_task, argument=(Task(task_name),))
				self.scheduler.run()
				# Scheduler.add_task(Task(task_name))
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