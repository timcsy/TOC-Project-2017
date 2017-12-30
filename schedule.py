import threading, time
from datetime import datetime
import sched
import telegram

# class Scheduler:
# 		def __init__(self):
# 				self.scheduler = sched.scheduler(time.time, time.sleep)
		
# 		def add_task(period, action, *args=(), **kwargs={}):
# 				# action is function
# 				# period is second
# 				self.scheduler.enter(period, 0, add_task, args, kwargs)
# 				action()
# 				self.bot.send_message(chat_id=236304646, text=s)

def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
	menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
	if header_buttons:
		menu.insert(0, header_buttons)
	if footer_buttons:
		menu.append(footer_buttons)
	return menu

class MainTask(threading.Thread):
	def __init__(self, bot):
		threading.Thread.__init__(self)
		self.bot = bot
	
	def run(self):
		while True:
			s = input('sent to client > ')
			self.bot.send_message(chat_id=236304646, text=s)
			button_list = [
				telegram.InlineKeyboardButton("col1", callback_data='col1callbacktest'),
				telegram.InlineKeyboardButton("col2", callback_data='col2callbacktest'),
				telegram.InlineKeyboardButton("row 2", callback_data='row2callbacktest')
			]
			reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
			self.bot.send_message(chat_id=236304646, text="A two-column menu", reply_markup=reply_markup)
			self.bot.sendMessage(chat_id=236304646, text='testing custom keyboard',
                            reply_markup=telegram.ReplyKeyboardMarkup(
                                keyboard=[
                                    [telegram.KeyboardButton(text="Yes"), telegram.KeyboardButton(text="No")]
                                ]
                            ))