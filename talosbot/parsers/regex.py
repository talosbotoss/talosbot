import re
from talosbot.parsers.abstract_parser import AbstractParser
from talosbot.parsers.exceptions import MissingParametersException


class RegexParser(AbstractParser):
    ''' Parser using regular expressions '''
    def __init__(self) -> None:
        super().__init__()

    def extract_parameters(self, sentence: str, extraction_patterns: dict, all_required: bool=True) -> dict:
        ''' This method uses search so it's an implicit .* at the begining '''
        parameters = dict()
        for name, expression in extraction_patterns.items():
            match = re.search(expression, sentence)
            if match:
                parameters[name] = match.group(1)
            elif all_required:
                raise MissingParametersException(f'Missing required parameter: {name}')
        return parameters
