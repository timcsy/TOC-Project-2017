from flask import Flask, request, send_file
from bots import *

class MainActor(pykka.ThreadingActor):
	def __init__(self):
		super(MainActor, self).__init__()
		self.actors = []

	def register(self, actor):
		self.actors.append(actor)
		print('Registered ' + str(actor.get_id().get()))
		s = actor.wait().get()
		print('Read' + s)
		actor.send_text(s).get()

app = Flask(__name__)

@app.route('/hook', methods=['POST'])
def webhook_handler():
	update = telegram.Update.de_json(request.get_json(force=True), bot)
	tele_bot.update(update)
	return 'ok'

if __name__ == "__main__":
	main_actor = MainActor.start().proxy()

	bot = telegram.Bot(token=TELEGRAM_API_TOKEN)
	tele_bot = TelegramBot.start(bot, main_actor).proxy()
	
	app.run()
	pykka.ActorRegistry.stop_all()