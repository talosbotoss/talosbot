import argparse
from talosbot.parsers.ner import NERTrainer

class TalosCLI(object):
    ''' Talos CLI '''
    
    def __new__(cls):
        '''
        Avoid this class to get an instance
        '''
        raise TypeError('Cannot instansiate this static class')
    
    @classmethod
    def ner_trainer(cls, training_set: str, output: str, model: str = None) -> None:
        NERTrainer.run(training_set, output, model)

    @classmethod
    def run(cls) -> None:
        '''
        Main method where all available subcommands are passed through
        '''
        parser = argparse.ArgumentParser(prog='talos', description='Talos CLI')
        subparsers = parser.add_subparsers(dest='command', required=True)

        # Command for 'nertrainer'
        parser_trainer = subparsers.add_parser('trainer', help='Train the NER model')
        parser_trainer.add_argument('--trainingset', metavar='TRAINING_SET', required=True, help='Training set file')
        parser_trainer.add_argument('--output', metavar='DIR', required=True, help='Output empty dir for the generated model')
        parser_trainer.add_argument('--model', metavar='NAME', required=False, help='Model name to use instead creating a blank new one')

        args = parser.parse_args()

        if args.command == 'trainer':
            cls.ner_trainer(args.trainingset, args.output, args.model)
