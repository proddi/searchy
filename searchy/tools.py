from . import Token
import re


#-----------------------------------------------------------
#   TOKENIZER
#-----------------------------------------------------------

class Tokenizer(object):
    def __ror__(self, tokenizer):
        assert isinstance(tokenizer, Tokenizer) or isinstance(tokenizer, function)
        return TokenizerPipe(self, tokenizer)

class TokenizerPipe(Tokenizer):
    def __init__(self, left, right):
        super(Tokenizer, self).__init__()
        self._left = left
        self._right = right
    def __call__(self, tokens):
        for token in self._left(self._right(tokens)):
            yield token

class WhitespaceTokenizer(Tokenizer):
    def __call__(self, tokens):
        for token in tokens:
            i = token.pos
            for piece in token.text.split(" "):
                yield Token(piece, i)
                i += len(piece)+1

class RegexTokenizer(Tokenizer):
    def __init__(self, expression=re.compile(r"\w+(\.?\w+)*"), gaps=False):
        super(RegexTokenizer, self).__init__()
        self._expression = expression
    def __call__(self, tokens):
        for token in tokens:
            for pos, match in enumerate(self._expression.finditer(token.text)):
                yield Token(match.group(0), pos)

class NGramTokenizer(Tokenizer):
    def __init__(self, minsize=2, maxsize=4):
        super(NGramTokenizer, self).__init__()
        self._minsize = minsize
        self._maxsize = maxsize
    def __call__(self, tokens):
        for token in tokens:
            word = token.text
            for i in range(len(word)-2):
                yield Token(word[i:i+3], i+token.pos)

def NgramWordTokenizer():
    return RegexTokenizer() | StopFilter() | LowercaseFilter() | NGramTokenizer()
#-----------------------------------------------------------
#   FILTER
#-----------------------------------------------------------

class Filter(Tokenizer):
    pass

class LowercaseFilter(Filter):
    def __call__(self, tokens):
        for token in tokens:
            token.text = token.text.lower()
            yield token

STOP_WORDS = set(('a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'can',
                        'for', 'from', 'have', 'if', 'in', 'is', 'it', 'may',
                        'not', 'of', 'on', 'or', 'tbd', 'that', 'the', 'this',
                        'to', 'us', 'we', 'when', 'will', 'with', 'yet',
                        'you', 'your'))

class StopFilter(Filter):
    def __init__(self, words=STOP_WORDS):
        super(StopFilter, self).__init__()
        self._words = words
    def __call__(self, tokens):
        for token in tokens:
            if token.text not in self._words:
                yield token
