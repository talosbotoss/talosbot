from talosbot.channels.abstract_channel import AbstractChannel
from talosbot.talos import Message
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


class TelegramChannel(AbstractChannel):
    ''' Channel for Telegram '''

    def __init__(self, token, restricted=False, white_list=[], trigger_word='talos') -> None:
        super().__init__()
        self.token = token
        self.restricted = restricted
        self.white_list = white_list
        self.app = ApplicationBuilder().token(self.token).build()
        self.app.add_handler(CommandHandler(trigger_word, self.recieve_message))

    def establish(self):
        '''
        Establishes a connection so it has implemented its loop until interruption signal
        '''
        self.app.run_polling()

    async def recieve_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> Message:
        '''
        When a message is recieved, the message handler is called,
        then sends the response with the dispatch method
        '''
        user_message = ' '.join(context.args).strip()
        meta = {
            'update': update,
            'context': context,
        }
        if not self.restricted or update.effective_user.id in self.white_list:
            message = Message(user_message, meta)
            response_message = await self.bot.async_message_handler(message)
        else:
            response_message = Message(f'Access denied for user with ID {update.effective_user.id}', meta=meta)
        await self.dispatch_message(response_message)
    
    async def dispatch_message(self, message: Message) -> None:
        '''
        Uses the message meta object to send the response message back
        '''
        update = message.meta['update']
        user_message = message.message
        await update.message.reply_text(user_message)
