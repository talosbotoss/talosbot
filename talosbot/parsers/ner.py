import random
import spacy
import json
import jsonschema
from importlib.util import find_spec
from pathlib import Path

import spacy.cli
import spacy.cli.download
from talosbot import logger
from talosbot.parsers.abstract_parser import AbstractParser
from talosbot.parsers.exceptions import MissingParametersException

class NERParser(AbstractParser):
    ''' NER parser that uses a spacy model, so it's flexible enough to customize it '''

    def __init__(self, model_path) -> None:
        super().__init__()
        self.model = spacy.load(model_path)
    
    def extract_parameters(self, sentence: str, extraction_patterns: list, all_required=True) -> dict:
        ''' Extraction of the detected entities '''
        doc = self.model(sentence)
        entities = set(extraction_patterns)
        parameters = dict()
        for entity in entities:
            logger.debug(f'Found user defined entity: {entity}')
            parameters[entity] = None
            for ent in doc.ents:
                ent_found = ent.label_
                text = ent.text
                logger.debug(f'Doc ent=[{ent_found}] has text=[{text}]')
                if ent_found == entity:
                    parameters[entity] = text
            if parameters[entity] is None and all_required:
                raise MissingParametersException(f'Could not extract any parameter for {entity} entity')
        return parameters

class NERTrainer(object):
    ''' NER trainer is a static class to train a custom model from a training set '''
    TRAINING_SET_SCHEMA = '''
    {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "meta": {
            "type": "object",
            "properties": {
                "labels": {
                    "type": "array",
                    "description": "A list with the entity labels in the training data"
                }
            },
            "required": ["labels"]
        },
        "training_data": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "sentence": {
                        "type": "string",
                        "description": "Text input containing an example sentence."
                    },
                    "entities": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "label": {
                                    "type": "string",
                                    "description": "Entity name label."
                                },
                                "start": {
                                    "type": "integer",
                                    "minimum": 0,
                                    "description": "Start index of the entity in the example sentence."
                                },
                                "end": {
                                    "type": "integer",
                                    "minimum": 0,
                                    "description": "End index of the entity in the example sentence."
                                }
                            },
                            "required": ["label", "start", "end"]
                        }
                    }
                },
                "required": ["sentence", "entities"]
            }
        }
    },
        "required": ["meta", "training_data"]
    }
    '''

    def __new__(cls):
        '''
        Avoid this class to get an instance
        '''
        raise TypeError('Cannot instansiate this static class')
    
    @classmethod
    def load_training_set(cls, path: str) -> dict:
        '''
        Gets a valid path with a json trianing set,
        then verifies the json payload,
        at last, returns the 
        '''
        schema = json.loads(cls.TRAINING_SET_SCHEMA)
        with open(path, 'r') as json_file:
            training_set = json.load(json_file)
        jsonschema.validate(training_set, schema)
        return training_set
    
    @classmethod
    def save_model(cls, model: spacy.language.Language, output_dir: str) -> None:
        '''
        Save model into an output directory
        '''
        if output_dir is not None:
            output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        model.to_disk(output_dir)
        logger.info(f'Model saved into {output_dir}')
    
    @classmethod
    def train_model(cls, model: spacy.language.Language, training_set: dict, n_iter: int = 100) -> None:
        '''
        Get a well formatted training set
        and generates a model in the specified path
        '''
        training_data = training_set['training_data']
        # Setup the ner pipe and put the custom labels
        if 'ner' not in model.pipe_names:
            ner = model.add_pipe('ner')
        else:
            ner = model.get_pipe('ner')
        for label in training_set['meta']['labels']:
            if label not in ner.labels:
                ner.add_label(label)
        # Initialize the model
        model.initialize()
        # Disable other pipes and train only NER
        other_pipes = [pipe for pipe in model.pipe_names if pipe != 'ner']
        with model.disable_pipes(*other_pipes):
            optimizer = model.create_optimizer()
            for ith in range(n_iter):
                logger.debug(f'Starting iteration #{ith}')
                random.shuffle(training_data)
                losses = {}
                for raw_example in training_data:
                    doc = model.make_doc(raw_example['sentence'])
                    entities = [(ent['start'], ent['end'], ent['label']) for ent in raw_example['entities']]
                    example = spacy.training.example.Example.from_dict(doc, {"entities": entities})
                    model.update(
                        [example],
                        drop=0.5,
                        sgd=optimizer,
                        losses=losses)
                    logger.debug(losses)
                logger.info(f'Iteration {ith} - Losses: {losses}')
                logger.debug(f'End of iteration #{ith}')

    
    @classmethod
    def build_model(cls, from_model: str = None) -> spacy.language.Language:
        '''
        Load a model from blank default or load specified model
        '''
        if from_model:
            if not find_spec(from_model):
                # If the model is not found, try to download it
                spacy.cli.download(from_model)
            model = spacy.load(from_model)
            logger.info(f'Loaded model: {from_model}')
        else:
            model = spacy.blank('en')
            logger.info(f'Created blank "en" model')
        return model

    @classmethod
    def run(cls, training_set_path: str, output_model: str, from_model: str = None) -> None:
        '''
        Main program execution
        '''
        model = cls.build_model(from_model)
        training_set = cls.load_training_set(training_set_path)
        cls.train_model(model, training_set)
        cls.save_model(model, output_model)
        