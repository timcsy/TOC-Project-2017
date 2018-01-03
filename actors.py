from config import *
import pykka
from schedule import *

class ScheduleActor(pykka.ThreadingActor):
	def __init__(self, bot):
		super(ScheduleActor, self).__init__()
		self.bot = bot
		self.tape = []
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
					if list[i].canceled == False:
						s += str(i) + ': ' + str(list[i].interval) + '\n'
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
			self.scheduler.cancel(self.scheduler.tasks[task_num])
			self.state = 'start'