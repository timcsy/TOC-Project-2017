from config import *
import sys
from io import BytesIO
import telegram
from flask import Flask, request, send_file
from fsm import TocMachine
from schedule import *

app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)
machine = TocMachine(
    states=[
        'user',
        'state1',
        'state2',
        'instruction',
        'start',
        'pray',
        'pray_view',
        'pray_reply',
        'pray_prayed',
        'pray_remain',
        'pray_hidden',
        'pray_remind',
        'pray_my_pray',
        'pray_add',
        'pray_edit',
        'pray_remove',
        'pray_close'
    ],
    transitions=[
        ['start', 'instruction' , 'start'],
        {
            'trigger': 'go_back',
            'source': [
                'start'
            ],
            'dest': 'instruction'
        },
        ['pray', 'start' , 'pray'],
        {
            'trigger': 'go_back',
            'source': [
                'pray'
            ],
            'dest': 'start'
        },
        ['pray_add', 'pray' , 'pray_add'],
        {
            'trigger': 'pray_view',
            'source': [
                'pray'
                'pray_remind',
                'pray_my_pray',
                'pray_add'
            ],
            'dest': 'pray_view'
        },
        ['pray_reply', 'pray_view' , 'pray_reply'],
        ['pray_prayed', 'pray_view' , 'pray_prayed'],
        ['pray_remain', 'pray_view' , 'pray_remain'],
        ['pray_hidden', 'pray_view' , 'pray_hidden'],
        {
            'trigger': 'go_back',
            'source': [
                'pray_reply',
                'pray_prayed',
                'pray_remain',
                'pray_hidden'
            ],
            'dest': 'pray_view'
        },
        {
            'trigger': 'pray_remind',
            'source': [
                'pray'
                'pray_view',
                'pray_my_pray'
            ],
            'dest': 'pray_remind'
        },
        ['pray_my_pray', 'pray' , 'pray_my_pray'],
        ['pray_edit', 'pray_my_pray' , 'pray_edit'],
        ['pray_remove', 'pray_my_pray' , 'pray_remove'],
        ['pray_close', 'pray_my_pray' , 'pray_close'],
        {
            'trigger': 'go_back',
            'source': [
                'pray_edit',
                'pray_remove',
                'pray_close',
            ],
            'dest': 'pray_my_pray'
        },        
        {
            'trigger': 'go_back',
            'source': [
                'pray_view',
                'pray_remind',
                'pray_my_pray',
                'pray_add'
            ],
            'dest': 'pray'
        },
        
        



        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'state1',
            'conditions': 'is_going_to_state1'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'state2',
            'conditions': 'is_going_to_state2'
        },
        {
            'trigger': 'go_back',
            'source': [
                'state1',
                'state2'
            ],
            'dest': 'user'
        }
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)


def _set_webhook():
    status = bot.set_webhook(WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
    else:
        print('Your webhook URL has been set to "{}"'.format(WEBHOOK_URL))


@app.route('/hook', methods=['POST'])
def webhook_handler():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    print(update)
    # machine.advance(bot, update)
    return 'ok'


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    byte_io = BytesIO()
    machine.graph.draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')


if __name__ == "__main__":
    _set_webhook()
    MainTask(bot).start()
    app.run(threaded=True)