class AmbiguousScoreException(Exception):
    ''' Use it when you cannot determine the match from multiple candidates '''
    pass

class NoMatchingSkillException(Exception):
    ''' Use it when there's not a match '''
    pass
