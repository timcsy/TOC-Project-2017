import threading, time

class MainTask(threading.Thread):
    def __init__(self, bot):
        threading.Thread.__init__(self)
        self.bot = bot
    
    def run(self):
        while True:
            s = input('sent to client > ')
            self.bot.send_message(chat_id=236304646, text=s)