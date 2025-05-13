import re
from talosbot.matchers.abstract_matcher import AbstractMatcher
from talosbot.matchers.exceptions import NoMatchingSkillException

class RegexMatcher(AbstractMatcher):
    ''' Matcher with regular expresions '''
    def __init__(self) -> None:
        super().__init__()
    
    def match_sentences(self, sentences: list, input_sentence: str) -> list:
        '''
        The actual matching implementation
        '''
        results = []
        for sentence in sentences:
            if re.match(sentence, input_sentence):
                results.append(sentence)
        return results

    def sentence_matcher(self, input_sentence: str) -> str:
        '''
        Regex sentence matcher that returns the first occurrence
        '''
        sentences = list(self.available_skills.keys())
        results = self.match_sentences(sentences, input_sentence)
        # Check results are returned
        if len(results) == 0:
            raise NoMatchingSkillException("Couldn't match any sentence")
        # Just return always the first match
        matched_sentence = results[0]
        return matched_sentence
