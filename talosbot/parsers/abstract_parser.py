from abc import ABC, abstractmethod


class AbstractParser(ABC):
    ''' Abstract parser '''
    
    def __init__(self) -> None:
        pass
    
    @abstractmethod
    def extract_parameters(self, sentence: str, extraction_patterns: list|dict, all_required: bool=True) -> dict:
        '''
        The parser implementation requires this method with the extraction logic
        '''
        pass
