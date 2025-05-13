from talosbot.channels.abstract_channel import AbstractChannel
from talosbot.talos import Message

class CLIChannel(AbstractChannel):
    def __init__(self) -> None:
        super().__init__()

    def recieve_message(self) -> Message:
        '''
        Returns the message obtained from the stdin
        '''
        msg = input('Me: ')
        return Message(msg)
    
    def dispatch_message(self, message: Message) -> None:
        '''
        Returns the message to the stdout
        '''
        print(f'Bot: {message.message}')

    def establish(self) -> None:
        '''
        Makes an execution loop with the in/out message
        '''
        while True:
            message = self.recieve_message()
            response_message = self.bot.message_handler(message)
            self.dispatch_message(response_message)
