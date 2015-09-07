token_index = {}  # word -> document

hash_tokens = {}

class Index(object):
    def __init__(self, backend=None, tokenizer=None):
        self._backend = backend
        self._tokenizer = tokenizer

    def debug(self):
        for field, index in token_index.iteritems():
            for h, datas in index.iteritems():
                print "- %s.%s: %s" % (field, hash_tokens[h], datas)

    def stats(self):
        c = 0
        for field, index in token_index.iteritems():
            c += len(index)
        return {
            "tokens": len(hash_tokens),
            "total": c,
            "fields": token_index.keys(),
        }


    def add(self, data=None, **fields):
        print "Index.add(%s)" % fields

        for field, text in fields.iteritems():
            index = token_index.setdefault(field, {})
            for token in self._tokenizer([Token(text, 0)]):
                index.setdefault(token.id(), []).append((data, token.pos))
                hash_tokens.setdefault(token.id(), token)

    def query(self, **fields):
        print "Index.query(%s)" % fields
        results = {}
        for field, text in fields.iteritems():
            index = token_index.get(field, {})
            tokens = list(self._tokenizer([Token(text, 0)]))
            print " (%s tokens)" % len(tokens)
            score = 1.0/len(tokens)
            for token in tokens:
                for data, pos in index.get(token.id(), []):
                    results.setdefault(data, 0.0)
                    results[data] += score * token.score

        for data, score in results.iteritems():
            yield data, score

class Token(object):
    def __init__(self, text, pos):
        self.text = text
        self.pos = pos
        self.score = 1
    def __str__(self):
        return "<%s:%d>" % (self.text, self.pos)
    def __repr__(self):
        return "<%s:%d>" % (self.text, self.pos)
    def id(self):
        return hash(self.text)
