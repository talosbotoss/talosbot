from numpy import ndarray
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from talosbot.matchers.abstract_matcher import AbstractMatcher
from talosbot.matchers.exceptions import AmbiguousScoreException, NoMatchingSkillException


class BertMatcher(AbstractMatcher):
    ''' Matcher using BERT sentence transformer with cosine similarity '''
    
    DEFAULT_MODEL = 'bert-base-nli-mean-tokens'
    DEFAULT_ACCEPTANCE_THRESHOLD = .8
    
    def __init__(self, **kwargs) -> None:
        super().__init__()
        model_name = kwargs.get('model', self.DEFAULT_MODEL)
        self.model = SentenceTransformer(model_name)
        self.acceptance_threshold = kwargs.get('acceptance_threshold', self.DEFAULT_ACCEPTANCE_THRESHOLD)
    
    def get_similarities(self, sentences: list, pattern: str) -> ndarray:
        '''
        Executes the cosine similarity and returns its scores
        '''
        sentences = [pattern] + sentences
        sentence_embeddings = self.model.encode(sentences)
        cosine_similarity_results = cosine_similarity([sentence_embeddings[0]], sentence_embeddings[1:])
        return cosine_similarity_results
    
    def match_sentence(self, sentence: str, pattern: str) -> dict[str, float | bool]:
        '''
        Obtains a cosine similarity score from a single sentence
        '''
        cosine_similarity_result = self.get_similarities([sentence], pattern)
        score = float(cosine_similarity_result[0][0])
        passed = score >= self.acceptance_threshold
        result = {"score": score, "passed": passed}
        return result
    
    def match_sentences(self, sentences: list, pattern: str) -> dict[str, str | float | bool]:
        '''
        Obtains a cosine similarity scores from a list of sentences
        '''
        cosine_similarity_results = self.get_similarities(sentences, pattern)
        results = []
        for result, sentence in zip(cosine_similarity_results[0], sentences):
            score = float(result)
            passed = score >= self.acceptance_threshold
            results.append({"sentence": sentence,
                            "score": score,
                            "passed": passed,
                           })
        return results
    
    def sentence_matcher(self, input_sentence: str) -> str:
        sentences = list(self.available_skills.keys())
        results = self.match_sentences(sentences, input_sentence)
        # Check results are returned
        if len(results) == 0:
            raise NoMatchingSkillException("Couldn't match any sentence")
        # Validate at least one threshold score exist and there is no ambiguity
        scores = []
        for result in results:
            scores.append(result['score'])
        if scores[-1] < self.acceptance_threshold:
            raise NoMatchingSkillException(f"The maximum score ({scores[-1]}) doesn't reach the acceptance_threshold ({self.acceptance_threshold})")
        if len(scores) > 1:
            if sorted(scores)[-2:][0] == sorted(scores)[-2:][1]:
                raise AmbiguousScoreException(f'Abiguous score, two sentences matched the same maximum score of {sorted(scores)[-2:][0]}')
        # Now everything is ok, look for the maximum scored sentence
        current_maximum_score = 0
        for result in results:
            current_score = result['score']
            if current_score > current_maximum_score:
                current_maximum_score = current_score
                matched_sentence = result['sentence']
        return matched_sentence
