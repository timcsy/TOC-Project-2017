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
