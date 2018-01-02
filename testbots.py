from flask import Flask, request, send_file
from bots import *

app = Flask(__name__)
tele_bot = TelegramBot().start()

@app.route('/hook', methods=['POST'])
def webhook_handler():
	update = telegram.Update.de_json(request.get_json(force=True), tele_bot.bot)
	tele_bot.tell(update)
	return 'ok'

if __name__ == "__main__":
	app.run(threaded=True)