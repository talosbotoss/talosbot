from talosbot.matchers.exceptions import NoMatchingSkillException
from talosbot import logger


class Message(object):
    ''' Message class with the raw message string and an optinal meta dict with any custom objects '''
    def __init__(self, message, meta=None):
        self.message = message
        self.meta = meta

class Bot(object):
    ''' Bot main class '''
    def __init__(self, matcher, parser, channel) -> None:
        self.matcher = matcher
        self.parser = parser
        self.channel = channel
        self.default_match = matcher.default_match
        self.channel.set_bot(self)

    def match(self, sentence: str, patterns: str):
        '''
        Makes accessible from the bot, the match decorator method from the matcher
        '''
        if type(patterns) not in (list, tuple, dict, None):
            msg = f'Unsupported type {type(patterns)} for patterns'
            raise Exception(msg)
        return self.matcher.match(sentence, patterns)
    
    def execute_skill(self, sentence: str) -> str:
        '''
        Gets a sentence, then the matching and params extraction (if any) is executed,
        at last, the result obtained from the skill is returned
        '''
        skill_function = self.matcher.default_skill
        skill_patterns = dict()
        extracted_patterns = dict()
        try:
            matched_sentence = self.matcher.sentence_matcher(sentence)
            skill_function = self.matcher.available_skills[matched_sentence]['func']
            skill_patterns = self.matcher.available_skills[matched_sentence]['patterns']
            extracted_patterns = self.parser.extract_parameters(sentence=sentence, extraction_patterns=skill_patterns)
        except NoMatchingSkillException as e:
            msg = f'Cannot match any sentence, getting the default one\n{e}'
            logger.warning(msg)
        finally:
            logger.debug(f'Extracted parameters: {extracted_patterns}')
            result = skill_function(**extracted_patterns)
            return result
    
    async def async_execute_skill(self, sentence: str) -> str:
        '''
        Async version of execute skill method,
        use it when you are using a library that implements coroutines
        '''
        return self.execute_skill(sentence)

    async def async_message_handler(self, user_message: Message) -> Message:
        '''
        Async version for the message handler method
        '''
        sentence = user_message.message
        result_message = await self.async_execute_skill(sentence)
        result = Message(result_message, user_message.meta)
        return result
    
    def message_handler(self, user_message: Message) -> Message:
        '''
        Gets a message, passes the raw string to the execute skill method and
        builds the response returned as a Message object again
        '''
        sentence = user_message.message
        result_message = self.execute_skill(sentence)
        result = Message(result_message, user_message.meta)
        return result

    def run(self) -> None:
        '''
        Main module execution
        '''
        self.channel.establish()
