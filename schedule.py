import threading, time

class MainTask(threading.Thread):
    def __init__(self, bot):
        threading.Thread.__init__(self)
        self.bot = bot
    
    def run(self):
        i = 0
        while True:
            print('main')
            self.bot.send_message(chat_id=236304646, text="I'm sorry Song Yu I'm afraid I can't do that.{0}".format(i))
            i = i + 1
            time.sleep(10)