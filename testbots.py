from flask import Flask, request, send_file
from config import *
import pykka
import telegram
import sys

class TelegramBot(pykka.ThreadingActor):
	def __init__(self, bot):
		super(TelegramBot, self).__init__()
		self.bot = bot
		self._set_webhook()

	def _set_webhook(self):
		status = self.bot.set_webhook(TELEGRAM_WEBHOOK_URL)
		if not status:
			print('Webhook setup failed')
			sys.exit(1)
		else:
			print('Your webhook URL has been set to "{}"'.format(TELEGRAM_WEBHOOK_URL))
	
	def on_receive(self, message):
		print(message)

class Greeter(pykka.ThreadingActor):
    def on_receive(self, message):
        return 'Hi there!'



app = Flask(__name__)
bot = telegram.Bot(token=TELEGRAM_API_TOKEN)
tele_bot = TelegramBot.start(bot)

@app.route('/hook', methods=['POST'])
def webhook_handler():
	update = telegram.Update.de_json(request.get_json(force=True), bot)
	tele_bot.tell(update)
	return 'ok'

if __name__ == "__main__":
	actor_ref = Greeter.start()
	answer = actor_ref.ask({'msg': 'Hi?'})
	print(answer)
	tele_bot.tell('Hello')
	app.run()
	tele_bot.stop()