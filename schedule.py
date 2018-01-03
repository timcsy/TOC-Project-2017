import threading, sched
import heapq
import time, sys
from datetime import datetime
import telegram

class Task:
	def __init__(self, bot, interval):
		self.bot = bot
		self.interval = interval
		self.canceled = False
		
	def start(self):
		self.bot.send_text("Task " + str(self.interval) + ' expired')

	def next_time(self):
		return self.interval

class Scheduler:
	def __init__(self):
		self.tasks = []
		self.queue = []
		self.thread = None
		
	def add(self, task):
		self.tasks.append(task)
		now = time.time()
		next_time = task.next_time()
		heapq.heappush(self.queue, (now + next_time, task))
		print("in")
		self.next()
		print("out")
		# if len(self.queue) == 1:
		# 	self.thread = threading.Timer(next_time, self.run)
		# 	self.thread.start()

	def cancel(self, task):
		task.canceled = True
	
	def run(self):
		while len(self.queue) > 0 and self.queue[0][1].canceled == True:
			heapq.heappop(self.queue)
		if len(self.queue) > 0:
			timestamp, task = heapq.heappop(self.queue)
			self.next()
			# now = time.time()
			# next_time = 0
			# if len(self.queue) > 0 and self.queue[0][0] > now:
			# 	next_time = self.queue[0][0] - now
			# self.thread = threading.Timer(next_time, self.run)
			# self.thread.start()
			task.start()
			if task.canceled != True:
				self.add(task)
	
	def next(self):
		if not self.thread == None:
			self.thread.cancel()
		if len(self.queue) > 0:
			now = time.time()
			next_time = 0
			if self.queue[0][0] > now:
				next_time = self.queue[0][0] - now
			self.thread = threading.Timer(next_time, self.run)
			print("start")
			self.thread.start()
			print("next")
	
	def list_tasks(self):
		# for i in range(len(self.queue)):
		# 	print(str(i) + ': ' + self.queue[i][1].name)
		return self.tasks