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
		self.push(task)

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
				self.push(task)
	
	def push(self, task):
		now = time.time()
		next_time = task.next_time()
		heapq.heappush(self.queue, (now + next_time, task))
		self.next()
		# if len(self.queue) == 1:
		# 	self.thread = threading.Timer(next_time, self.run)
		# 	self.thread.start()
	
	def next(self):
		if not self.thread == None:
			self.thread.cancel()
		if len(self.queue) > 0:
			now = time.time()
			next_time = 0
			if self.queue[0][0] > now:
				next_time = self.queue[0][0] - now
			self.thread = threading.Timer(next_time, self.run)
			self.thread.start()
	
	def list_tasks(self):
		# for i in range(len(self.queue)):
		# 	print(str(i) + ': ' + self.queue[i][1].name)
		return self.tasks