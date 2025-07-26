from talosbot.channels.abstract_channel import AbstractChannel
from talosbot.talos import Message
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler


# Please, note channel here is a talosbot connector to slack,
# not a slack channel by itself
class SlackChannel(AbstractChannel):
    ''' Channel for Slack (TalosBot connector) '''
    def __init__(self, app_token: str, bot_token: str, trigger_word: str='/talos') -> None:
        super().__init__()
        self.app_token = app_token
        self.bot_token = bot_token
        self.trigger_word = trigger_word if trigger_word.startswith('/') else f'/{trigger_word}'
        self.app = App(token=bot_token)
        self._build_slack_handler()

    def _build_slack_handler(self):
        '''
        Registers the slash command handler for the configured trigger word
        '''
        @self.app.command(self.trigger_word)
        def handle_message(ack, respond, command: dict) -> None:
            ack()
            user_message = command['text']
            message = Message(user_message)
            response_message = self.bot.message_handler(message)
            respond(response_message.message)

    def establish(self) -> None:
        SocketModeHandler(self.app, self.app_token).start()

    def receive_message(self) -> Message:
        '''
        Required by AbstractChannel. Not used directly in SlackChannel
        '''
        raise NotImplementedError('SlackChannel uses slash commands via decorators')

    def dispatch_message(self, message: Message) -> None:
        '''
        Required by AbstractChannel. Not used directly in SlackChannel
        '''
        raise NotImplementedError('SlackChannel uses slash commands via decorators')
