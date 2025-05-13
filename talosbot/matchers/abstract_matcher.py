from abc import ABC, abstractmethod


class AbstractMatcher(ABC):
    ''' Abstract matcher '''
    
    def __init__(self) -> None:
        self.available_skills = {}
        self.args = []
    
    def match(self, sentence: str, patterns=None):
        '''
        This decorator method works the register of all the available skills,
        the actual match happens at the sentence matcher method
        '''
        def decorator(skill_func):
            self.available_skills[sentence] = {
                'func': skill_func,
                }
            if patterns is not None:
                self.available_skills[sentence]['patterns'] = patterns
            return skill_func
        return decorator
    
    def default_match(self):
        '''
        Decorator method for overriding a default skill
        '''
        def decorator(skill_func):
            self.default_skill = skill_func
            return skill_func
        return decorator
    
    def default_skill(self) -> str:
        '''
        Generic default skill, notice you can override it in the specific matcher
        and the user can override it with its own using default match decorator
        '''
        return 'I have no skill for that, sorry!'
    
    @abstractmethod
    def sentence_matcher(self, input_sentence: str) -> str:
        '''
        The matcher implementation requires this method with the matching logic
        '''
        pass
