import threading, time
from datetime import datetime
import sched

# class Scheduler:
# 		def __init__(self):
# 				self.scheduler = sched.scheduler(time.time, time.sleep)
		
# 		def add_task(period, action, *args=(), **kwargs={}):
# 				# action is function
# 				# period is second
# 				self.scheduler.enter(period, 0, add_task, args, kwargs)
# 				action()
# 				self.bot.send_message(chat_id=236304646, text=s)

class MainTask(threading.Thread):
    def __init__(self, bot):
        threading.Thread.__init__(self)
        self.bot = bot
    
    def run(self):
        while True:
            s = input('sent to client > ')
            self.bot.send_message(chat_id=236304646, text=s)