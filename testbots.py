from flask import Flask, request, send_file
from bots import *

app = Flask(__name__)


@app.route('/hook', methods=['POST'])
def webhook_handler():
	update = telegram.Update.de_json(request.get_json(force=True), bot)
	tele_bot.tell(update)
	return 'ok'

if __name__ == "__main__":
	bot = telegram.Bot(token=TELEGRAM_API_TOKEN)
	tele_bot = TelegramBot.start(bot)
	app.run(threaded=True)