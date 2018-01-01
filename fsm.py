from transitions.extensions import GraphMachine


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )

    def is_going_to_state1(self, bot, update):
        text = update.message.text
        return text.lower() == 'go to state1'

    def is_going_to_state2(self, bot, update):
        text = update.message.text
        return text.lower() == 'go to state2'

    def on_enter_state1(self, bot, update):
        update.message.reply_text("I'm entering state1")
        bot.send_message(chat_id=236304646, text="waited so long")
        bot.send_message(chat_id=236304646, text=updates.message.text)
        self.go_back(update)

    def on_exit_state1(self, bot, update):
        print('Leaving state1')

    def on_enter_state2(self, bot, update):
        update.message.reply_text("I'm entering state2")
        self.go_back(update)

    def on_exit_state2(self, bot, update):
        print('Leaving state2')

    def on_enter_instruction(self, bot, update):
        print('Enter instruction')
        bot.reply_text('嗨！這是FellowBot，也就是成大信望愛團契的小助手，它可以提醒你每天要禱告，還可以幫你整理代禱事項')
        self.start(bot)

    def on_exit_instruction(self, bot, update):
        print('Exit instruction')

    def on_enter_start(self, bot, update):
        print('Enter start')
        bot.reply_text('輸入pray: 開始禱告')
        text = bot.read_text()
        if text == 'pray':
            self.pray(bot)

    def on_exit_start(self, bot, update):
        print('Exit start')




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