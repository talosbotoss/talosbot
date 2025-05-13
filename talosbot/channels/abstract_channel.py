from abc import ABC, abstractmethod
from talosbot.talos import Message


class AbstractChannel(ABC):
    ''' Abstract channel '''
    def __init__(self) -> None:
        super().__init__()
        self.bot = None
    
    def set_bot(self, bot):
        '''
        This is required in order to access back to the bot skill execution
        '''
        self.bot = bot

    @abstractmethod
    def recieve_message(self) -> Message:
        '''
        Gets a new message from the channel and returns it
        '''
        pass
    
    @abstractmethod
    def dispatch_message(self, message: Message) -> None:
        '''
        Returns the message back to the channel
        '''
        pass

    @abstractmethod
    def establish(self) -> None:
        '''
        This method starts the communication and it's executed in the
        bot run stage with the corresponding loop
        '''
        pass
