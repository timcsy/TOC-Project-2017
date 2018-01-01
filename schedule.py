import threading, sched
import heapq
import time, sys
from datetime import datetime
import telegram

class Task:
	def __init__(self, name):
		self.name = name
		self.canceled = False

	def start(self):
		print("Task " + self.name)

	def next_time(self):
		return 5

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
		while len(self.queue) > 0 and self.queue[0][1].canceled == True:
			heapq.heappop(self.queue)
		if len(self.queue) > 0:
			timestamp, task = heapq.heappop(self.queue)
			now = time.time()
			next_time = 0
			if len(self.queue) > 0 and self.queue[0][0] > now:
				next_time = self.queue[0][0] - now
			threading.Timer(next_time, self.run).start()
			task.start()
			if task.canceled != True:
				self.add(task)
	
	def list_tasks(self):
		for i in range(len(self.queue)):
			print(str(i) + ': ' + self.queue[i][1].name)